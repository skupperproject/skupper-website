---
title: Configuring Skupper sites using YAML
---
# Configuring Skupper sites using YAML

Using YAML files to configure Skupper allows you to use source control to track and manage Skupper network changes.

## Installing Skupper using YAML

Installing Skupper using YAML provides a declarative method to install Skupper.
You can store your YAML files in source control to track and manage Skupper network changes.

* Access to a Kubernetes cluster

1. Log into your cluster.
If you are deploying Skupper to be available for all namespaces, verify you have `cluster-admin` privileges.
2. Deploy the site controller:
   * To install Skupper into the current namespace deploy the site controller using the following YAML:

     ```bash
     kubectl apply -f deploy-watch-current-ns.yaml
     ```
     where the contents of `deploy-watch-current-ns.yaml` is specified in the [YAML for watching current namespace](#yaml-for-watching-current-namespace) appendix.
   * To install Skupper for all namespaces:

     1. Create a namespace named `skupper-site-controller`.
     2. Deploy the site controller using the following YAML:

        ```bash
        kubectl apply -f deploy-watch-all-ns.yaml
        ```
        where the contents of `deploy-watch-all-ns.yaml` is specified in the [YAML for watching all namespaces](#yaml-for-watching-all-namespaces) appendix.
3. Verify the installation.

   ```bash
   $ kubectl get pods
   NAME                                       READY   STATUS    RESTARTS   AGE
   skupper-site-controller-84694bdbb5-n8slb   1/1     Running   0          75s
   ```

## Creating a Skupper site using YAML

Using YAML files to create Skupper sites allows you to use source control to track and manage Skupper network changes.

* Skupper is installed in the cluster or namespace you want to target.
* You are logged into the cluster.

1. Create a YAML file to define the site, for example, `my-site.yaml`:

   ```bash
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: skupper-site
   data:
     name: my-site
     console: "true"
     console-user: "admin"
     console-password: "changeme"
     flow-collector: "true"
   ```
   The YAML creates a site with a console and you can create tokens from this site.

   To create a site that has no ingress:

   ```
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: skupper-site
   data:
     name: my-site
     ingress: "none"
   ```

2. Apply the YAML file to your cluster:

   ```bash
   kubectl apply -f ~/my-site.yml
   ```

See the [Site ConfigMap YAML reference](#site-configmap-yaml-reference) section for more reference.

## Linking sites using YAML

While it is not possible to declaratively link sites, you can create a token using YAML.
Only use this procedure to create links if the Skupper CLI is not available in your environment.

* Skupper is installed on the clusters you want to link.
* You are logged into the cluster.

1. Log into the cluster you want to link to and change context to the namespace where Skupper is installed.
This site must have `ingress` enabled.
2. Create a YAML file named `token-request.yml` to request a token:

   ```
   apiVersion: v1
   kind: Secret
   metadata:
     labels:
       skupper.io/type: connection-token-request
     annotations:
       skupper.io/cost: "2"
     name: secret-name
   ```
3. Apply the YAML to the namespace to create a secret.

   ```bash
   $ kubectl apply -f token-request.yml
   ```
4. Create the token YAML from the secret.

   ```bash
   $ kubectl get secret -o yaml secret-name | yq 'del(.metadata.namespace)' > ~/token.yaml
   ```
5. Log into the cluster you want to link from and change context to the namespace where Skupper is installed.
6. Apply the token YAML.

   ```bash
   $ kubectl apply -f token.yml
   ```
7. Verify the link, allowing some time for the process to complete.

   ```bash
   $ skupper link status --wait 60
   ```

Skupper recommends using the CLI to create links.

A future release of Skupper will provide an alternative declarative method to create links.

## Configuring services using annotations

After creating and linking sites, you can use Kubernetes annotations to control which services are available on the service network.

### Exposing simple services on a service network using annotations

This section provides an alternative to the `skupper expose` command, allowing you to annotate existing resources to expose simple services on the service network.

* A site with a service you want to expose

1. Log into the namespace in your cluster that is configured as a site.
2. Create a deployment, some pods, or a service in one of your sites, for example:

   ```bash
   $ kubectl create deployment hello-world-backend --image quay.io/skupper/hello-world-backend
   ```

   This step is not Skupper-specific, that is, this process is unchanged from standard processes for your cluster.
3. Annotate the kubernetes resource to create a service that can communicate on the service network, for example:

   ```bash
   $ kubectl annotate deployment backend "skupper.io/address=backend" "skupper.io/port=8080" "skupper.io/proxy=tcp"
   ```

   The annotations include:

   * `skupper.io/proxy` - the protocol you want to use, `tcp`, `http` or `http2`.
   This is the only annotation that is required.
   For example, if you annotate a simple deployment named `backend` with `skupper.io/proxy=tcp`, the service is exposed as `backend` and the `containerPort` value of the deployment is used as the port number.
   * `skupper.io/address` - the name of the service on the service network.
   * `skupper.io/port` - one or more ports for the service on the service network.

   <dl><dt><strong>📌 NOTE</strong></dt><dd>

   When exposing services, rather than other resources like deployments, you can use the `skupper.io/target` annotation to avoid modifying the original service.
   For example, if you want to expose the `backend` service:

   ```bash
   $ kubectl annotate service backend "skupper.io/address=van-backend" "skupper.io/port=8080" \
   "skupper.io/proxy=tcp" "skupper.io/target=backend"
   ```

   This allows you to delete and recreate the `backend` service without having to apply the annotation again.
   </dd></dl>
4. Check that you have exposed the service:

   ```bash
   $ skupper service status -v
   Services exposed through Skupper:
   ╰─ backend:8080 (tcp)
      ╰─ Sites:
         ├─ 4d80f485-52fb-4d84-b10b-326b96e723b2(west)
         │  policy: disabled
         ╰─ 316fbe31-299b-490b-9391-7b46507d76f1(east)
            │ policy: disabled
            ╰─ Targets:
               ╰─ backend:8080 name=backend-9d84544df-rbzjx
   ```

   **📌 NOTE**\
   The related targets for services are only displayed when the target is available on the current cluster.

### Understanding Skupper annotations

Annotations allow you to expose services on the service network.
This section provides details on the scope of those annotations

* **skupper.io/address**\
The name of the service on the service network.
Applies to:
  * Deployments
  * StatefulSets
  * DaemonSets
  * Services
* **skupper.io/port**\
The port for the service on the service network.
Applies to:
  * Deployments
  * StatefulSets
  * DaemonSets
* **skupper.io/proxy**\
The protocol you want to use, `tcp`, `http` or `http2`.
Applies to:
  * Deployments
  * StatefulSets
  * DaemonSets
  * Services
* **skupper.io/target**\
The name of the target service you want to expose.
Applies to:
  * Services
* **skupper.io/service-labels**\
A comma separated list of label keys and values for the exposed service.
You can use this annotation to set up labels for monitoring exposed services.
Applies to:
  * Deployments
  * DaemonSets
  * Services

### Site ConfigMap YAML reference

Using YAML files to configure Skupper requires that you understand all the fields so that you provision the site you require.

The following YAML defines a Skupper site:
```yaml
apiVersion: v1
data:
  name: my-site
  console: "true"
  flow-collector: "true"
  console-authentication: internal
  console-user: "username"
  console-password: "password"
  cluster-local: "false"
  edge: "false"
  service-sync: "true"
  ingress: "none"
kind: ConfigMap
metadata:
  name: skupper-site
```

* **name**\
Specifies the site name.
* **console**\
Enables the skupper console, defaults to `false`.
NOTE: You must enable `console` and `flow-collector` for the console to function.
* **flow-collector**\
Enables the flow collector, defaults to `false`.
* **console-authentication**\
Specifies the skupper console authentication method. The options are `openshift`, `internal`, `unsecured`.
* **console-user**\
Username for the `internal` authentication option.
* **console-password**\
Password for the `internal` authentication option.
* **cluster-local**\
Only accept connections from within the local cluster, defaults to `false`.
* **edge**\
Specifies whether an edge site is created, defaults to `false`.
* **service-sync**\
Specifies whether the services are synchronized across the service network, defaults to `true`.
* **ingress**\
Specifies whether the site supports ingress.
If you do not specify a value, the default ingress ('loadbalancer' on Kubernetes, 'route' on OpenShift) is enabled.
This allows you to create tokens usable from remote sites.

**📌 NOTE**\
All ingress types are supported using the same parameters as the `skupper` CLI.

### YAML for watching current namespace

The following example deploys Skupper to watch the current namespace.

```
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: skupper-site-controller
  labels:
    application: skupper-site-controller
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  labels:
    application: skupper-site-controller
  name: skupper-site-controller
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  - pods
  - pods/exec
  - services
  - secrets
  - serviceaccounts
  - events
  verbs:
  - get
  - list
  - watch
  - create
  - update
  - delete
  - patch
- apiGroups:
  - apps
  resources:
  - deployments
  - statefulsets
  - daemonsets
  verbs:
  - get
  - list
  - watch
  - create
  - update
  - delete
- apiGroups:
  - route.openshift.io
  resources:
  - routes
  verbs:
  - get
  - list
  - watch
  - create
  - delete
- apiGroups:
  - networking.k8s.io
  resources:
  - ingresses
  - networkpolicies
  verbs:
  - get
  - list
  - watch
  - create
  - delete
- apiGroups:
  - projectcontour.io
  resources:
  - httpproxies
  verbs:
  - get
  - list
  - watch
  - create
  - delete
- apiGroups:
  - rbac.authorization.k8s.io
  resources:
  - rolebindings
  - roles
  verbs:
  - get
  - list
  - watch
  - create
  - delete
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    application: skupper-site-controller
  name: skupper-site-controller
subjects:
- kind: ServiceAccount
  name: skupper-site-controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: skupper-site-controller
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skupper-site-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      application: skupper-site-controller
  template:
    metadata:
      labels:
        application: skupper-site-controller
    spec:
      serviceAccountName: skupper-site-controller
      # Please ensure that you can use SeccompProfile and do not use
      # if your project must work on old Kubernetes
      # versions < 1.19 or on vendors versions which
      # do NOT support this field by default
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: site-controller
        image: quay.io/skupper/site-controller:master
        securityContext:
          capabilities:
            drop:
            - ALL
          runAsNonRoot: true
          allowPrivilegeEscalation: false
        env:
        - name: WATCH_NAMESPACE
          valueFrom:
             fieldRef:
               fieldPath: metadata.namespace
```

### YAML for watching all namespaces

The following example deploys Skupper to watch all namespaces.

```
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: skupper-site-controller
  namespace: skupper-site-controller
  labels:
    application: skupper-site-controller
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    application: skupper-site-controller
  name: skupper-site-controller
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  - pods
  - pods/exec
  - services
  - secrets
  - serviceaccounts
  verbs:
  - get
  - list
  - watch
  - create
  - update
  - delete
- apiGroups:
  - apps
  resources:
  - deployments
  - statefulsets
  - daemonsets
  verbs:
  - get
  - list
  - watch
  - create
  - update
  - delete
- apiGroups:
  - route.openshift.io
  resources:
  - routes
  verbs:
  - get
  - list
  - watch
  - create
  - delete
- apiGroups:
  - networking.k8s.io
  resources:
  - ingresses
  - networkpolicies
  verbs:
  - get
  - list
  - watch
  - create
  - delete
- apiGroups:
  - projectcontour.io
  resources:
  - httpproxies
  verbs:
  - get
  - list
  - watch
  - create
  - delete
- apiGroups:
  - rbac.authorization.k8s.io
  resources:
  - rolebindings
  - roles
  verbs:
  - get
  - list
  - watch
  - create
  - delete
  - update
- apiGroups:
  - rbac.authorization.k8s.io
  resources:
  - clusterrolebindings
  verbs:
  - create
- apiGroups:
  - rbac.authorization.k8s.io
  resources:
  - clusterroles
  verbs:
  - bind
  resourceNames:
  - skupper-service-controller
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    application: skupper-site-controller
  name: skupper-site-controller
subjects:
- kind: ServiceAccount
  name: skupper-site-controller
  namespace: skupper-site-controller
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: skupper-site-controller
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skupper-site-controller
  namespace: skupper-site-controller
spec:
  replicas: 1
  selector:
    matchLabels:
      application: skupper-site-controller
  template:
    metadata:
      labels:
        application: skupper-site-controller
    spec:
      serviceAccountName: skupper-site-controller
      # Please ensure that you can use SeccompProfile and do not use
      # if your project must work on old Kubernetes
      # versions < 1.19 or on vendors versions which
      # do NOT support this field by default
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: site-controller
        image: quay.io/skupper/site-controller:1.3.0
        securityContext:
          capabilities:
            drop:
            - ALL
          runAsNonRoot: true
          allowPrivilegeEscalation: false
```
