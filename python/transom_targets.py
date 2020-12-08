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

from plano import *
from transom import TransomCommand

import_targets("bullseye", "modules")

class _Site:
    def __init__(self):
        self.config_dir = "config"
        self.input_dir = "input"
        self.output_dir = "output"

site = _Site()

_force_arg = Argument("force", help="Render all input files, including unmodified ones")
_verbose_arg = Argument("verbose", help="Print detailed logging to the console")

@target(help="Render site output", default=True,
        args=(_force_arg, _verbose_arg))
def render(force=False, verbose=False):
    with project_env():
        args = ["render", "--force", site.config_dir, site.input_dir, site.output_dir]

        if force:
            args.append("--force")

        if verbose:
            args.append("--verbose")

        TransomCommand().main(args)

# https://stackoverflow.com/questions/22475849/node-js-what-is-enospc-error-and-how-to-solve
# $ echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
@target(help="Serve the site and rerender when input files change",
        args=(Argument("port", help="Serve on PORT"), _force_arg, _verbose_arg))
def serve(port=8080, force=False, verbose=False):
    with project_env():
        args = ["render", "--serve", str(port), site.config_dir, site.input_dir, site.output_dir]

        if force:
            args.append("--force")

        if verbose:
            args.append("--verbose")

        TransomCommand().main(args)

@target(help="Check for broken links", args=(_verbose_arg,))
def check_links(verbose=False):
    run_target("render")

    args = ["check-links", site.config_dir, site.input_dir, site.output_dir]

    if verbose:
        args.append("--verbose")

    with project_env():
        TransomCommand().main(args)

@target(help="Check for missing or extra files", args=(_verbose_arg,))
def check_files(verbose=False):
    run_target("render")

    args = ["check-files", site.config_dir, site.input_dir, site.output_dir]

    if verbose:
        args.append("--verbose")

    with project_env():
        TransomCommand().main(args)

@target
def clean():
    for path in find(".", "__pycache__"):
        remove(path)

    for path in find(".", "*.pyc"):
        remove(path)

@target(help="Update Git submodules",
        args=[Argument("remote", help="Get remote commits"),
              Argument("recursive", help="Update modules recursively")])
def modules(remote=False, recursive=False):
    check_program("git")

    command = ["git", "submodule", "update", "--init"]

    if remote:
        command.append("--remote")

    if recursive:
        command.append("--recursive")

    run(command)

class project_env(working_env):
    def __init__(self):
        super(project_env, self).__init__(PYTHONPATH="python")
