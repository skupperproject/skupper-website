from plano import *

import datetime as _datetime

def path_nav(page):
    links = " <span class=\"path-separator\">&#8250;</span> ".join(list(page.path_nav_links)[1:])
    return f"<nav id=\"-path-nav\"><div>{links}</div></nav>"

def _parse_timestamp(timestamp, format="%Y-%m-%dT%H:%M:%SZ"):
    if timestamp is None:
        return None

    dt = _datetime.datetime.strptime(timestamp, format)
    dt = dt.replace(tzinfo=_datetime.timezone.utc)

    return dt

_latest_release = read_json("data/releases.json")["latest_release"]
_latest_release_date = _parse_timestamp(_latest_release["date"])

skupper_release = _latest_release["version"]
skupper_release_date = f"{_latest_release_date.day} {_latest_release_date.strftime('%B %Y')}"
