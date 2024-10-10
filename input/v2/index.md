# Skupper v2

_10 October 2024_

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
standard Kubernetes [role-based access control][rbac], so cluster
admins can use standard tooling to control use of Skupper if they
choose.  Second, they provide a standard mechanism for reporting
resource status.

Choosing custom resources comes with a trade off: installing custom
resource definitions (CRDs) requires cluster admin privileges,
something v1 did not require.  This is an advantage for some of our
users, but a disadvantage for others.  We believe that custom
resources are, on balance, the right choice.

<!-- ref the adr -->

[custom-resources]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
[rbac]: https://kubernetes.io/docs/reference/access-authn-authz/rbac/

## A uniform declarative API

V2 has a new, uniform API for site configuration, site linking, and
service exposure.  In v2, all of Skupper's interfaces and platforms
use this common API.

The following are the core API resources in v2, organized by function:

| | |
| - | - |
| *Site configuration* | [Site][site-ref] |
| *Site linking* |  [Link][link-ref], [AccessGrant][access-grant-ref], [AccessToken][access-token-ref] |
| *Service exposure* | [Connector][connector-ref], [Listener][listener-ref] |

[site-ref]: https://skupperproject.github.io/refdog/resources/site.html
[link-ref]: https://skupperproject.github.io/refdog/resources/link.html
[access-grant-ref]: https://skupperproject.github.io/refdog/resources/accessgrant.html
[access-token-ref]: https://skupperproject.github.io/refdog/resources/accesstoken.html
[connector-ref]: https://skupperproject.github.io/refdog/resources/connector.html
[listener-ref]: https://skupperproject.github.io/refdog/resources/listener.html

The new API is designed to enable automation with GitOps and other
tools and to provide a foundation for third-party integrations.

Service exposure in particular sees a change in v2.  In v1, service
exposure is implicit: exposing a service in one site by default
exposed it in all the linked sites.  In v2, service exposure is
instead explicit.  A connector binds a local workload to a routing
key.  In another site, a listener with a matching routing key makes it
available for application connections.  Only those sites with a
listener can connect to the service.

<!-- V2 also has a new approach to exposing pods in another namespace. -->
<!-- AttachedConnector and AttachedConnectorAnchor.  A better security -->
<!-- model. -->

## A new controller and CLI

The new controller combines the previous service and site controllers
into one that can be deployed at cluster or namespace scope.  The
improved implementation is easier to maintain and understand.

The new controller also addresses a v1 pain point: it allows site
configuration changes without requiring re-creation of the site.
Notably, you can reconfigure your site without losing existing
site-to-site links.

The new CLI closely follows the API, and indeed the CLI is really just
a thin layer on top of the API.  To simplify its use, the CLI blocks
until operations are complete.

<!-- XXX use of CLI to generate YAML -->

<!-- ## Router improvements -->

<!-- XXX -->
<!-- A new, faster TCP adaptor. -->
<!-- Cut through.  Input IO thread directly to output IO thread, without going through a third coordinating thread. -->
<!-- Protocol observers built in to said adaptor. -->
<!-- Lower latency, and lower CPU utilization. -->

<!-- No more dedicated HTTP adaptors.  This simplifies our work and makes the code easier to maintain. -->

<!-- HA router configuration -->

<!-- ## Docker, Podman, and Systemd sites -->

<!-- XXX -->
<!-- Simpler and more uniform. -->
<!-- Multiple sites per single user -->
<!-- Uses the standard resources and API. -->

<!-- Gateways go away. -->

<!-- ## The observability components stand apart -->

<!-- Deployment is separate from that of sites. -->

<!-- ## More stuff -->

<!-- Cert reloading -->
<!-- OpenShift site console plugin -->

<!-- - CRDs! -->
<!-- - Uniform model.  Declarative API.  Everything goes through the CRDs. -->
<!--   - New CLI that follows the new model.  The CLI isn't doing anything clever.  It's just a convenient tool for producing CRs. -->
<!--   - Same model and CRDs across site types (Kubernetes, Docker, Podman, and Systemd sites) -->
<!--   - GitOps -->
<!--   - Integrations -->
<!-- - A uniform model and API across platforms and interfaces. -->

<!-- - Service exposure model! -->
<!-- - (?) Attached connectors - Tracking pods in namespaces other than that of the site -->
<!-- - No more service sync -->

<!-- - A new controller impl. -->
<!-- - Combine site and service controllers. -->
<!-- - Avoiding site recreation! -->

<!-- - HA routers! -->
<!-- - Faster routers! -->

<!-- - Gordon's preso -->
<!-- - My planning docs -->

<!-- - Observability decoupled -->

<!-- ## Important to know -->

<!-- 1.x is _not_ backward compatible with 2. -->
<!-- We are developing tooling to migrate 1.x config to 2.x config. -->

<!-- | 1.x | 2.x | -->
<!-- |-|-| -->
<!-- | Gateways | Docker, Podman, and Systemd sites | -->

## When will v2 be available?

The preview 1 release is available now.  Preview 2 is set for the end
of October, and we are aiming to release 2.0 at the end of November.

Note that things are still changing in the preview releases as we
review interfaces and make improvements.

## Try it out

The best way to start exploring v2 is with our examples.  With preview
1, we have converted our CLI and YAML Hello World examples:

- [Hello World using the CLI](https://github.com/skupperproject/skupper-example-hello-world/tree/v2)
- [Hello World using YAML](https://github.com/skupperproject/skupper-example-yaml/tree/v2)

We would love to get your feedback!

## More resources

- [V2 API reference](https://skupperproject.github.io/refdog/resources/)
- [V2 CLI reference](https://skupperproject.github.io/refdog/commands/)
- [V2 installation YAML](https://skupper.io/v2/install.yaml)
