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
import collections as _collections
import collections.abc as _abc
import csv as _csv
import fnmatch as _fnmatch
import os as _os
import re as _re
import shutil as _shutil
import subprocess as _subprocess
import sys as _sys
import threading as _threading
import types as _types

from . import markdown2 as _markdown
from urllib import parse as _urlparse
from xml.etree.ElementTree import XML as _XML
from xml.sax.saxutils import escape as _xml_escape

_default_body_template = "<body>{{page.content}}</body>"
_default_page_template = "{{page.body}}"
_index_file_names = "index.md", "index.html.in", "index.html"
_markdown_title_regex = _re.compile(r"(#|##)(.+)")
_variable_regex = _re.compile("({{.+?}})")

# _reload_script = "<script src=\"http://localhost:35729/livereload.js\"></script>"

_markdown_converter = _markdown.Markdown(extras={
    "code-friendly": True,
    "footnotes": True,
    "header-ids": True,
    "markdown-in-html": True,
    "tables": True,
})

class Transom:
    def __init__(self, config_dir, input_dir, output_dir, verbose=False, quiet=False):
        self.config_dir = config_dir
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.verbose = verbose
        self.quiet = quiet

        self._config = {
            "site": self,
            "lipsum": _lipsum,
            "html_table": _html_table,
            "html_table_csv": _html_table_csv,
        }

        self._body_template = None
        self._page_template = None

        self._index_files = dict() # parent input dir => _File

        self.ignored_file_patterns = [".git", ".svn", ".#*", "#*"]
        self.ignored_link_patterns = []

    def init(self):
        self._page_template = _load_template(_os.path.join(self.config_dir, "default-page.html"), _default_page_template)
        self._body_template = _load_template(_os.path.join(self.config_dir, "default-body.html"), _default_body_template)

        try:
            exec(_read_file(_os.path.join(self.config_dir, "config.py")), self._config)
        except FileNotFoundError as e:
            self.warn("Config file not found: {}", e)

    def _init_files(self):
        for root, dirs, files in _os.walk(self.input_dir):
            files = {x for x in files if not self._is_ignored_file(x)}
            index_files = {x for x in files if x in _index_file_names}

            if len(index_files) > 1:
                raise Exception(f"Duplicate index files in {root}")

            for name in index_files:
                yield self._init_file(_os.path.join(root, name))

            for name in files - index_files:
                yield self._init_file(_os.path.join(root, name))

    def _is_ignored_file(self, name):
        return any((_fnmatch.fnmatchcase(name, x) for x in self.ignored_file_patterns))

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

        for file_ in self._init_files():
            file_._render(force=force)

        if _os.path.exists(self.output_dir):
            _os.utime(self.output_dir)

        if serve is not None:
            self._serve(serve)

    def _serve(self, port):
        try:
            watcher = _WatcherThread(self)
        except ImportError:
            self.notice("Failed to import pyinotify, so I won't auto-render updated input files")
            self.notice("Try installing the python3-pyinotify package")
        else:
            watcher.start()

        server = _ServerThread(self, port)
        server.run()

        # livereload = None
        #
        # try:
        #     livereload = _subprocess.Popen(f"livereload {self.output_dir} --wait 100", shell=True)
        # except _subprocess.CalledProcessError as e:
        #     self.notice("Failed to start the livereload server, so I won't auto-reload the browser")
        #     self.notice("Use 'npm install -g livereload' to install the server")
        #     self.notice("Subprocess error: {}", e)
        #
        # try:
        #     server = _ServerThread(self, port)
        #     server.run()
        # finally:
        #     if livereload is not None:
        #         livereload.terminate()

    def check_files(self):
        expected_paths = {x._output_path for x in self._init_files()}
        found_paths = set()

        for root, dirs, files in _os.walk(self.output_dir):
            found_paths.update((_os.path.join(root, x) for x in files))

        missing_paths = expected_paths - found_paths
        extra_paths = found_paths - expected_paths

        if missing_paths:
            print("Missing output files:")

            for path in sorted(missing_paths):
                print(f"  {path}")

        if extra_paths:
            print("Extra output files:")

            for path in sorted(extra_paths):
                print(f"  {path}")

        return len(missing_paths), len(extra_paths)

    def check_links(self):
        link_sources = _collections.defaultdict(set) # link => files
        link_targets = set()

        for file_ in self._init_files():
            try:
                file_._collect_link_data(link_sources, link_targets)
            except Exception as e:
                self.warn("Error collecting link data from {}: {}", file_, str(e))

        def not_ignored(link):
            return not any((_fnmatch.fnmatchcase(x) for x in self.ignored_link_patterns))

        links = filter(not_ignored, link_sources.keys())
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
        print("Warning:", message.format(*args))

class _File:
    __slots__ = "site", "_input_path", "_input_mtime", "_output_path", "_output_mtime", "url", "title", "parent"

    def __init__(self, site, input_path, output_path):
        self.site = site

        self._input_path = input_path
        self._input_mtime = _os.path.getmtime(self._input_path)

        self._output_path = output_path
        self._output_mtime = None

        self.url = self._output_path[len(self.site.output_dir):]
        self.title = ""
        self.parent = None

        dir_, name = _os.path.split(self._input_path)

        if name in _index_file_names:
            self.site._index_files[dir_] = self
            dir_ = _os.path.dirname(dir_)

        while dir_ != "":
            try:
                self.parent = self.site._index_files[dir_]
            except:
                dir_ = _os.path.dirname(dir_)
            else:
                break

    def __repr__(self):
        return f"{self.__class__.__name__}({self._input_path}, {self._output_path})"

    def _render(self, force=False):
        self._process_input()

        if self._is_modified() or force:
            self.site.info("Rendering {}", self)
            self._render_output()

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
                    self.site.warn("Duplicate link target in '{}'", normalized_url)

                link_targets.add(normalized_url)

class _TemplatePage(_File):
    __slots__ = "_content", "_attributes", "_page_template", "_body_template"

    def _process_input(self):
        self._content = _read_file(self._input_path)
        self._content, self._attributes = _extract_metadata(self._content)

        self.title = self._attributes.get("title", self.title)

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

        return (f"<a href=\"{x.url}\">{x.title}</a>" for x in reversed(files))

    def path_nav(self, start=None, end=None):
        return f"<nav id=\"-path-nav\">{''.join(list(self.path_nav_links)[start:end])}</nav>"

    def _render_template(self, template):
        local_vars = {"page": self}

        for elem in template:
            if type(elem) is _types.CodeType:
                result = eval(elem, self.site._config, local_vars)

                if type(result) is _types.GeneratorType:
                    yield from result
                else:
                    yield result
            else:
                yield elem

    def render_text(self, text, markdown=False):
        if markdown:
            text = _convert_markdown(text)

        return self._render_template(_parse_template(text))

    def include(self, input_path):
        return self.render_text(_read_file(input_path), markdown=input_path.endswith(".md"))

class _MarkdownPage(_TemplatePage):
    __slots__ = ()

    def _process_input(self):
        super()._process_input()

        if not self.title:
            match = _markdown_title_regex.search(self._content)
            self.title = match.group(2).strip() if match else ""

    def _convert_content(self):
        self._content = _convert_markdown(self._content)

class _WatcherThread(_threading.Thread):
    def __init__(self, site):
        import pyinotify as _pyinotify

        super().__init__(name="watcher", daemon=True)

        self.site = site

        watcher = _pyinotify.WatchManager()
        mask = _pyinotify.IN_CREATE | _pyinotify.IN_MODIFY

        def render(event):
            input_path = _os.path.relpath(event.pathname, _os.getcwd())

            if _os.path.isdir(input_path) or self.site._is_ignored_file(_os.path.basename(input_path)):
                return True

            self.site._init_file(input_path)._render()

            if _os.path.exists(self.site.output_dir):
                _os.utime(self.site.output_dir)

        watcher.add_watch(self.site.input_dir, mask, render, rec=True, auto_add=True)

        self.notifier = _pyinotify.Notifier(watcher)

    def run(self):
        self.site.notice("Watching for input file changes")
        self.notifier.loop()

class _ServerThread(_threading.Thread):
    def __init__(self, site, port):
        import http.server as _http
        import functools as _functools

        super().__init__(name="server", daemon=True)

        self.site = site
        self.port = port

        handler = _functools.partial(_http.SimpleHTTPRequestHandler, directory=self.site.output_dir)
        self.server = _http.ThreadingHTTPServer(("localhost", self.port), handler)

    def run(self):
        self.site.notice("Serving at http://localhost:{}", self.port)
        self.server.serve_forever()

class _Command(object):
    def __init__(self, home=None, name=None, standard_args=True):
        self.home = home
        self.name = name
        self.standard_args = standard_args

        self.parser = _argparse.ArgumentParser()
        self.parser.formatter_class = _argparse.RawDescriptionHelpFormatter

        self.args = None

        if self.name is None:
            self.name = self.parser.prog

        self.id = self.name

        self.quiet = False
        self.verbose = False
        self.init_only = False

    def add_argument(self, *args, **kwargs):
        self.parser.add_argument(*args, **kwargs)

    def add_subparsers(self, *args, **kwargs):
        return self.parser.add_subparsers(*args, **kwargs)

    @property
    def description(self):
        return self.parser.description

    @description.setter
    def description(self, text):
        self.parser.description = text.strip()

    @property
    def epilog(self):
        return self.parser.epilog

    @epilog.setter
    def epilog(self, text):
        self.parser.epilog = text.strip()

    def load_config(self):
        dir_ = _os.path.expanduser("~")
        config_file = _os.path.join(dir_, ".config", self.name, "config.py")
        config = dict()

        if _os.path.exists(config_file):
            entries = _runpy.run_path(config_file, config)
            config.update(entries)

        return config

    def init(self, args=None):
        assert self.args is None

        self.args = self.parser.parse_args(args)

        if self.standard_args:
            self.quiet = self.args.quiet
            self.verbose = self.args.verbose
            self.init_only = self.args.init_only

    def run(self):
        raise NotImplementedError()

    def main(self, args=None):
        self.init(args)

        assert self.args is not None

        if self.init_only:
            return

        try:
            self.run()
        except KeyboardInterrupt: # pragma: nocover
            pass

    def info(self, message, *args):
        if self.verbose:
            self.print_message(message, *args)

    def notice(self, message, *args):
        if not self.quiet:
            self.print_message(message, *args)

    def warn(self, message, *args):
        message = "Warning: {0}".format(message)
        self.print_message(message, *args)

    def error(self, message, *args):
        message = "Error! {0}".format(message)
        self.print_message(message, *args)

    def fail(self, message, *args):
        self.error(message, *args)
        _sys.exit(1)

    def print_message(self, message, *args):
        message = message[0].upper() + message[1:]
        message = message.format(*args)
        message = "{0}: {1}".format(self.id, message)

        _sys.stderr.write("{0}\n".format(message))
        _sys.stderr.flush()

class TransomCommand(_Command):
    def __init__(self, home=None):
        super().__init__(home=home, name="transom", standard_args=False)

        self.description = "Generate static websites from Markdown and Python"

        subparsers = self.add_subparsers(title="subcommands")

        common = _argparse.ArgumentParser()
        common.add_argument("--verbose", action="store_true",
                            help="Print detailed logging to the console")
        common.add_argument("--quiet", action="store_true",
                            help="Print no logging to the console")
        common.add_argument("--init-only", action="store_true",
                            help=_argparse.SUPPRESS)

        common_io = _argparse.ArgumentParser(add_help=False)
        common_io.add_argument("config_dir", metavar="CONFIG-DIR",
                        help="Read config files from CONFIG-DIR")
        common_io.add_argument("input_dir", metavar="INPUT-DIR",
                        help="The base directory for input files")
        common_io.add_argument("output_dir", metavar="OUTPUT-DIR",
                        help="The base directory for output files")

        init = subparsers.add_parser("init", parents=(common,), add_help=False,
                                     help="Prepare an input directory")
        init.set_defaults(command_fn=self.init_command)
        init.add_argument("config_dir", metavar="CONFIG-DIR",
                          help="Read config files from CONFIG-DIR")
        init.add_argument("input_dir", metavar="INPUT-DIR",
                          help="Place default input files in INPUT-DIR")

        render = subparsers.add_parser("render", parents=(common, common_io), add_help=False,
                                       help="Generate output files")
        render.set_defaults(command_fn=self.render_command)
        render.add_argument("--force", action="store_true",
                            help="Render all input files, including unmodified ones")
        render.add_argument("--serve", type=int, metavar="PORT",
                            help="Serve the site and rerender when input files change")

        check_links = subparsers.add_parser("check-links", parents=(common, common_io), add_help=False,
                                            help="Check for broken links")
        check_links.set_defaults(command_fn=self.check_links_command)

        check_files = subparsers.add_parser("check-files", parents=(common, common_io), add_help=False,
                                            help="Check for missing or extra files")
        check_files.set_defaults(command_fn=self.check_files_command)

    def init(self, args=None):
        super().init(args)

        if "command_fn" not in self.args:
            self.fail("Missing subcommand")

        if self.args.command_fn != self.init_command:
            self.lib = Transom(self.args.config_dir, self.args.input_dir, self.args.output_dir,
                               verbose=self.args.verbose, quiet=self.args.quiet)
            self.lib.init()

            if self.args.init_only:
                self.parser.exit()

    def run(self):
        self.args.command_fn()

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
        self.lib.render(force=self.args.force, serve=self.args.serve)

    def check_links_command(self):
        errors = self.lib.check_links()

        if errors == 0:
            self.notice("PASSED")
        else:
            self.fail("FAILED")

    def check_files_command(self):
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
    with open(path, "r") as f:
        return f.read()

def _copy_file(from_path, to_path):
    _make_dir(_os.path.dirname(to_path))
    _shutil.copyfile(from_path, to_path)

def _extract_metadata(text):
    attrs = dict()

    if text.startswith("---\n"):
        end = text.index("---\n", 4)
        lines = text[4:end].strip().split("\n")

        for line in lines:
            key, value = (x.strip() for x in line.split(":", 1))
            attrs[key] = None if value.lower() in ("none", "null") else value

        text = text[end + 4:]

    return text, attrs

def _load_template(path, default_text):
    if path is None or not _os.path.isfile(path):
        return list(_parse_template(default_text))

    return list(_parse_template(_read_file(path)))

def _parse_template(text):
    for token in _variable_regex.split(text):
        if token.startswith("{{") and token.endswith("}}"):
            yield compile(token[2:-2], "<string>", "eval")
        else:
            yield token

def _convert_markdown(text):
    lines = (x for x in text.splitlines(keepends=True) if not x.startswith(";;"))
    return _markdown_converter.convert("".join(lines))

_lipsum_words = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "vestibulum", "enim", "urna",
    "ornare", "pellentesque", "felis", "eget", "maximus", "lacinia", "lorem", "nulla", "auctor", "massa", "vitae",
    "ultricies", "varius", "curabitur", "consectetur", "lacus", "sapien", "a", "lacinia", "urna", "tempus", "quis",
    "vestibulum", "vitae", "augue", "non", "augue", "lobortis", "semper", "nullam", "fringilla", "odio", "quis",
    "ligula", "consequat", "condimentum", "integer", "tempus", "sem",
]

def _lipsum(count=50, end="."):
    return (" ".join((_lipsum_words[i % len(_lipsum_words)] for i in range(count))) + end).capitalize()

def _html_table_csv(path, **attrs):
    with open(path, newline="") as f:
        return _html_table(_csv.reader(f), **attrs)

def _html_table_cell(column_index, value):
    return _html_elem("td", str(value if value is not None else ""))

def _html_table(data, headings=None, cell_fn=_html_table_cell, **attrs):
    return _html_elem("table", _html_elem("tbody", _html_table_rows(data, headings, cell_fn)), **attrs)

def _html_table_rows(data, headings, cell_fn):
    if headings:
        yield _html_elem("tr", (_html_elem("th", x) for x in headings))

    for row in data:
        yield _html_elem("tr", (cell_fn(i, x) for i, x in enumerate(row)))

def _html_elem(tag, content, **attrs):
    if isinstance(content, _abc.Iterable) and not isinstance(content, str):
        content = "".join(content)

    return f"<{tag}{''.join(_html_attrs(attrs))}>{content or ''}</{tag}>"

def _html_attrs(attrs):
    for name, value in attrs.items():
        name = "class" if name in ("class_", "_class") else name
        value = name if value is True else value

        if value is not False:
            yield f" {name}=\"{_xml_escape(value)}\""

if __name__ == "__main__":
    command = TransomCommand()
    command.main()
