#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import argparse as _argparse
import commandant as _commandant
import csv as _csv
import fnmatch as _fnmatch
import functools as _functools
import http.server as _http
import markdown2 as _markdown
import os as _os
import re as _re
import shutil as _shutil
import subprocess as _subprocess
import threading as _threading
import types as _types

from collections import defaultdict as _defaultdict
from urllib import parse as _urlparse
from xml.etree.ElementTree import XML as _XML
from xml.sax.saxutils import escape as _xml_escape

_default_body_template = "<body>{{page.content}}</body>"
_default_page_template = "{{page.body}}"
_markdown_title_regex = _re.compile(r"(#|##)(.+)")
_reload_script = "<script src=\"http://localhost:35729/livereload.js\"></script>"
_variable_regex = _re.compile("({{.+?}})")

_markdown_extras = {
    "code-friendly": True,
    "footnotes": True,
    "header-ids": True,
    "markdown-in-html": True,
    "tables": True,
}

class Transom:
    def __init__(self, config_dir, input_dir, output_dir):
        self.config_dir = config_dir
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.verbose = False
        self.quiet = False
        self._reload = False

        self._config_file = _os.path.join(self.config_dir, "config.py")
        self._config = None

        self._body_template = None
        self._page_template = None

        self._files = list()
        self._files_by_url = dict()

        self._ignored_file_patterns = [".git", ".svn", ".#*", "#*"]
        self._ignored_link_patterns = []

        self._markdown_converter = _markdown.Markdown(extras=_markdown_extras)

    def init(self):
        self._page_template = _load_template(_os.path.join(self.config_dir, "default-page.html"), _default_page_template)
        self._body_template = _load_template(_os.path.join(self.config_dir, "default-body.html"), _default_body_template)

        self._config = {
            "site": self,
            "ignored_files": self._ignored_file_patterns,
            "ignored_links": self._ignored_link_patterns,
            "lipsum": _lipsum,
            "html_table": _html_table,
            "html_table_csv": _html_table_csv,
        }

        if _os.path.isfile(self._config_file):
            exec(_read_file(self._config_file), self._config)

    def _init_files(self):
        for root, dirs, files in _os.walk(self.input_dir):
            files = {x for x in files if not self._is_ignored_file(x)}
            index_files = {x for x in files if x in ("index.md", "index.html.in", "index.html")}

            for name in index_files:
                self._init_file(_os.path.join(root, name))

            for name in files - index_files:
                self._init_file(_os.path.join(root, name))

    def _is_ignored_file(self, name):
        for pattern in self._ignored_file_patterns:
            if _fnmatch.fnmatchcase(name, pattern):
                return True

        return False

    def _init_file(self, input_path):
        output_path = _os.path.join(self.output_dir, input_path[len(self.input_dir) + 1:])

        if input_path.endswith(".md"):
            return _MarkdownPage(self, input_path, f"{output_path[:-3]}.html")
        elif input_path.endswith(".html.in"):
            return _TemplatePage(self, input_path, output_path[:-3])
        else:
            return _File(self, input_path, output_path)

    def render(self, force=False, serve=None):
        self.notice("Rendering input files")

        if serve is not None:
            self._reload = True

        self._init_files()

        for file_ in self._files:
            self.info("Processing {}", file_)
            file_._process_input()

        for file_ in self._files:
            if file_._is_modified() or force:
                self.info("Rendering {}", file_)
                file_._render_output()

        if _os.path.exists(self.output_dir):
            _os.utime(self.output_dir)

        if serve is not None:
            self._serve(serve)

    def _serve(self, port):
        try:
            watcher = _WatcherThread(self)
            watcher.start()
        except ImportError:
            self.notice("Failed to import pyinotify, so I won't auto-render updated input files")
            self.notice("Try installing the python3-pyinotify package")

        try:
            livereload = _subprocess.Popen(f"livereload {self.output_dir}", shell=True)
        except _subprocess.CalledProcessError as e:
            self.notice("Failed to start the livereload server, so I won't auto-reload the browser")
            self.notice("Use 'npm install -g livereload' to install the server")
            self.notice("Subprocess error: {}", e)

            livereload = None

        try:
            server = _ServerThread(self, port)
            server.run()
        finally:
            if livereload is not None:
                livereload.terminate()

    def _render_one_file(self, input_path):
        self.notice("Rendering {}", input_path)

        file_ = self._init_file(input_path)
        file_._process_input()
        file_._render_output()

        _os.utime(self.output_dir)

    def check_files(self):
        self._init_files()

        expected_paths = {x._output_path for x in self._files}
        found_paths = self._find_output_paths()

        missing_paths = expected_paths.difference(found_paths)
        extra_paths = found_paths.difference(expected_paths)

        if missing_paths:
            print("Missing output files:")

            for path in sorted(missing_paths):
                print(f"  {path}")

        if extra_paths:
            print("Extra output files:")

            for path in sorted(extra_paths):
                print(f"  {path}")

        return len(missing_paths), len(extra_paths)

    def _find_output_paths(self):
        output_paths = set()

        for root, dirs, files in _os.walk(self.output_dir):
            output_paths.update({_os.path.join(root, x) for x in files})

        return output_paths

    def check_links(self):
        link_sources = _defaultdict(set) # link => files
        link_targets = set()

        self._init_files()

        for file_ in self._files:
            try:
                file_._collect_link_data(link_sources, link_targets)
            except Exception as e:
                self.warn("Error collecting link data from {}: {}", file_, str(e))

        def retain(link):
            for pattern in self._ignored_link_patterns:
                if _fnmatch.fnmatchcase(link, pattern):
                    return False

            return True

        links = filter(retain, link_sources.keys())
        errors = 0

        for link in links:
            if link not in link_targets:
                errors += 1

                print(f"Error: Link to '{link}' has no destination")

                for source in link_sources[link]:
                    print(f"  Source: {source._input_path}")

        return errors

    def info(self, message, *args):
        if self.verbose:
            print(message.format(*args))

    def notice(self, message, *args):
        if not self.quiet:
            print(message.format(*args))

    def warn(self, message, *args):
        print("Warning!", message.format(*args))

class _File:
    __slots__ = "site", "_input_path", "_input_mtime", "_output_path", "_output_mtime", "url", "parent"

    def __init__(self, site, input_path, output_path):
        self.site = site

        self._input_path = input_path
        self._input_mtime = _os.path.getmtime(self._input_path)

        self._output_path = output_path
        self._output_mtime = None

        self.url = self._output_path[len(self.site.output_dir):]
        self.parent = None

        if self.url != "/index.html":
            parent_dir, name = _os.path.split(self.url)

            if name == "index.html":
                parent_dir = _os.path.dirname(parent_dir)

            self.parent = self.site._files_by_url.get(_os.path.join(parent_dir, "index.html"))

        self.site._files.append(self)
        self.site._files_by_url[self.url] = self

    def __repr__(self):
        return f"{self.__class__.__name__}({self._input_path}, {self._output_path})"

    def _process_input(self):
        pass

    def _is_modified(self):
        if self._output_mtime is None:
            try:
                self._output_mtime = _os.path.getmtime(self._output_path)
            except FileNotFoundError:
                return True

        return self._input_mtime > self._output_mtime

    def _render_output(self):
        _copy_file(self._input_path, self._output_path)

    def _collect_link_data(self, link_sources, link_targets):
        link_targets.add(self.url)

        if not self.url.endswith(".html"):
            return

        root = _XML(_read_file(self._output_path))

        for elem in root.iter("*"):
            for name in ("href", "src", "action"):
                try:
                    url = elem.attrib[name]
                except KeyError:
                    continue

                split_url = _urlparse.urlsplit(url)

                if split_url.scheme or split_url.netloc:
                    continue

                normalized_url = _urlparse.urljoin(self.url, _urlparse.urlunsplit(split_url))

                link_sources[normalized_url].add(self)

        for elem in root.iter("*"):
            if "id" in elem.attrib:
                normalized_url = _urlparse.urljoin(self.url, f"#{elem.attrib['id']}")

                if normalized_url in link_targets:
                    self.site.info("Duplicate link target in '{}'", normalized_url)

                link_targets.add(normalized_url)

class _TemplatePage(_File):
    __slots__ = "_content", "_attributes", "title", "_page_template", "_body_template"

    def _process_input(self):
        self._content = _read_file(self._input_path)
        self._content, self._attributes = _extract_metadata(self._content)

        self.title = self._attributes.get("title", "")

        try:
            self._page_template = _load_template(self._attributes["page_template"], _default_page_template)
        except KeyError:
            self._page_template = self.site._page_template

        try:
            self._body_template = _load_template(self._attributes["body_template"], _default_body_template)
        except KeyError:
            self._body_template = self.site._body_template

    def _render_output(self):
        _make_dir(_os.path.dirname(self._output_path))

        with open(self._output_path, "w") as f:
            for elem in self._render_template(self._page_template):
                f.write(elem)

    @property
    def reload_script(self):
        return _reload_script if self.site._reload else ""

    @property
    def extra_headers(self):
        return self._attributes.get("extra_headers", "")

    @property
    def body(self):
        return self._render_template(self._body_template)

    @property
    def content(self):
        self._convert_content()
        return self._render_template(_parse_template(self._content))

    def _convert_content(self):
        pass

    @property
    def path_nav_links(self):
        files = [self]
        file_ = self.parent

        while file_ is not None:
            files.append(file_)
            file_ = file_.parent

        return [f"<a href=\"{x.url}\">{x.title}</a>" for x in reversed(files)]

    def path_nav(self, start=None, end=None):
        return f"<nav id=\"-path-nav\">{''.join(self.path_nav_links[start:end])}</nav>"

    def _render_template(self, template):
        for elem in template:
            if type(elem) is _types.CodeType:
                result = eval(elem, self.site._config, {"page": self})

                if type(result) is _types.GeneratorType:
                    yield from result
                else:
                    yield result
            else:
                yield elem

    def include(self, input_path):
        content = _read_file(input_path)

        if input_path.endswith(".md"):
            content = self.site._markdown_converter.convert(content)

        return self._render_template(_parse_template(content))

class _MarkdownPage(_TemplatePage):
    __slots__ = ()

    def _process_input(self):
        super()._process_input()

        if not self.title:
            match = _markdown_title_regex.search(self._content)
            self.title = match.group(2).strip() if match else ""

    def _convert_content(self):
        # Strip out comments
        content_lines = self._content.splitlines()
        content_lines = (x for x in content_lines if not x.startswith(";;"))

        self._content = _os.linesep.join(content_lines)
        self._content = self.site._markdown_converter.convert(self._content)

class _WatcherThread(_threading.Thread):
    def __init__(self, site):
        import pyinotify as _pyinotify

        super().__init__()

        self.site = site
        self.daemon = True

        watcher = _pyinotify.WatchManager()
        mask = _pyinotify.IN_CREATE | _pyinotify.IN_DELETE | _pyinotify.IN_MODIFY

        def render(event):
            input_path = _os.path.relpath(event.pathname, _os.getcwd())

            if _os.path.isdir(input_path) or self.site._is_ignored_file(_os.path.basename(input_path)):
                return True

            self.site._render_one_file(input_path) # XXX Handle delete

        watcher.add_watch(self.site.input_dir, mask, render, rec=True, auto_add=True)

        self.notifier = _pyinotify.Notifier(watcher)

    def run(self):
        self.site.notice("Watching for input file changes")
        self.notifier.loop()

class _ServerThread(_threading.Thread):
    def __init__(self, site, port):
        super().__init__()

        self.site = site
        self.port = port
        self.daemon = True

        address = "localhost", self.port
        handler = _functools.partial(_http.SimpleHTTPRequestHandler, directory=self.site.output_dir)

        self.server = _http.ThreadingHTTPServer(address, handler)

    def run(self):
        self.site.notice("Serving at http://localhost:{}", self.port)
        self.server.serve_forever()

_description = """
Generate static websites from Markdown and Python
"""

_epilog = """
subcommands:
  init                  Prepare an input directory
  render                Generate the output files
  check-links           Check for broken links
  check-files           Check for missing or extra files
"""

class TransomCommand(_commandant.Command):
    def __init__(self, home=None):
        super().__init__(home=home, name="transom", standard_args=False)

        self.description = _description
        self.epilog = _epilog

        subparsers = self.add_subparsers()

        init = subparsers.add_parser("init")
        init.description = "Prepare an input directory"
        init.set_defaults(func=self.init_command)
        init.add_argument("config_dir", metavar="CONFIG-DIR",
                          help="Read config files from CONFIG-DIR")
        init.add_argument("input_dir", metavar="INPUT-DIR",
                          help="Place default input files in INPUT-DIR")
        init.add_argument("--quiet", action="store_true",
                          help="Print no logging to the console")
        init.add_argument("--verbose", action="store_true",
                          help="Print detailed logging to the console")
        init.add_argument("--init-only", action="store_true",
                          help=_argparse.SUPPRESS)

        render = subparsers.add_parser("render")
        render.description = "Generate output files"
        render.set_defaults(func=self.render_command)
        render.add_argument("config_dir", metavar="CONFIG-DIR",
                            help="Read config files from CONFIG-DIR")
        render.add_argument("input_dir", metavar="INPUT-DIR",
                            help="Read input files from INPUT-DIR")
        render.add_argument("output_dir", metavar="OUTPUT-DIR",
                            help="Write output files to OUTPUT-DIR")
        render.add_argument("--force", action="store_true",
                            help="Render all input files, including unmodified ones")
        render.add_argument("--serve", type=int, metavar="PORT",
                            help="Serve the site and rerender when input files change")
        render.add_argument("--quiet", action="store_true",
                            help="Print no logging to the console")
        render.add_argument("--verbose", action="store_true",
                            help="Print detailed logging to the console")
        render.add_argument("--init-only", action="store_true",
                            help=_argparse.SUPPRESS)

        check_links = subparsers.add_parser("check-links")
        check_links.description = "Check for broken links"
        check_links.set_defaults(func=self.check_links_command)
        check_links.add_argument("config_dir", metavar="CONFIG-DIR",
                                 help="Read config files from CONFIG-DIR")
        check_links.add_argument("input_dir", metavar="INPUT-DIR",
                                 help="Check input files in INPUT-DIR")
        check_links.add_argument("output_dir", metavar="OUTPUT-DIR",
                                 help="Check output files in OUTPUT-DIR")
        check_links.add_argument("--quiet", action="store_true",
                                 help="Print no logging to the console")
        check_links.add_argument("--verbose", action="store_true",
                                 help="Print detailed logging to the console")
        check_links.add_argument("--init-only", action="store_true",
                                 help=_argparse.SUPPRESS)

        check_files = subparsers.add_parser("check-files")
        check_files.description = "Check for missing or extra files"
        check_files.set_defaults(func=self.check_files_command)
        check_files.add_argument("config_dir", metavar="CONFIG-DIR",
                                 help="Read config files from CONFIG-DIR")
        check_files.add_argument("input_dir", metavar="INPUT-DIR",
                                 help="Check input files in INPUT-DIR")
        check_files.add_argument("output_dir", metavar="OUTPUT-DIR",
                                 help="Check output files in OUTPUT-DIR")
        check_files.add_argument("--quiet", action="store_true",
                                 help="Print no logging to the console")
        check_files.add_argument("--verbose", action="store_true",
                                 help="Print detailed logging to the console")
        check_files.add_argument("--init-only", action="store_true",
                                 help=_argparse.SUPPRESS)

        self.lib = None

    def init(self):
        super().init()

        if "func" not in self.args:
            self.fail("Missing subcommand")

    def init_lib(self):
        assert self.lib is None

        self.lib = Transom(self.args.config_dir, self.args.input_dir, self.args.output_dir)
        self.lib.verbose = self.args.verbose
        self.lib.quiet = self.args.quiet

        self.lib.init()

        if self.args.init_only:
            self.parser.exit()

    def run(self):
        self.args.func()

    def init_command(self):
        if self.home is None:
            self.fail("I can't find the default input files")

        def copy(file_name, to_path):
            if _os.path.exists(to_path):
                self.notice("Skipping '{}'. It already exists.", to_path)
                return

            _copy_file(_os.path.join(self.home, "files", file_name), to_path)

            self.notice("Creating '{}'", to_path)

        if self.args.init_only:
            self.parser.exit()

        copy("default-page.html", _os.path.join(self.args.config_dir, "default-page.html"))
        copy("default-body.html", _os.path.join(self.args.config_dir, "default-body.html"))
        copy("config.py", _os.path.join(self.args.config_dir, "config.py"))

        copy("main.css", _os.path.join(self.args.input_dir, "main.css"))
        copy("main.js", _os.path.join(self.args.input_dir, "main.js"))
        copy("index.md", _os.path.join(self.args.input_dir, "index.md"))

    def render_command(self):
        self.init_lib()
        self.lib.render(force=self.args.force, serve=self.args.serve)

    def check_links_command(self):
        self.init_lib()

        errors = self.lib.check_links()

        if errors == 0:
            self.notice("PASSED")
        else:
            self.fail("FAILED")

    def check_files_command(self):
        self.init_lib()

        missing_files, extra_files = self.lib.check_files()

        if extra_files != 0:
            self.warn("{} extra files in the output", extra_files)

        if missing_files == 0:
            self.notice("PASSED")
        else:
            self.fail("FAILED")

def _make_dir(path):
    _os.makedirs(path, exist_ok=True)

def _read_file(path):
    with open(path, "r") as file_:
        return file_.read()

def _copy_file(from_path, to_path):
    _make_dir(_os.path.dirname(to_path))
    _shutil.copyfile(from_path, to_path)

def _extract_metadata(content):
    attributes = dict()

    if content.startswith("---\n"):
        end = content.index("---\n", 4)
        lines = content[4:end].strip().split("\n")

        for line in lines:
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip()

            if value.lower() in ("none", "null"):
                value = None

            attributes[key] = value

        content = content[end + 4:]

    return content, attributes

def _load_template(path, default_text):
    if path is None:
        return list(_parse_template(default_text))

    return list(_parse_template(_read_file(path)))

def _parse_template(text):
    for token in _variable_regex.split(text):
        if token.startswith("{{") and token.endswith("}}"):
            yield compile(token[2:-2], "<string>", "eval")
        else:
            yield token

_lipsum_words = [
    "Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit.",
    "Vestibulum", "enim", "urna,", "ornare", "pellentesque", "felis", "eget,", "maximus", "lacinia", "lorem.",
    "Nulla", "auctor", "massa", "vitae", "ultricies", "varius.",
    "Curabitur", "consectetur", "lacus", "sapien,", "a", "lacinia", "urna", "tempus", "quis.",
    "Vestibulum", "vitae", "augue", "non", "augue", "lobortis", "semper.",
    "Nullam", "fringilla", "odio", "quis", "ligula", "consequat", "condimentum.",
    "Integer", "tempus", "sem.",
]

def _lipsum(count=50):
    words = (_lipsum_words[i % len(_lipsum_words)] for i in range(count))
    text = " ".join(words)

    if text.endswith(","):
        text = text[:-1] + "."

    if not text.endswith("."):
        text = text + "."

    return text

def _html_table_csv(path, **attrs):
    with open(path, newline="") as f:
        return _html_table([x for x in _csv.reader(f)], **attrs)

def _html_table(items, column_headings=True, row_headings=False, escape_cell_data=False, cell_render_fn=None, **attrs):
    rows = list()

    if column_headings:
        headings = (_html_elem("th", cell) for cell in items[0])
        rows.append(_html_elem("tr", "".join(headings)))
        items = items[1:]

    for row_index, item in enumerate(items):
        columns = list()

        for column_index, cell in enumerate(item):
            if escape_cell_data:
                cell = _xml_escape(cell)

            if cell_render_fn is not None:
                cell = cell_render_fn(row_index, column_index, cell)

            if column_index == 0 and row_headings:
                columns.append(_html_elem("th", cell))
            else:
                columns.append(_html_elem("td", cell))

        rows.append(_html_elem("tr", "".join(columns)))

    tbody = _html_elem("tbody", "".join(rows))

    return _html_elem("table", tbody, **attrs)

def _html_elem(tag, content, **attrs):
    attrs = (_html_attr(name, value) for name, value in attrs.items() if value is not False)
    return f"<{tag} {' '.join(attrs)}>{content or ''}</{tag}>"

def _html_attr(name, value):
    if value is True:
        value = name

    if name in ("class_", "_class"):
        name = "class"

    return f"{name}=\"{_xml_escape(value)}\""

if __name__ == "__main__":
    command = TransomCommand()
    command.main()
