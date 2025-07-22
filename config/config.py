site.prefix = "/skupper-website"

from plano import *

_latest_release = read_json("input/data/releases.json")["latest"]

latest_release_version = _latest_release["version"]
latest_release_date = format_date(parse_timestamp(_latest_release["date"]))
