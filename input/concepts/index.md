---
refdog_links:
  - title: Concept overview
    url: overview.html
  - title: Resource index
    url: /resources/index.html
  - title: Command index
    url: /commands/index.html
---

# Skupper concepts

#### Sites

<table class="objects">
<tr><th><a href="{{site.prefix}}/concepts/site.html">Site</a></th><td>A site is a place on the network where application workloads are running</td></tr>
<tr><th><a href="{{site.prefix}}/concepts/workload.html">Workload</a></th><td>A workload is a set of processes running on a platform</td></tr>
<tr><th><a href="{{site.prefix}}/concepts/platform.html">Platform</a></th><td>A platform is a system for running application workloads</td></tr>
</table>

#### Networks

<table class="objects">
<tr><th><a href="{{site.prefix}}/concepts/network.html">Network</a></th><td>A network is a set of sites joined by links</td></tr>
<tr><th><a href="{{site.prefix}}/concepts/link.html">Link</a></th><td>A link is a channel for communication between sites</td></tr>
<tr><th><a href="{{site.prefix}}/concepts/access-token.html">Access token</a></th><td>An access token is a short-lived credential used to create a link</td></tr>
</table>

#### Services

<table class="objects">
<tr><th><a href="{{site.prefix}}/concepts/listener.html">Listener</a></th><td>A listener binds a local connection endpoint to connectors in remote sites</td></tr>
<tr><th><a href="{{site.prefix}}/concepts/connector.html">Connector</a></th><td>A connector binds a local workload to listeners in remote sites</td></tr>
<tr><th><a href="{{site.prefix}}/concepts/routing-key.html">Routing key</a></th><td>A routing key is a string identifier for matching listeners and connectors</td></tr>
</table>

#### Applications

<table class="objects">
<tr><th><a href="{{site.prefix}}/concepts/application.html">Application</a></th><td>An application is a set of components that work together</td></tr>
<tr><th><a href="{{site.prefix}}/concepts/component.html">Component</a></th><td>A component is a logical part of an application</td></tr>
</table>
