---
body_class: object concept
refdog_links:
- title: Service exposure
  url: /topics/service-exposure.html
- title: Listener resource
  url: /resources/listener.html
- title: Listener command
  url: /commands/listener/index.html
- title: Connector concept
  url: /concepts/connector.html
- title: Routing key concept
  url: /concepts/routing-key.html
---

# Listener concept

A listener binds a local connection endpoint to
[connectors](connector.html) in remote [sites](site.html).
Listeners and connectors are matched using [routing
keys](routing-key.html).

<figure>
  <img src="images/listener-model.svg"/>
  <figcaption>The listener model</figcaption>
</figure>

<figure>
  <img src="images/routing-key-model.svg"/>
  <figcaption>The routing key model</figcaption>
</figure>

A site has zero or more listeners.  Each listener has an associated
connection endpoint and routing key.  The connection endpoint
exposes a host and port for accepting connections from local
clients.  The routing key is a string identifier that binds the
listener to connectors in remote sites.

On Kubernetes, a listener is implemented as a
[Service][kube-service].  On Docker, Podman, and Linux, it is a
listening socket bound to a local network interface.

[kube-service]: https://kubernetes.io/docs/concepts/services-networking/service/

<figure>
  <img src="images/service-1.svg"/>
  <figcaption>Client connections forwarded to servers</figcaption>
</figure>

Skupper routers forward client connections across the network from
listeners to connectors with matching routing keys.  The connectors
then forward the client connections to the workload servers.

<figure>
  <img src="images/listener-1.svg"/>
  <figcaption>A database service with listeners in two
  sites</figcaption>
</figure>
