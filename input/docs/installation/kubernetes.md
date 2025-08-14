# Installing Skupper on Kubernetes

Before you can create a site on Kubernetes, you must install the
Skupper controller and CRDs.  You can use any of the following
methods:

* Using YAML
* Using Helm
<!-- * Using the Operator -->

After installation, you can create sites using the CLI or YAML:

* [Creating a site using the CLI][cli-site]
* [Creating a site using YAML][yaml-site]

[cli-site]: ../kube-cli/site-configuration.html
[yaml-site]: ../kube-yaml/site-configuration.html

## Using YAML

Prerequisites:

* Cluster administrator access (`cluster-admin`)

To install the latest release, use `kubectl apply` with
<https://skupper.io/install.yaml>:

~~~ shell
kubectl apply -f https://skupper.io/install.yaml
~~~

To install a particular version of Skupper, use the GitHub release URL:

~~~ shell
kubectl apply -f https://github.com/skupperproject/skupper/releases/download/<version>/skupper-cluster-scope.yaml
~~~

Skupper is typically installed at cluster scope.  There is also an
option to install the controller at namespace scope:

~~~ shell
kubectl apply -f https://github.com/skupperproject/skupper/releases/download/<version>/skupper-namespace-scope.yaml
~~~

**NOTE**: If you install the controller at cluster scope, you can
create sites in any namespace.  If you install the controller at
namespace scope, you can create sites only in that namespace.

## Using Helm

Prerequisites:

* Cluster administrator access (`cluster-admin`)
* Helm (see [Installing Helm](https://helm.sh/docs/intro/install/))

To install the latest release, use the `helm install` command:

~~~ shell
helm install skupper oci://quay.io/skupper/helm/skupper
~~~

To install a particular version of Skupper, add the
`--version=<version>` option.

To install the controller at namespace scope, add the `--set
scope=namespace` option.

**NOTE**: If you install the controller at cluster scope, you can
create sites in any namespace.  If you install the controller at
namespace scope, you can create sites only in that namespace.
