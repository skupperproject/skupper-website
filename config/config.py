from plano import *

site.output_dir = "docs"

def path_nav(page):
    files = reversed(list(page.ancestors)[:-1])
    links = [f"<a href=\"{x.url}\">{x.title}</a>" for x in files]
    links = " <span class=\"path-separator\">&#8250;</span> ".join(links)

    return f"<nav id=\"-path-nav\"><div>{links}</div></nav>"

_latest_release = read_json("input/data/releases.json")["latest"]

latest_release_version = _latest_release["version"]
latest_release_date = format_date(parse_timestamp(_latest_release["date"]))
