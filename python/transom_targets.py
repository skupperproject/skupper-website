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

@target(help="Render site output")
def render(force=False):
    with project_env():
        args = ["render", "--force", site.config_dir, site.input_dir, site.output_dir]

        if force:
            args.append("--force")

        TransomCommand().main(args)

# https://stackoverflow.com/questions/22475849/node-js-what-is-enospc-error-and-how-to-solve
# $ echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
@target(help="Render and serve the site")
def serve(port=8080, force=False):
    with project_env():
        args = ["render", "--serve", str(port), site.config_dir, site.input_dir, site.output_dir]

        if force:
            args.append("--force")

        TransomCommand().main(args)

@target(help="Check for broken links")
def check_links():
    render()

    with project_env():
        TransomCommand().main(["check-links", site.config_dir, site.input_dir, site.output_dir])

@target(help="Check for missing or extra files")
def check_files():
    render()

    with project_env():
        TransomCommand().main(["check-files", site.config_dir, site.input_dir, site.output_dir])

@target
def clean():
    remove("output")

    for path in find(".", "__pycache__"):
        remove(path)

    for path in find(".", "*.pyc"):
        remove(path)

class project_env(working_env):
    def __init__(self):
        super(project_env, self).__init__(PYTHONPATH="python")
