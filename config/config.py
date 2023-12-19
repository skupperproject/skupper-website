from plano import *

site.output_dir = "docs"

def path_nav(page):
    links = " <span class=\"path-separator\">&#8250;</span> ".join(list(page.path_nav_links)[1:])
    return f"<nav id=\"-path-nav\"><div>{links}</div></nav>"

_latest_release = read_json("input/data/releases.json")["latest"]
_latest_release_date = parse_timestamp(_latest_release["date"])

skupper_release = _latest_release["version"]
skupper_release_date = format_date(_latest_release_date)
