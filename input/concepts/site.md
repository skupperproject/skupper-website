---
body_class: object concept
refdog_links:
- title: Site resource
  url: /resources/site.html
- title: Site command
  url: /commands/site/index.html
- title: Link concept
  url: /concepts/link.html
- title: Network concept
  url: /concepts/network.html
- title: Platform concept
  url: /concepts/platform.html
- title: Workload concept
  url: /concepts/workload.html
---

# Site concept

A site is a place on the [network](network.html) where application
[workloads](workload.html) are running.  Sites are joined by
[links](link.html).

<figure>
  <img src="images/site-model.svg"/>
  <figcaption>The site model</figcaption>
</figure>

A site is associated with one platform and one network.  Each site
has zero or more workloads and zero or more links.

Sites operate on multiple [platforms](platform.html).  One site
corresponds to one namespace in a platform instance.  Sites can be
added to a network and removed from a network dynamically.

Each site has a Skupper router which is responsible for
communicating with the local workloads and forwarding traffic to
routers in remote sites.

<figure>
  <img src="images/site-1.svg"/>
  <figcaption>A site with three workloads</figcaption>
</figure>

<figure>
  <img src="images/site-2.svg"/>
  <figcaption>Two sites linked to form a network</figcaption>
</figure>

<figure>
  <img src="images/site-3.svg"/>
  <figcaption>A network with sites on three different
  platforms</figcaption>
</figure>
