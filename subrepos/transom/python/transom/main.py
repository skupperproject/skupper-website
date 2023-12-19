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
import http.server as _http
import math as _math
import mistune as _mistune
import multiprocessing as _multiprocessing
import os as _os
import re as _re
import shutil as _shutil
import subprocess as _subprocess
import sys as _sys
import threading as _threading
import types as _types

from html import escape as _escape
from html.parser import HTMLParser as _HTMLParser
from urllib import parse as _urlparse

_default_page_template = "{{page.body}}"
_default_body_template = "{{page.content}}"
_index_file_names = "index.md", "index.html.in", "index.html"
_markdown_title_regex = _re.compile(r"(#|##)(.+)")
_variable_regex = _re.compile(r"({{.+?}})")

# An improvised solution for trouble on Mac OS
_once = False
if not _once:
    _multiprocessing.set_start_method("fork")
    _once = True

class Transom:
    def __init__(self, project_dir, verbose=False, quiet=False):
        self.project_dir = _os.path.normpath(project_dir)
        self.config_dir = _os.path.normpath(_os.path.join(self.project_dir, "config"))
        self.input_dir = _os.path.normpath(_os.path.join(self.project_dir, "input"))
        self.output_dir = _os.path.normpath(_os.path.join(self.project_dir, "output"))

        self.verbose = verbose
        self.quiet = quiet

        self.ignored_file_patterns = [".git", ".svn", ".#*", "#*"]
        self.ignored_link_patterns = []

        self._config = {
            "site": self,
            "lipsum": _lipsum,
            "plural": _plural,
            "html_table": _html_table,
            "html_table_csv": _html_table_csv,
        }

        self._body_template = None
        self._page_template = None

        self._files = list()
        self._index_files = dict() # parent input dir => _File

    def init(self):
        self._page_template = _load_template(_os.path.join(self.config_dir, "page.html"), _default_page_template)
        self._body_template = _load_template(_os.path.join(self.config_dir, "body.html"), _default_body_template)

        self._ignored_file_regex = "({})".format("|".join([_fnmatch.translate(x) for x in self.ignored_file_patterns]))
        self._ignored_file_regex = _re.compile(self._ignored_file_regex)

        try:
            exec(_read_file(_os.path.join(self.config_dir, "config.py")), self._config)
        except FileNotFoundError as e:
            self.warn("Config file not found: {}", e)

    def _init_files(self):
        self._files.clear()
        self._index_files.clear()

        for root, dirs, names in _os.walk(self.input_dir):
            files = {x for x in names if not self._ignored_file_regex.match(x)}
            index_files = {x for x in names if x in _index_file_names}

            if len(index_files) > 1:
                raise Exception(f"Duplicate index files in {root}")

            for name in index_files:
                self._files.append(self._init_file(_os.path.join(root, name)))

            for name in files - index_files:
                self._files.append(self._init_file(_os.path.join(root, name)))

    def _init_file(self, input_path):
        output_path = _os.path.join(self.output_dir, input_path[len(self.input_dir) + 1:])

        if input_path.endswith(".md"):
            return _MarkdownPage(self, input_path, f"{output_path[:-3]}.html")
        elif input_path.endswith(".html.in"):
            return _TemplatePage(self, input_path, output_path[:-3])
        else:
            return _File(self, input_path, output_path)

    def render(self, force=False):
        self.notice("Rendering files from '{}' to '{}'", self.input_dir, self.output_dir)

        self._init_files()

        self.notice("Found {:,} input {}", len(self._files), _plural("file", len(self._files)))

        for file_ in self._index_files.values():
            file_._process_input()

        proc_count = _os.cpu_count()
        procs = list()
        batch_size = _math.ceil(len(self._files) / proc_count)

        for i in range(proc_count):
            start = i * batch_size
            end = start + batch_size

            procs.append(_RenderProcess(self._files[start:end], force))

        for proc in procs:
            proc.start()

        for proc in procs:
            proc.join()

        if _os.path.exists(self.output_dir):
            _os.utime(self.output_dir)

        rendered_count = sum([x.rendered_count.value for x in procs])
        unmodified_count = len(self._files) - rendered_count
        unmodified_note = ""

        if unmodified_count > 0:
            unmodified_note = " ({:,} unchanged)".format(unmodified_count)

        self.notice("Rendered {:,} output {}{}", rendered_count, _plural("file", rendered_count), unmodified_note)

    def serve(self, port=8080):
        watcher = None
        livereload = None

        try:
            watcher = _WatcherThread(self)
        except ImportError: # pragma: nocover
            self.notice("Failed to import pyinotify, so I won't auto-render updated input files")
            self.notice("Try installing the Python inotify package")
            self.notice("On Fedora, use 'dnf install python-inotify'")
        else:
            watcher.start()

        try:
            livereload = _subprocess.Popen(f"livereload {self.output_dir} --wait 100", shell=True)
        except _subprocess.CalledProcessError as e: # pragma: nocover
            self.notice("Failed to start the livereload server, so I won't auto-reload the browser")
            self.notice("Use 'npm install -g livereload' to install the server")
            self.notice("Subprocess error: {}", e)

        try:
            server = _ServerThread(self, port)
            server.run()
        finally:
            if livereload is not None:
                livereload.terminate()

            if watcher is not None:
                watcher.stop()

    def check_files(self):
        self._init_files()

        expected_paths = {x._output_path for x in self._files}
        found_paths = set()

        for root, dirs, names in _os.walk(self.output_dir):
            found_paths.update((_os.path.join(root, x) for x in names))

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
        self._init_files()

        link_sources = _collections.defaultdict(set) # link => files
        link_targets = set()

        for file_ in self._files:
            file_._collect_link_data(link_sources, link_targets)

        def not_ignored(link):
            return not any((_fnmatch.fnmatchcase(link, x) for x in self.ignored_link_patterns))

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
    __slots__ = "site", "_input_path", "_input_mtime", "_output_path", "_output_mtime", "_rendered", \
        "url", "title", "parent"

    def __init__(self, site, input_path, output_path):
        self.site = site

        self._input_path = input_path
        self._input_mtime = _os.path.getmtime(self._input_path)

        self._output_path = output_path
        self._output_mtime = None

        self._rendered = False

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
            except KeyError:
                dir_ = _os.path.dirname(dir_)
            else:
                break

    def __repr__(self):
        return f"{self.__class__.__name__}({self._input_path}, {self._output_path})"

    def _process_input(self): # pragma: nocover
        pass

    def _render(self, force=False):
        if not force and not self._is_modified():
            return

        self.site.info("Rendering {}", self)

        self._render_content()

        self._rendered = True

    def _is_modified(self):
        if self._output_mtime is None:
            try:
                self._output_mtime = _os.path.getmtime(self._output_path)
            except FileNotFoundError:
                return True

        return self._input_mtime > self._output_mtime

    def _render_content(self):
        _copy_file(self._input_path, self._output_path)

    def _collect_link_data(self, link_sources, link_targets):
        link_targets.add(self.url)

        if not self.url.endswith(".html"):
            return

        parser = _LinkParser(self, link_sources, link_targets)
        parser.feed(_read_file(self._output_path))

class _LinkParser(_HTMLParser):
    def __init__(self, file_, link_sources, link_targets):
        super().__init__()

        self.file = file_
        self.link_sources = link_sources
        self.link_targets = link_targets

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        for name in ("href", "src", "action"):
            try:
                url = attrs[name]
            except KeyError:
                continue

            split_url = _urlparse.urlsplit(url)

            if split_url.scheme or split_url.netloc:
                continue

            normalized_url = _urlparse.urljoin(self.file.url, _urlparse.urlunsplit(split_url))

            self.link_sources[normalized_url].add(self.file)

        if "id" in attrs:
            normalized_url = _urlparse.urljoin(self.file.url, f"#{attrs['id']}")

            if normalized_url in self.link_targets:
                self.file.site.warn("Duplicate link target in '{}'", normalized_url)

            self.link_targets.add(normalized_url)

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

    def _render_content(self):
        if not hasattr(self, "_content"):
            self._process_input()

        _os.makedirs(_os.path.dirname(self._output_path), exist_ok=True)

        with open(self._output_path, "w") as f:
            for elem in self._render_template(self._page_template):
                f.write(elem)

    @property
    def root_class(self):
        return self._attributes.get("root_class", "")

    @property
    def extra_headers(self):
        return self._attributes.get("extra_headers", "")

    @property
    def body(self):
        return self._render_template(self._body_template)

    @property
    def content(self):
        parsed = _parse_template(self._content)
        rendered = "".join(self._render_template(parsed))

        return self._convert_content(rendered)

    def _convert_content(self, content):
        return content

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

    def _convert_content(self, content):
        return _convert_markdown(content)

class _RenderProcess(_multiprocessing.Process):
    def __init__(self, files, force):
        super().__init__()

        self.files = files
        self.force = force
        self.rendered_count = _multiprocessing.Value('L', 0)

    def run(self):
        rendered_count = 0

        for file_ in self.files:
            file_._render(force=self.force)

            if file_._rendered:
                rendered_count += 1

        self.rendered_count.value = rendered_count

class _WatcherThread:
    def __init__(self, site):
        import pyinotify as _pyinotify

        self.site = site

        watcher = _pyinotify.WatchManager()
        mask = _pyinotify.IN_CREATE | _pyinotify.IN_MODIFY

        def render_file(event):
            input_path = _os.path.relpath(event.pathname, _os.getcwd())
            _, base_name = _os.path.split(input_path)

            if _os.path.isdir(input_path) or self.site._ignored_file_regex.match(base_name):
                return True

            file_ = self.site._init_file(input_path)
            file_._render()

            if _os.path.exists(self.site.output_dir):
                _os.utime(self.site.output_dir)

        def render_site(event):
            self.site.init()
            self.site.render(force=True)

        watcher.add_watch(self.site.input_dir, mask, render_file, rec=True, auto_add=True)
        watcher.add_watch(self.site.config_dir, mask, render_site, rec=True, auto_add=True)

        self.notifier = _pyinotify.ThreadedNotifier(watcher)

    def start(self):
        self.site.notice("Watching for input file changes")
        self.notifier.start()

    def stop(self):
        self.notifier.stop()

class _ServerThread(_threading.Thread):
    def __init__(self, site, port):
        super().__init__(name="server", daemon=True)

        self.site = site
        self.port = port
        self.server = _Server(site, port)

    def run(self):
        self.site.notice("Serving at http://localhost:{}", self.port)
        self.server.serve_forever()

class _Server(_http.ThreadingHTTPServer):
    def __init__(self, site, port):
        super().__init__(("localhost", port), _ServerRequestHandler)

        self.site = site

class _ServerRequestHandler(_http.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server, directory=None):
        super().__init__(request, client_address, server, directory=server.site.output_dir)

    def do_GET(self):
        path = _os.path.join(self.directory, self.path[1:])

        if _os.path.isdir(path):
            path = _os.path.join(path, "index.html")

        if path.endswith(".html"):
            with open(path) as file_:
                content = file_.read()
                content = content.replace("</head>", "<script src=\"http://localhost:35729/livereload.js\"></script></head>")

                self.send_response(_http.HTTPStatus.OK)
                self.send_header("Content-type", "text/html; charset=UTF-8")
                self.send_header("Content-length", len(content))
                self.end_headers()

                self.wfile.write(content.encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/STOP":
            self.server.shutdown()

        self.send_response(_http.HTTPStatus.OK)
        self.end_headers()

class TransomCommand:
    def __init__(self, home=None):
        self.home = home
        self.name = "transom"

        self.parser = _argparse.ArgumentParser()
        self.parser.description = "Generate static websites from Markdown and Python"
        self.parser.formatter_class = _argparse.RawDescriptionHelpFormatter

        self.args = None
        self.quiet = False
        self.verbose = False

        subparsers = self.parser.add_subparsers(title="subcommands")

        common = _argparse.ArgumentParser()
        common.add_argument("--verbose", action="store_true",
                            help="Print detailed logging to the console")
        common.add_argument("--quiet", action="store_true",
                            help="Print no logging to the console")
        common.add_argument("--init-only", action="store_true",
                            help=_argparse.SUPPRESS)
        common.add_argument("project_dir", metavar="PROJECT-DIR", nargs="?", default=".",
                            help="The project root directory (default: current directory)")

        init = subparsers.add_parser("init", parents=[common], add_help=False,
                                     help="Prepare an input directory")
        init.set_defaults(command_fn=self.init_command)
        init.add_argument("--profile", metavar="PROFILE", choices=("website", "webapp"), default="website",
                          help="Select starter files for different scenarios (default: website)")
        init.add_argument("--github", action="store_true",
                          help="Add extra files for use in a GitHub repo")

        render = subparsers.add_parser("render", parents=[common], add_help=False,
                                       help="Generate output files")
        render.set_defaults(command_fn=self.render_command)
        render.add_argument("--force", action="store_true",
                            help="Render all input files, including unmodified ones")

        render = subparsers.add_parser("serve", parents=[common], add_help=False,
                                       help="Generate output files and serve the site on a local port")
        render.set_defaults(command_fn=self.serve_command)
        render.add_argument("--port", type=int, metavar="PORT", default=8080,
                            help="Listen on PORT (default 8080)")
        render.add_argument("--force", action="store_true",
                            help="Render all input files, including unmodified ones")

        check_links = subparsers.add_parser("check-links", parents=[common], add_help=False,
                                            help="Check for broken links")
        check_links.set_defaults(command_fn=self.check_links_command)

        check_files = subparsers.add_parser("check-files", parents=[common], add_help=False,
                                            help="Check for missing or extra files")
        check_files.set_defaults(command_fn=self.check_files_command)

    def init(self, args=None):
        self.args = self.parser.parse_args(args)

        if "command_fn" not in self.args:
            self.parser.print_usage()
            _sys.exit(1)

        self.quiet = self.args.quiet
        self.verbose = self.args.verbose

        if self.args.command_fn != self.init_command:
            self.lib = Transom(self.args.project_dir, verbose=self.verbose, quiet=self.quiet)
            self.lib.init()

    def main(self, args=None):
        self.init(args)

        assert self.args is not None

        if self.args.init_only:
            return

        try:
            self.args.command_fn()
        except KeyboardInterrupt: # pragma: nocover
            pass

    def notice(self, message, *args):
        if not self.quiet:
            self.print_message(message, *args)

    def warn(self, message, *args):
        message = "Warning: {}".format(message)
        self.print_message(message, *args)

    def error(self, message, *args):
        message = "Error! {}".format(message)
        self.print_message(message, *args)

    def fail(self, message, *args):
        self.error(message, *args)
        _sys.exit(1)

    def print_message(self, message, *args):
        message = message[0].upper() + message[1:]
        message = message.format(*args)
        message = "{}: {}".format(self.name, message)

        _sys.stderr.write("{}\n".format(message))
        _sys.stderr.flush()

    def init_command(self):
        if self.home is None:
            self.fail("I can't find the default input files")

        def copy(from_path, to_path):
            if _os.path.exists(to_path):
                self.notice("Skipping '{}'. It already exists.", to_path)
                return

            _copy_path(from_path, to_path)

            self.notice("Creating '{}'", to_path)

        profile_dir = _os.path.join(self.home, "profiles", self.args.profile)
        project_dir = self.args.project_dir

        assert _os.path.exists(profile_dir), profile_dir

        for name in _os.listdir(_os.path.join(profile_dir, "config")):
            copy(_os.path.join(profile_dir, "config", name),
                 _os.path.join(project_dir, "config", name))

        for name in _os.listdir(_os.path.join(profile_dir, "input")):
            copy(_os.path.join(profile_dir, "input", name),
                 _os.path.join(project_dir, "input", name))

        if self.args.github:
            python_dir = _os.path.join(self.home, "python")

            copy(_os.path.join(profile_dir, ".plano.py"), _os.path.join(project_dir, ".plano.py"))
            copy(_os.path.join(profile_dir, ".nojekyll"), _os.path.join(project_dir, ".nojekyll"))
            copy(_os.path.join(python_dir, "mistune"), _os.path.join(project_dir, "python", "mistune"))
            copy(_os.path.join(python_dir, "transom"), _os.path.join(project_dir, "python", "transom"))

            with open(_os.path.join(project_dir, "config", "config.py"), "a") as f:
                f.write("\nsite.output_dir = \"docs\"\n")

    def render_command(self):
        self.lib.render(force=self.args.force)

    def serve_command(self):
        self.lib.render(force=self.args.force)
        self.lib.serve(port=self.args.port)

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

def _read_file(path):
    with open(path, "r") as f:
        return f.read()

def _copy_file(from_path, to_path):
    try:
        _shutil.copyfile(from_path, to_path)
    except FileNotFoundError:
        _os.makedirs(_os.path.dirname(to_path), exist_ok=True)
        _shutil.copyfile(from_path, to_path)

def _copy_dir(from_dir, to_dir):
    for name in _os.listdir(from_dir):
        if name == "__pycache__":
            continue

        from_path = _os.path.join(from_dir, name)
        to_path = _os.path.join(to_dir, name)

        _copy_path(from_path, to_path)

def _copy_path(from_path, to_path):
    if _os.path.isdir(from_path):
        _copy_dir(from_path, to_path)
    else:
        _copy_file(from_path, to_path)

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

_heading_id_regex_1 = _re.compile(r"[^a-zA-Z0-9_ ]+")
_heading_id_regex_2 = _re.compile(r"[_ ]")

class _HtmlRenderer(_mistune.renderers.html.HTMLRenderer):
    def heading(self, text, level, **attrs):
        id = _heading_id_regex_1.sub("", text)
        id = _heading_id_regex_2.sub("-", id)
        id = id.lower()

        return f"<h{level} id=\"{id}\">{text}</h{level}>\n"

class _MarkdownLocal(_threading.local):
    def __init__(self):
        self.value = _mistune.create_markdown(renderer=_HtmlRenderer(escape=False), plugins=["table"])

_markdown_local = _MarkdownLocal()

def _convert_markdown(text):
    lines = (x for x in text.splitlines(keepends=True) if not x.startswith(";;"))
    return _markdown_local.value("".join(lines))

_lipsum_words = [
    "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "vestibulum", "enim", "urna",
    "ornare", "pellentesque", "felis", "eget", "maximus", "lacinia", "lorem", "nulla", "auctor", "massa", "vitae",
    "ultricies", "varius", "curabitur", "consectetur", "lacus", "sapien", "a", "lacinia", "urna", "tempus", "quis",
    "vestibulum", "vitae", "augue", "non", "augue", "lobortis", "semper", "nullam", "fringilla", "odio", "quis",
    "ligula", "consequat", "condimentum", "integer", "tempus", "sem",
]

def _lipsum(count=50, end="."):
    return (" ".join((_lipsum_words[i % len(_lipsum_words)] for i in range(count))) + end).capitalize()

def _plural(noun, count=0, plural=None):
    if noun in (None, ""):
        return ""

    if count == 1:
        return noun

    if plural is None:
        if noun.endswith("s"):
            plural = "{}ses".format(noun)
        else:
            plural = "{}s".format(noun)

    return plural

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
            yield f" {name}=\"{_escape(value, quote=True)}\""

if __name__ == "__main__": # pragma: nocover
    command = TransomCommand()
    command.main()
