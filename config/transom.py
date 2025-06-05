from plano import *

site.prefix = "/skupper-website"

_latest_release = read_json("input/data/releases.json")["latest"]

latest_release_version = _latest_release["version"]
latest_release_date = format_date(parse_timestamp(_latest_release["date"]))

# XXX
skupper_version = latest_release_version
skupper_cli_version = skupper_version

skupper_version_v1 = "1.9.2"

skupper_site_url = "https://www.ssorj.net/skupper-website"

def get_edit_url(page):
    return f"https://github.com/ssorj/skupper-website/edit/main/{page.input_path}"

skupper_api_ref = f"{{site.prefix}}/docs/reference/resources"
