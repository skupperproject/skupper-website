---
body_class: object concept
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
- title: Site concept
  url: /concepts/site.html
- title: Connector concept
  url: /concepts/connector.html
---

# Workload concept

A workload is a set of processes running on a
[platform](platform.html).  A _process_ is a pod, container, or
system process.  Workloads in a [site](site.html) are exposed as
services on the [network](network.html) using
[connectors](connector.html).

<figure>
  <img src="images/workload-model.svg"/>
  <figcaption>The workload model</figcaption>
</figure>

A platform has zero or more workloads.  A site also has zero or more
workloads.  Each workload has zero or more processes and zero or
more [connectors](connector.html).

A workload implements one part of an application by providing a
network interface (for example, an API) that other parts of the
application use.  A workload can be both a client and a server.

On Kubernetes, a workload is a Deployment, StatefulSet, or
DaemonSet.  On Docker or Podman, a workload is a set of containers.
On Linux, a workload is a set of system processes.

<figure>
  <img src="images/workload-1.svg"/>
  <figcaption>A workload with three processes</figcaption>
</figure>

<figure>
  <img src="images/workload-2.svg"/>
  <figcaption>A workload exposed as a service using a
  connector</figcaption>
</figure>
