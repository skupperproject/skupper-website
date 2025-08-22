# Installing Skupper on Kubernetes

Before you can create a site on Kubernetes, you must install the
Skupper controller and CRDs.  There are two ways to install them:
using kubectl apply or using the Helm chart.

After installation, you can create sites using the Skupper API or CLI:

- [Creating a site using the API](../operation/api/site-configuration.html)
- [Creating a site using the CLI](../operation/cli/site-configuration.html)

## Using kubectl apply

Prerequisites:

- Cluster administrator access (`cluster-admin`)
- kubectl (see [Installing kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl))

To install the latest release, use `kubectl apply` with the [Skupper
install YAML](https://skupper.io/install.yaml):

~~~ shell
kubectl apply -f https://skupper.io/install.yaml
~~~

To install a particular version of Skupper, use the GitHub release
URL, replacing the `<version>` placeholder with your selection:

~~~ shell
kubectl apply -f https://github.com/skupperproject/skupper/releases/download/<version>/skupper-cluster-scope.yaml
~~~

## Using the Helm chart

Prerequisites:

- Cluster administrator access (`cluster-admin`)
- Helm (see [Installing Helm](https://helm.sh/docs/intro/install/))

To install the latest release, use the `helm install` command:

~~~ shell
helm install skupper oci://quay.io/skupper/helm/skupper
~~~

To install a particular version of Skupper, add the
`--version=<version>` option.

## Installing at namespace scope

The Skupper controller is usually installed at cluster scope.  This
enables you to create sites in any namespace on the cluster.

You also have the option to install the controller at namespace scope.
This is useful in the following cases:

- You do not have permission to install at cluster scope.
- You want multiple versions of the controller running on the cluster.
- You want different configurations of the controller running on the
  cluster.

The Skupper CRDs must still be installed with cluster privileges (a
Kubernetes requirement).

Using YAML:

~~~ shell
kubectl apply -f https://github.com/skupperproject/skupper/releases/download/<version>/skupper-namespace-scope.yaml
~~~

Using Helm:

~~~ shell
helm install skupper oci://quay.io/skupper/helm/skupper --set scope=namespace
~~~

**NOTE**: If you install the controller at cluster scope, you can
create sites in any namespace.  If you install the controller at
namespace scope, you can create sites only in that namespace.
