# Define custom variables and functions for use in {{replaceables}}
#
# Use `site_url` to build fully qualified paths

lipsum_5 = "Lorem ipsum dolor sit amet"

lipsum_10 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur
interdum.
"""
lipsum_15 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur
interdum orci eget metus dapibus dictum.
"""

lipsum_25 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur
interdum orci eget metus dapibus, dictum mollis est porta. Nullam eget
vestibulum ex. Proin lobortis urna.
"""

lipsum_50 = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum
enim urna, ornare pellentesque felis eget, maximus lacinia
lorem. Nulla auctor massa vitae ultricies varius. Curabitur
consectetur lacus sapien, a lacinia urna tempus quis. Vestibulum vitae
augue non augue lobortis semper. Nullam fringilla odio quis ligula
consequat condimentum. Integer tempus sem.
"""

def circle(diameter, color="#000"):
    position = .15 * diameter
    cx = .5 * diameter
    cy = .5 * diameter
    radius = .4 * diameter
    stroke = .1 * diameter
    
    return \
        f"<svg height=\"{diameter}\" width=\"{diameter}\" style=\"position: relative; top: {position}; margin: 0;\">" \
        f"  <circle cx=\"{cx}\" cy=\"{cy}\" r=\"{radius}\" stroke=\"{color}\" stroke-width=\"{stroke}\" fill=\"none\"/>" \
        "</svg>"
