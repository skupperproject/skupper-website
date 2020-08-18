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

skupper_cli_release = "0.3.1"
