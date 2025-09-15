---
body_class: object concept
refdog_links:
- title: Site concept
  url: /concepts/site.html
---

# Platform concept

A platform is a system for running application
[workloads](workload.html).  A platform hosts [sites](site.html).
Skupper supports Kubernetes, Docker, Podman, and Linux.  Each site
in a network can run on any supported platform.

Platforms provide _namespaces_ for related workloads and resources.
Skupper uses namespaces to host multiple independent sites on one
instance of a platform.  Each site on a platform can belong to a
distinct application network.

<figure>
  <img src="images/platform-model.svg"/>
  <figcaption>The platform model</figcaption>
</figure>

A platform has zero or more namespaces.  Each namespace is
associated with zero or more workloads.  A namespace may be
associated with a site.

<figure>
  <img src="images/platform-1.svg"/>
  <figcaption>A simple network with sites on two different
  platforms</figcaption>
</figure>

<figure>
  <img src="images/platform-2.svg"/>
  <figcaption>Two different networks spanning two
  platforms</figcaption>
</figure>
