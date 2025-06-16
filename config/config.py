import os

site_prefix = os.environ.get("SITE_PREFIX", "")

from plano import *

def path_nav(page):
    files = reversed(list(page.ancestors))
    links = [f"<a href=\"{site_prefix}{x.url}\">{x.title}</a>" for x in files]

    return f"<nav class=\"path-nav\">{''.join(links)}</nav>"

def directory_nav(page):
    def sort_fn(x):
        return x.title

    children = sorted(page.children, key=sort_fn)
    links = [f"<li><a href=\"{site_prefix}{x.url}\">{x.title}</a></li>" for x in children]

    return f"<nav class=\"directory-nav\"><ul>{''.join(links)}</ul></nav>"

_latest_release = read_json("input/data/releases.json")["latest"]

latest_release_version = _latest_release["version"]
latest_release_date = format_date(parse_timestamp(_latest_release["date"]))
