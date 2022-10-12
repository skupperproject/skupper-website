
def path_nav(page):
    links = " <span class=\"path-separator\">&#8250;</span> ".join(list(page.path_nav_links)[1:])
    return f"<nav id=\"-path-nav\"><div>{links}</div></nav>"

def circle(diameter, color="#000"):
    position = .2 * diameter
    cx = .5 * diameter
    cy = .5 * diameter
    radius = .4 * diameter
    stroke = .1 * diameter

    return \
        f"<svg height=\"{diameter}\" width=\"{diameter}\" style=\"position: relative; top: {position}; margin: 0;\">" \
        f"  <circle cx=\"{cx}\" cy=\"{cy}\" r=\"{radius}\" stroke=\"{color}\" stroke-width=\"{stroke}\" fill=\"none\"/>" \
        "</svg>"

skupper_release = "1.1.1"
skupper_release_date = "7 October 2022"
