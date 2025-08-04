# Installing Skupper on Kubernetes

Before you can create a site on Kubernetes, you must install the Skupper controller.
You can install the controller using the following methods:

* Directly using YAML
* Helm charts
* Operator

After installing the Skupper controller, you can create sites using the CLI or YAML:

* [Creating a site using the CLI][cli-site]
* [Creating a site using YAML][yaml-site]

[cli-site]: ../kube-cli/site-configuration.html
[yaml-site]: ../kube-yaml/site-configuration.html

**NOTE**: If you install the controller scoped to cluster, you can create sites in any namespace.
If you scope the controller to a namespace, you can only create sites in that namespace.

## Installing Skupper using YAML

**Prerequisites**

* cluster-admin access to cluster

**Procedure**

Install a cluster-scoped controller using the following commands:

```bash
kubectl apply -f https://github.com/skupperproject/skupper/releases/download/{{skupper_version}}/skupper-cluster-scope.yaml
```

Install a namespace-scoped controller using the following commands:

```bash
kubectl apply -f https://github.com/skupperproject/skupper/releases/download/{{skupper_version}}/skupper-namespace-scope.yaml
```

## Installing Skupper using Helm

**Prerequisites**

* cluster-admin access to cluster
* helm (See https://helm.sh/docs/intro/install/)

**Procedure**

Run the following command to install a cluster-scoped controller:

```
helm install skupper oci://quay.io/skupper/helm/skupper --version {{skupper_version}}
```
To install a namespace-scoped controller, add the `--set scope=namespace` option.

<!--
## Installing the Skupper controller using the Skupper Operator

**Prerequisites**

* cluster-admin access to cluster
* OpenShift

**Procedure**

1. Navigate to the **OperatorHub** in the **Administrator** view.
2. Search for `Skupper`, provided by `Skupper project`.
3. Select **stable-2.0** from **Channel**.
4. Select the latest **Version**.
5. Click **Install**.
-->
