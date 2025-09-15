---
title: Securing a service network using Skupper policies
---
# Securing a service network using Skupper policies

By default, Skupper includes many security features, including using mutual TLS for all service network communication between sites.
You can add extra security features by installing the Skupper policy CRD.
By default, applying a Skupper policy CRD to a cluster prevents all service network communication to and from that cluster.
You specify granular Skupper policies CRs to permit only the service network communication you require.

**📌 NOTE**\
A Skupper policy is distinct from the Kubernetes network policy, that is the `network-policy` option, which restricts access to Skupper services to the current namespace as described in [Using the Skupper CLI](../cli/index.html).

Each site in a service network runs a Skupper router and has a private, dedicated certificate authority (CA).
Communication between sites is secured with mutual TLS, so the service network is isolated from external access, preventing security risks such as lateral attacks, malware infestations, and data exfiltration.
A set of Skupper policies adds another layer at a cluster level to help a cluster administrator control access to a service network.

This guide assumes that you understand the following Skupper concepts:

* **site**\
A namespace in which Skupper is installed.
* **token**\
A token is required to establish a link between two sites.
* **service network**\
After exposing services using Skupper, you have created a service network.

## About Skupper policies

After a cluster administrator installs a Skupper policy Custom Resource Definition (CRD), the cluster administrator needs to configure one or more policies to allow _developers_ create and use services on the service network.

**📌 NOTE**\
In this guide, _developers_ refers to users of a cluster who have access to a namespace, but do not have administrator privileges.

A cluster administrator configures one or more of following items using custom resources (CRs) to enable communication:

* **Allow incoming links**\
Use `allowIncomingLinks` to enable developers create tokens and configure incoming links.
* **Allow outgoing links to specific hosts**\
Use `allowedOutgoingLinksHostnames` to specify hosts that developers can create links to.
* **Allow services**\
Use `allowedServices` to specify which services developers can create or use on the service network.
* **Allow resources to be exposed**\
Use `allowedExposedResources` to specify which resources a developer can expose on the service network.

**📌 NOTE**\
A cluster administrator can apply each policy CR setting to one or more namespaces.

For example, the following policy CR fully allows all Skupper capabilities on all namespaces, except for:

* only allows outgoing links to any domain ending in `.example.com`.
* only allows 'deployment/nginx' resources to be exposed on the service network.

```yaml
apiVersion: skupper.io/v1alpha1
kind: SkupperClusterPolicy
metadata:
  name: cluster-policy-sample-01
spec:
  namespaces:
    - "*"
  allowIncomingLinks: true
  allowedExposedResources:
    - "deployment/nginx"
  allowedOutgoingLinksHostnames: [".*\.example.com$"]
  allowedServices:
    - "*"
```

<dl><dt><strong>📌 NOTE</strong></dt><dd>

You can apply many policy CRs, and if there are conflicts in the items allowed, the most permissive policy is applied.
For example, if you apply an additional policy CR with the line `allowedOutgoingLinksHostnames: []`, which does not list any hostnames, outgoing links to `*.example.com` are still permitted because that is permitted in the original CR.
</dd></dl>

* **`namespaces`**\
One or more patterns to specify the namespaces that this policy applies to.
Note that you can use [Label selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) to match the namespaces.
* **`allowIncomingLinks`**\
Specify `true` to allow other sites create links to the specified namespaces.
* **`allowedOutgoingLinksHostnames`**\
Specify one or more patterns to determine which hosts you can create links to from the specified namespaces.
* **`allowedServices`**\
Specify one or more patterns to determine the permitted names of services allowed on the service network from the specified namespaces.
* **`allowedExposedResources`**\
Specify one or more permitted names of resources allowed on the service network from the specified namespaces.
Note that patterns are not supported.

<dl><dt><strong>💡 TIP</strong></dt><dd>

Use regular expressions to create pattern matches, for example:

* `.*\.com$` matches any string ending in `.com`.
A double backslash is required to avoid issues in YAML.
* `^abc$` matches the string `abc`.

</dd></dl>

If you create another Skupper policy CR that allows outgoing links for a specific namespace, a user can create a link from that namespace to join a service network. That is, the logic for multiple policy CRs is `OR`.
An operation is permitted if any single policy CR permits the operation.

## Installing the Skupper policy CRD

Installing the Skupper policy CRD enables a cluster administrator to enforce policies for service networks.

**📌 NOTE**\
If there are existing sites on the cluster, see [Installing a Skupper policy CRD on a cluster with existing sites](#installing-a-skupper-policy-crd-on-a-cluster-with-existing-sites) to avoid service network disruption.

* Access to a cluster using a `cluster-admin` account
* The Skupper operator is installed

1. Log in to the cluster using a `cluster-admin` account.
2. Download the CRD:

   ```bash
   $ wget https://raw.githubusercontent.com/skupperproject/skupper/{skupper-version}/api/types/crds/skupper_cluster_policy_crd.yaml
   ```
3. Apply the CRD:

   ```bash
   $ kubectl apply -f skupper_cluster_policy_crd.yaml

   customresourcedefinition.apiextensions.k8s.io/skupperclusterpolicies.skupper.io created
   clusterrole.rbac.authorization.k8s.io/skupper-service-controller created
   ```
4. To verify that a Skupper policy is active, use the `skupper status` command and check that the output includes the following line:

   ```bash
   Skupper is enabled for namespace "<namespace>" in interior mode (with policies).
   ```

## Installing a Skupper policy CRD on a cluster with existing sites

If the cluster already hosts Skupper sites, note the following before installing the CRD:

* All existing connections are closed.
You must apply a policy CR to reopen connections.
* All existing service network services and exposed resources are removed.
You must create those resources again.

To avoid disruption:

1. Plan the CRD deployment for an appropriate time.
2. Search your cluster for sites:

   ```bash
   $ kubectl get pods --all-namespaces --selector=app=skupper
   ```
3. Document each service and resource exposed on the service network.
4. Install the CRD as described in [Installing the Skupper policy CRD](#installing-the-skupper-policy-crd).
This step closes connections and removes all service network services and exposed resources.
5. If Skupper sites that were not created by `cluster-admin` exist in the cluster, you must grant permissions to read Skupper policies to avoid that site being blocked from the service network.

   For each site namespace:

   ```bash
   $ kubectl create clusterrolebinding skupper-service-controller-<namespace> --clusterrole=skupper-service-controller --serviceaccount=<namespace>:skupper-service-controller
   ```

   where `<namespace>` is the site namespace.
6. Create Skupper policy CRs as described in [Creating Skupper policy CRs](#creating-skupper-policy-crs)
7. Recreate any services and exposed resources as required.

## Creating Skupper policy CRs

Skupper Policy CRs allow a cluster administrator to control communication across the service network from a cluster.

* Access to a cluster using a `cluster-admin` account.
* The Skupper policy CRD is installed on the cluster.

**📌 NOTE**\
Typically, you create a Skupper policy CR that combines many elements from the steps below. See [About Skupper policies](#about-skupper-policies) for an example CR.

1. [Implement a policy to allow incoming links](#implement-a-policy-to-allow-incoming-links)
2. [Implement a policy to allow outgoing links to specific hosts](#implement-a-policy-to-allow-outgoing-links-to-specific-hosts)
3. [Implement a policy to allow specific services](#implement-a-policy-to-allow-specific-services)
4. [Implement a policy to allow specific resources](#implement-a-policy-to-allow-specific-resources)

### Implement a policy to allow incoming links

Use `allowIncomingLinks` to enable developers create tokens and configure incoming links.

1. Determine which namespaces you want to apply this policy to.
2. Create a CR with `allowIncomingLinks` set to `true` or `false`.
3. Create and apply the CR.

For example, the following CR allows incoming links for all namespaces:
```yaml
apiVersion: skupper.io/v1alpha1
kind: SkupperClusterPolicy
metadata:
  name: allowincominglinks
spec:
  namespaces:
    - "*"
  allowIncomingLinks: true
```

### Implement a policy to allow outgoing links to specific hosts

Use `allowedOutgoingLinksHostnames` to specify hosts that developers can create links to.
You cannot create a `allowedOutgoingLinksHostnames` policy to disallow a specific host that was previously allowed.

1. Determine which namespaces you want to apply this policy to.
2. Create a CR with `allowedOutgoingLinksHostnames` set to a pattern of allowed hosts.
3. Create and apply the CR.

For example, the following CR allows links to all subdomains of `example.com` for all namespaces:
```yaml
apiVersion: skupper.io/v1alpha1
kind: SkupperClusterPolicy
metadata:
  name: allowedoutgoinglinkshostnames
spec:
  namespaces:
    - "*"
  allowedOutgoingLinksHostnames: ['.*\.example\.com']
```

### Implement a policy to allow specific services

Use `allowedServices` to specify which services a developer can create or use on the service network.
You cannot create a `allowedServices` policy to disallow a specific service that was previously allowed.

1. Determine which namespaces you want to apply this policy to.
2. Create a CR with `allowedServices` set to specify the services allowed on the service network.
3. Create and apply the CR.

For example, the following CR allows users to expose and consume services with the prefix `backend-` for all namespaces:
```yaml
apiVersion: skupper.io/v1alpha1
kind: SkupperClusterPolicy
metadata:
  name: allowedservices
spec:
  namespaces:
    - "*"
  allowedServices: ['^backend-']
```

**📌 NOTE**\
When exposing services, you can use the `--address <name>` parameter of the `skupper` CLI to name services to match your policy.

### Implement a policy to allow specific resources

Use `allowedExposedResources` to specify which resources a developer can expose on the service network.
You cannot create a `allowedExposedResources` policy to disallow a specific resource that was previously allowed.

1. Determine which namespaces you want to apply this policy to.
2. Create a CR with `allowedExposedResources` set to specify resources that a developer can expose on the service network.
3. Create and apply the CR.

For example, the following CR allows you to expose an `nginx` deployment for all namespaces:
```yaml
apiVersion: skupper.io/v1alpha1
kind: SkupperClusterPolicy
metadata:
  name: allowedexposedresources
spec:
  namespaces:
    - "*"
  allowedExposedResources: ['deployment/nginx']
```

**📌 NOTE**\
For `allowedExposedResources`, each entry must conform to the `type/name` syntax.
