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

.NOTPARALLEL:

export PYTHONPATH := python

.PHONY: render
render: site_url := "file:${CURDIR}/output"
render: clean
	python3 -m transom render --quiet input output
	python3 -m transom render --quiet --site-url "https://www.ssorj.net/amq-io" input docs
	@echo "See the output at ${site_url}/index.html"

.PHONY: watch
watch:
	python3 -m transom render --quiet --watch input output

.PHONY: clean
clean:
	rm -rf output
	rm -rf python/__pycache__

.PHONY: update-%
update-%:
	curl -sfo python/$*.py "https://raw.githubusercontent.com/ssorj/$*/master/python/$*.py"
