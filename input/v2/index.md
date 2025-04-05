# Skupper v2

Skupper v2 is the next generation of Skupper.

- [V2 overview](overview.html)
<!-- - [Everything that's new in v2](whats-new.html) -->

## Installation

### Installing Skupper on Kubernetes

To install Skupper v2 on Kubernetes, use `kubectl apply` with the
[installation YAML](https://skupper.io/v2/install.yaml).  It contains
the v2 CRDs and controller.

~~~ shell
kubectl apply -f https://skupper.io/v2/install.yaml
~~~

Additional Kubernetes installation methods are available in the
[release
artifacts](https://github.com/skupperproject/skupper/releases/tag/2.0.0).

### Installing the CLI

~~~ shell
curl https://skupper.io/v2/install.sh | sh
~~~

[V2 CLI install script](https://skupper.io/v2/install.sh)

## Examples

- [Hello World using the CLI](https://github.com/skupperproject/skupper-example-hello-world/tree/v2)
- [Hello World using YAML](https://github.com/skupperproject/skupper-example-yaml/tree/v2)
- [Hello World using Podman](https://github.com/skupperproject/skupper-example-podman/tree/v2)
- [Patient Portal](https://github.com/skupperproject/skupper-example-patient-portal/tree/v2)

The v2 examples are available on the "v2" branch of the Skupper example repos.

## Documentation

- [V2 documentation](https://skupperproject.github.io/skupper-docs/)
- [V2 concepts](https://skupperproject.github.io/refdog/concepts/)
- [V2 API reference](https://skupperproject.github.io/refdog/resources/)
- [V2 CLI reference](https://skupperproject.github.io/refdog/commands/)

## Releases

- [2.0.0](https://github.com/skupperproject/skupper/releases/tag/2.0.0) - 7 March 2025

## Upgrades

V2 is not backward compatible with v1.  We are developing tooling to
convert v1 configuration to v2 custom resources.  Those upgrading from
v1 to v2 will have a small period of downtime while the v1 components
shut down and the v2 components start up.
