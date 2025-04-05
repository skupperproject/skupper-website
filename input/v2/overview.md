# Skupper v2 overview

Skupper v2 is a major change and a major improvement over v1.  Here's
why we're doing it and what it means for our users and contributors.

## Why a new major version?

Skupper first became available four years ago.  Since then, we've
learned a lot about what users need from Skupper.  We've also learned
about the pain points for both users and Skupper developers in our
existing design and implementation.  The changes we are making for v2
will result in a version of Skupper that is easier to operate, easier
to extend, and easier to maintain.

## The move to custom resources

Skupper v1 uses a combination of ConfigMaps and resource annotations
as its declarative interface.  Skupper v2 instead uses Kubernetes
[custom resources][custom-resources].

Custom resources have two key advantages.  First, they are subject to
Kubernetes [role-based access control][rbac], so cluster admins can
use standard tooling to control use of Skupper if they choose.
Second, they provide a standard mechanism for reporting resource
status.

Choosing custom resources comes with a trade off. Installing custom
resource definitions (CRDs) requires cluster admin privileges,
something v1 did not require.  This is an advantage for some of our
users, but a disadvantage for others.  We believe that custom
resources are, on balance, the right choice.

[custom-resources]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
[rbac]: https://kubernetes.io/docs/reference/access-authn-authz/rbac/

## A uniform declarative API

V2 has a new, uniform API for site configuration, site linking, and
service exposure.  In v2, all of Skupper's interfaces and platforms
use this common API.

The following are the key API resources in v2:

<style>
.data-table table {
    border-collapse: collapse;
}
.data-table td {
    border: 1px solid gray;
    padding: 0.2em 0.4em;
}
</style>

<div class="data-table">

| | |
| - | - |
| *Sites and networks* | [Site][site-ref], [Link][link-ref] |
| *Service exposure* | [Connector][connector-ref], [Listener][listener-ref] |

</div>

[site-ref]: https://skupperproject.github.io/refdog/resources/site.html
[link-ref]: https://skupperproject.github.io/refdog/resources/link.html
[connector-ref]: https://skupperproject.github.io/refdog/resources/connector.html
[listener-ref]: https://skupperproject.github.io/refdog/resources/listener.html

The new API is designed to enable automation with GitOps and other
tools and to provide a foundation for third-party integrations.

Service exposure in particular sees a change in v2.  In v1, service
exposure is implicit: exposing a service in one site by default
exposed it in all the linked sites.  In v2, service exposure is
instead *explicit*.  A connector binds a local workload to a routing
key.  In another site, a listener with a matching routing key makes it
available for application connections.  Only those sites with a
matching listener can connect to the service.

## A new controller and CLI

The new controller combines the previous service and site controllers
into one that can be deployed at cluster or namespace scope.  The
improved implementation is easier to maintain and understand.

The new controller also addresses a v1 pain point: it allows site
configuration changes without requiring re-creation of the site.
Notably, you can reconfigure your site without losing existing
site-to-site links.

The new CLI closely follows the API.  Indeed, in v2 the CLI is really
just a thin layer on top of the API.  To simplify its use, the CLI
blocks until operations are complete.

## Router improvements

The router in v2 has a new, faster TCP adaptor with improved buffer
handling and reduced threading overhead.  The new TCP adaptor
incorporates lightweight protocol observers for capturing HTTP traffic
metrics.  Together these reduce application latency and router CPU
utilization.

<!-- In v1, HA for routers was  -->
<!-- HA router configuration -->
<!-- - HA routers! -->

## Non-Kube sites

Skupper is not just for Kubernetes.  Skupper sites can run on Docker,
Podman, VMs, or bare metal.  In v2, we've made the support for
non-Kube sites simpler and more uniform.  They use the same YAML
resources as Kube sites.  One codebase implements support for all of
the non-Kube platforms.

<!-- ## The observability components stand apart -->

<!-- Deployment is separate from that of sites. -->

<!-- ## More stuff -->

<!-- Cert reloading -->
<!-- OpenShift site console plugin -->

<!-- - Service exposure model! -->
<!-- - (?) Attached connectors - Tracking pods in namespaces other than that of the site -->

<!-- - Gordon's preso -->
<!-- - My planning docs -->

<!-- - Observability decoupled - flexible deployment -->

<!-- ## Important to know -->

<!-- Gateways go away. -->
<!-- 1.x is _not_ backward compatible with 2. -->
<!-- We are developing tooling to migrate 1.x config to 2.x config. -->
<!-- stateful sets! -->

<!-- Multiple sites per single user -->
<!-- V2 also has a new approach to exposing pods in another namespace. -->
<!-- AttachedConnector and AttachedConnectorAnchor.  A better security -->
<!-- model. -->
