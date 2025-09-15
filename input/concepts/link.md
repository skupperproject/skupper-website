---
body_class: object concept
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Link resource
  url: /resources/link.html
- title: Link command
  url: /commands/link/index.html
- title: Network concept
  url: /concepts/network.html
- title: Site concept
  url: /concepts/site.html
- title: Access token concept
  url: /concepts/access-token.html
---

# Link concept

A link is a channel for communication between [sites](site.html).
Links carry application connections and requests.  A set of linked
sites constitutes a [network](network.html).

To create a link to a remote site, the remote site must enable
_link access_.  Link access provides an external access point for
accepting links.

<figure>
  <img src="images/link-model-1.svg"/>
  <figcaption>The link model</figcaption>
</figure>

<figure>
  <img src="images/link-model-2.svg"/>
  <figcaption>The link access model</figcaption>
</figure>

A site has zero or more links.  Each link has a host, port, and TLS
credentials for making a mutual TLS connection to a remote site.  In
addition, a site has zero or more link accesses.  Usually only one
is needed per site.  Each link access has a host, port, and TLS
credentials for exposing a TLS endpoint that accepts connections
from remote sites.

Application connections and requests flow across links in both
directions.  A linked site can communicate with any other site in
the network, even if it is not linked directly.  Links can be added
and removed dynamically.

You can use [access tokens](access-token.html) to securely exchange
the connection details required to create a link.

<figure>
  <img src="images/link-1.svg"/>
  <figcaption>A link joining two sites to create a simple network</figcaption>
</figure>

<figure>
  <img src="images/link-2.svg"/>
  <figcaption>A site with two links, to two remote sites</figcaption>
</figure>

<figure>
  <img src="images/link-3.svg"/>
  <figcaption>A larger network with links to a central hub site</figcaption>
</figure>
