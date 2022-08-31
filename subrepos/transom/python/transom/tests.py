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

import csv as _csv

from .commands import configure_file
from .main import _lipsum, _html_table, _html_table_csv
from plano import *
from plano.commands import PlanoCommand
from xml.etree.ElementTree import XML as _XML

test_site_dir = get_absolute_path("test-site")
result_file = "output/result.json"

class test_site(working_dir):
    def __enter__(self):
        dir = super(test_site, self).__enter__()
        copy(test_site_dir, ".", inside=False, symlinks=False)
        return dir

@test
def transom_options():
    run("transom --help")

@test
def transom_init():
    run("transom init --help")
    run("transom init --init-only --verbose config input")

    with working_dir():
        run("transom init config input")

        check_dir("config")
        check_dir("input")
        check_file("config/config.py")
        check_file("input/index.md")
        check_file("input/main.css")
        check_file("input/main.js")

        run("transom init config input") # Re-init

@test
def transom_render():
    run("transom render --help")
    run("transom render --init-only --quiet config input output")

    with test_site():
        run("transom render config input output")

        check_dir("output")
        check_file("output/index.html")
        check_file("output/test-1.html")
        check_file("output/test-2.html")
        check_file("output/main.css")
        check_file("output/main.js")

        result = read("output/index.html")
        assert "<title>Doorjamb</title>" in result, result
        assert "<h1 id=\"doorjamb\">Doorjamb</h1>" in result, result

        run("transom render config input output")
        run("transom render --force config input output")

@test
def transom_check_links():
    run("transom check-links --help")
    run("transom check-links --init-only --verbose config input output")

    with test_site():
        run("transom render config input output")
        run("transom check-links config input output")

        append(join("a", "index.md"), "[Not there](not-there.html)")

        run("transom check-links config input output")

@test
def transom_check_files():
    run("transom check-files --help")
    run("transom check-files --init-only --quiet config input output")

    with test_site():
        run("transom render config input output")

        remove(join("input", "test-page-1.md")) # An extra output file
        remove(join("output", "test-page-2.html")) # A missing output file

        run("transom check-files config input output")

@test
def plano_render():
    with test_site():
        PlanoCommand().main(["render"])

        result = read_json(result_file)
        assert result["rendered"], result

# @test
# def plano_serve():
#     with test_site():
#         PlanoCommand().main(["render", "--serve"])

#         result = read_json(result_file)
#         assert result["served"], result

@test
def plano_check_links():
    with test_site():
        PlanoCommand().main(["check-links"])

        result = read_json(result_file)
        assert result["links_checked"], result

@test
def plano_check_files():
    with test_site():
        PlanoCommand().main(["check-files"])

        result = read_json(result_file)
        assert result["files_checked"], result

@test
def plano_clean():
    with test_site():
        PlanoCommand().main(["clean"])

@test
def plano_modules():
    with test_site():
        with expect_system_exit():
            PlanoCommand().main(["modules", "--remote", "--recursive"])

@test
def configure_file_function():
    with working_dir():
        input_file = write("zeta-file", "X@replace-me@X")
        output_file = configure_file(input_file, "zeta-file", {"replace-me": "Y"})
        output = read(output_file)
        assert output == "XYX", output

@test
def lipsum_function():
    result = _lipsum(0, end="")
    assert result == "", result

    result = _lipsum(1)
    assert result == "Lorem."

    result = _lipsum(1000)
    assert result

@test
def html_table_functions():
    data = (
        (1, 2, 3),
        ("a", "b", "c"),
        (None, "", 0),
    )

    _XML(_html_table(data))
    _XML(_html_table(data, headings=("A", "B", "C")))

    with working_dir():
        with open("test.csv", "w", newline="") as f:
            writer = _csv.writer(f)
            writer.writerows(data)

        _XML(_html_table_csv("test.csv"))
