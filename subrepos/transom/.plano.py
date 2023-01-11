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

from bullseye import *

project.name = "transom"
project.data_dirs = ["files", "test-site"]
project.test_modules = ["transom.tests"]

@command(parent=build)
def build(*args, **kwargs):
    parent(*args, **kwargs)

    with project_env():
        run("transom --help", quiet=True, stash=True)

        with working_dir(quiet=True):
            touch("config/config.py", quiet=True)
            run("transom render --init-only config input output", quiet=True)

@command(parent=clean)
def clean(*args, **kwargs):
    parent(*args, **kwargs)

    remove("test-site/output")
    remove("qpid-site/output")
    remove("htmlcov")
    remove(".coverage")
