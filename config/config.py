def path_nav(page):
    links = " <span class=\"path-separator\">&#8250;</span> ".join(list(page.path_nav_links)[1:])
    return f"<nav id=\"-path-nav\"><div>{links}</div></nav>"

skupper_release = "1.5.0"
skupper_release_date = "10 November 2023"
