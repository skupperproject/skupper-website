#!/usr/bin/python3
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

from distutils.core import setup
from distutils.command.build_scripts import build_scripts
from distutils.file_util import copy_file

class BuildScripts(build_scripts):
    def run(self):
        super(BuildScripts, self).run()

        # content = open("bin/plano-self-test.in").read()
        # content.replace(...)
        # write to build/scripts-?.?/plano-self-test

setup(name="plano",
      version="1.0.0-SNAPSHOT",
      url="https://github.com/ssorj/plano",
      author="Justin Ross",
      author_email="justin.ross@gmail.com",
      cmdclass={'build_scripts': BuildScripts},
      py_modules=["plano"],
      package_dir={"": "python"},
      data_files=[("lib/plano/python", ["python/plano_tests.py",
                                        "python/bullseye.py",
                                        "python/bullseye_tests.py"])],
      scripts=["bin/plano", "bin/planosh", "bin/planotest"])
