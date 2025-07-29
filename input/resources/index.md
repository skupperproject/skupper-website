---
refdog_links:
  - title: Resource overview
    url: overview.html
  - title: Concept index
    url: /concepts/index.html
  - title: Command index
    url: /commands/index.html
---

# Skupper resources

#### Primary resources

<table class="objects">
<tr><th><a href="{{site.prefix}}/resources/site.html">Site</a></th><td>A site is a place on the network where application workloads are running</td></tr>
<tr><th><a href="{{site.prefix}}/resources/link.html">Link</a></th><td>A link is a channel for communication between sites</td></tr>
<tr><th><a href="{{site.prefix}}/resources/listener.html">Listener</a></th><td>A listener binds a local connection endpoint to connectors in remote sites</td></tr>
<tr><th><a href="{{site.prefix}}/resources/connector.html">Connector</a></th><td>A connector binds a local workload to listeners in remote sites</td></tr>
</table>

#### Sites and site linking

<table class="objects">
<tr><th><a href="{{site.prefix}}/resources/site.html">Site</a></th><td>A site is a place on the network where application workloads are running</td></tr>
<tr><th><a href="{{site.prefix}}/resources/link.html">Link</a></th><td>A link is a channel for communication between sites</td></tr>
<tr><th><a href="{{site.prefix}}/resources/access-grant.html">AccessGrant</a></th><td>Permission to redeem access tokens for links to the local site</td></tr>
<tr><th><a href="{{site.prefix}}/resources/access-token.html">AccessToken</a></th><td>A short-lived credential used to create a link</td></tr>
<tr><th><a href="{{site.prefix}}/resources/router-access.html">RouterAccess</a></th><td>Configuration for secure access to the site router</td></tr>
</table>

#### Service exposure

<table class="objects">
<tr><th><a href="{{site.prefix}}/resources/listener.html">Listener</a></th><td>A listener binds a local connection endpoint to connectors in remote sites</td></tr>
<tr><th><a href="{{site.prefix}}/resources/connector.html">Connector</a></th><td>A connector binds a local workload to listeners in remote sites</td></tr>
<tr><th><a href="{{site.prefix}}/resources/attached-connector.html">AttachedConnector</a></th><td>A connector in a peer namespace</td></tr>
<tr><th><a href="{{site.prefix}}/resources/attached-connector-binding.html">AttachedConnectorBinding</a></th><td>A binding to an attached connector in a peer namespace</td></tr>
</table>
