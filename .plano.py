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

from transom.planocommands import *

@command
def generate_docs(output_dir="input", owner="skupperproject", branch="main"):
    """
    Generate docs from the skupper-docs repo and config/docs-playbook.yaml.in
    """

    check_program("antora")

    docs_dir = get_absolute_path(f"{output_dir}/docs")
    playbook_in = get_absolute_path("config/docs-playbook.yaml.in")

    with working_dir():
        content = read(playbook_in)
        content = content.replace("@branch@", branch)
        content = content.replace("@owner@", owner)
        playbook = write("docs-playbook.yaml", content)

        run(f"antora --fetch {playbook}")

        for path in find("build", "*.html"):
            move(path, f"{path}.in")

        copy("build/skupper/latest/console", docs_dir)
        copy("build/skupper/latest/overview", docs_dir)
        copy("build/skupper/latest/cli/", docs_dir)
        copy("build/skupper/latest/cli-reference", docs_dir)
        copy("build/skupper/latest/cli-podman", docs_dir)
        copy("build/skupper/latest/declarative", docs_dir)
        copy("build/skupper/latest/troubleshooting", docs_dir)
        copy("build/skupper/latest/policy", docs_dir)
        copy("build/skupper/latest/operator", docs_dir)
        copy("build/skupper/latest/_images", docs_dir)

@command
def generate_examples(output_dir="input"):
    """
    Generate the example index using data from GitHub and config/examples.yaml
    """

    output_file = f"{output_dir}/examples/index.md"
    examples_data = read_yaml("config/examples.yaml")
    github_data = http_get_json("https://api.github.com/orgs/skupperproject/repos?per_page=100")
    repos = dict()

    for repo_data in github_data:
        repos[repo_data["name"]] = repo_data

    out = list()

    for category in examples_data["categories"]:
        category_title = category["title"]
        category_id = category_title.lower().replace(" ", "-")
        category_description = category.get("description")

        out.append(f"<h2 id=\"{category_id}\">{category_title}</h2>")
        out.append("")

        if category_description is not None:
            out.append(f"<p>{category_description}</p>")
            out.append("")

        out.append("<div class=\"examples\">")
        out.append("")

        for example_data in category["examples"]:
            name = example_data["name"]
            title = example_data["title"]

            try:
                repo_data = repos[name]
            except:
                description = example_data.get("description").strip()
                url = example_data.get("url")
            else:
                description = example_data.get("description", repo_data["description"])
                url = example_data.get("url", repo_data["html_url"])

            out.append("<div>")
            out.append(f"<h3><a href=\"{url}\">{title}</a></h3>")
            out.append(f"<p>{description}</p>")
            out.append("<nav class=\"inline-links\">")
            out.append(f"<a href=\"{url}\"><span class=\"fab fa-github fa-lg\"></span> Example</a>")

            if "video_url" in example_data:
                video_url = example_data["video_url"]
                out.append(f"<a href=\"{video_url}\"><span class=\"fab fa-youtube fa-lg\"></span> Video</a>")

            out.append("</nav>")
            out.append("</div>")

        out.append("</div>")
        out.append("")

    examples = "\n".join(out)
    markdown = read("config/examples.md.in").replace("@examples@", examples)

    write(output_file, markdown)

@command
def generate_releases(output_dir="input"):
    """
    Generate the release index using data from GitHub
    """

    output_file = f"{output_dir}/releases/index.md"
    data_file = f"{output_dir}/data/releases.json"

    _update_release_data(output_dir)

    releases = read_json(data_file)
    latest_version = releases["latest"]["version"]
    out = list()

    def sort(release):
        return parse_timestamp(release["date"])

    for release in sorted(releases.values(), key=sort, reverse=True):
        version = release["version"]
        url = release["github_url"]
        date = parse_timestamp(release["date"])

        if version == latest_version:
            continue

        out.append(f"* [{version}]({url}) - {format_date(date)}")

    releases = "\n".join(out)
    markdown = read("config/releases.md.in").replace("@releases@", releases)

    write(output_file, markdown)

def _update_release_data(output_dir):
    output_file = f"{output_dir}/data/releases.json"
    install_script_data_file = f"{output_dir}/data/install.json"

    releases = http_get_json("https://api.github.com/repos/skupperproject/skupper/releases?per_page=100")
    latest_release = http_get_json("https://api.github.com/repos/skupperproject/skupper/releases/latest")

    latest_release_tag = latest_release["tag_name"]

    write_json(install_script_data_file, {"version": latest_release_tag})

    data = dict()

    data["latest"] = {
        "version": latest_release_tag,
        "github_url": f"https://github.com/skupperproject/skupper/releases/tag/{latest_release_tag}",
        "date": latest_release["published_at"],
    }

    for release in releases:
        if release["prerelease"] or release["draft"]:
            continue

        release_tag = release["tag_name"]

        data[release_tag] = {
            "version": release_tag,
            "github_url": f"https://github.com/skupperproject/skupper/releases/tag/{release_tag}",
            "date": release["published_at"],
        }

    write_json(output_file, data)

@command
def generate_scripts(output_dir="input"):
    """
    Generate the install scripts
    """

    install_script = http_get("https://raw.githubusercontent.com/skupperproject/skupper-install-script/main/install.sh")
    uninstall_script = http_get("https://raw.githubusercontent.com/skupperproject/skupper-install-script/main/uninstall.sh")

    write(f"{output_dir}/install.sh", install_script)
    write(f"{output_dir}/uninstall.sh", uninstall_script)

@command
def test():
    render()
    check_links()
    check_files()

    with temp_dir() as temp:
        with working_env(HOME=temp):
            run("cat docs/install.sh | sh", shell=True)
            run("cat docs/uninstall.sh | sh", shell=True)

        generate_examples(output_dir=temp)
        generate_releases(output_dir=temp)
        generate_scripts(output_dir=temp)
