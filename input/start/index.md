---
title: Getting started
---

# Getting started with Skupper

## Overview

To show Skupper in action, we need an application to work with.  This
guide uses an HTTP Hello World application with a frontend service and
a backend service.  The frontend uses the backend to process requests.
In this scenario, the frontend is deployed in the `west`
namespace, and the backend is deployed in the `east` namespace.

<img style="margin: 2em; width: 80%;" src="/images/hello-world-entities.svg"/>

While these instructions use this particular application for
demonstration purposes, the steps are the same for any Skupper
deployment.

## Prerequisites

You must have access to at least two Kubernetes namespaces.  In the
steps below, replace `west` and `east` with your chosen namespaces.

Each namespace can reside on **any cluster you choose**, and **you are
not limited to two**.  You can have one on your laptop, another on
Amazon, another on Google, and so on.  For convenience, you can have
them all on one cluster.

Skupper works with any flavor of Kubernetes.  Here are some of your
options for setting up Kubernetes clusters:

<ul class="column-list">
  <li><a href="minikube.html">Minikube</a></li>
  <li><a href="eks.html">Amazon Elastic Kubernetes Service (EKS)</a></li>
  <li><a href="aks.html">Azure Kubernetes Service (AKS)</a></li>
  <li><a href="gke.html">Google Kubernetes Engine (GKE)</a></li>
  <li><a href="ibmks.html">IBM Kubernetes Service</a></li>
  <li><a href="openshift.html">OpenShift</a></li>
  <li><a href="https://kubernetes.io/partners/#kcsp">More providers</a></li>
</ul>

These instructions require `kubectl` version 1.15 or later.  See the
[kubectl installation guide][kubectl-install] for more information.

[kubectl-install]: https://kubernetes.io/docs/tasks/tools/

## Step 1: Install the Skupper command-line tool in your environment

The `skupper` command-line tool is the primary entrypoint for
installing and configuring the Skupper infrastructure.  You need to
install the `skupper` command only once for each development
environment.

Use the [install script][install-script] to download and extract the
command:

<div class="code-label">Linux or Mac</div>

    curl https://skupper.io/install.sh | sh

The script installs the command under your home directory.  It prompts
you to add the command to your path if necessary.

For Windows and other installation options, see [Installing
Skupper](/install/index.html).

[install-script]: https://github.com/skupperproject/skupper-website/blob/main/docs/install.sh

## Step 2: Configure access to multiple namespaces

Skupper is designed for use with multiple namespaces, typically on
different clusters.  The `skupper` command uses your
[kubeconfig][kubeconfig] and current context to select the namespace
where it operates.

[kubeconfig]: https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/

Your kubeconfig is stored in a file in your home directory.  The
`skupper` and `kubectl` commands use the `KUBECONFIG` environment
variable to locate it.

A single kubeconfig supports only one active context per user.  Since
you will be using *two* contexts at once in this exercise, you need to
create two distinct kubeconfigs.  You can then use the first
kubeconfig in one console session, and the second kubeconfig in
another.

### Configure separate console sessions

Start a console session for each of your namespaces.  Set the
`KUBECONFIG` environment variable to a different path in each session.

<div class="code-label session-2">Console for West</div>

    export KUBECONFIG=$HOME/.kube/config-west

<div class="code-label session-1">Console for East</div>

    export KUBECONFIG=$HOME/.kube/config-east

**Note:** On Windows, use the `set` command instead of `export`:

<div class="code-label">Windows</div>

    set KUBECONFIG=%UserProfile%\.kube\config-<namespace>

### Configure cluster access

The methods for logging in and accessing clusters vary by Kubernetes
provider.  Find the instructions for your chosen providers and use
them to authenticate and establish access for each console session.

See the following links for more information:

<ul class="column-list">
  <li><a href="minikube.html#cluster-access">Minikube</a></li>
  <li><a href="eks.html#cluster-access">Amazon Elastic Kubernetes Service (EKS)</a></li>
  <li><a href="aks.html#cluster-access">Azure Kubernetes Service (AKS)</a></li>
  <li><a href="gke.html#cluster-access">Google Kubernetes Engine (GKE)</a></li>
  <li><a href="ibmks.html#cluster-access">IBM Kubernetes Service</a></li>
  <li><a href="openshift.html#cluster-access">OpenShift</a></li>
</ul>

### Set the current namespaces

Use `kubectl create namespace` to create the namespaces you wish to
use (or use existing namespaces).  Use `kubectl config set-context` to
set the current namespace for each session.

<div class="code-label session-2">Console for West</div>

    kubectl create namespace west
    kubectl config set-context --current --namespace west

<div class="code-label session-1">Console for East</div>

    kubectl create namespace east
    kubectl config set-context --current --namespace east

### Check your configurations

Once you have logged in and set the current namespaces, use the
`skupper status` command to check that each namespace is correctly
configured.  You should see the following output:

<div class="code-label session-2">Console for West</div>

    $ skupper status
    Skupper is not enabled in namespace 'west'

<div class="code-label session-1">Console for East</div>

    $ skupper status
    Skupper is not enabled in namespace 'east'

## Step 3: Install the Skupper router in each namespace

The `skupper init` command installs the Skupper router in the current
namespace.

**Note:** If you are using Minikube, [you need to start `minikube
tunnel`](minikube.html#running-minikube-tunnel) before you install
Skupper.

### Install the router

Run the `skupper init` command in the West namespace.

<div class="code-label session-2">West</div>

    $ skupper init
    Skupper is now installed in namespace 'west'.  Use 'skupper status' to get more information.

Now run the `skupper init` command in the East namespace.

<div class="code-label session-1">East</div>

    $ skupper init
    Skupper is now installed in namespace 'east'.  Use 'skupper status' to get more information.

### Check the installation

To check the status of each namespace, use the `skupper status`
command.

<div class="code-label session-2">West</div>

    $ skupper status
    Skupper is enabled in namespace 'west'. It is not linked to any other sites.

<div class="code-label session-1">East</div>

    $ skupper status
    Skupper is enabled in namespace 'east'. It is not linked to any other sites.

## Step 4: Link your namespaces

After installation, you have the infrastructure you need, but your
namespaces are not linked.  Creating a link requires use of
two `skupper` commands in conjunction, `skupper token create` and
`skupper link create`.

The `skupper token create` command generates a secret token that
signifies permission to create a link.  The token also carries the
link details.  The `skupper link create` command then uses the link
token to create a link to the namespace that generated it.

**Note:** The link token is truly a *secret*.  Anyone who has
the token can link to your namespace.  Make sure that only those
you trust have access to it.

### Generate a link token

In West, use the `skupper token create` command to generate a token.

<div class="code-label session-2">West</div>

    skupper token create ~/west.token

### Use the token to create a link

With the token in hand, you are ready to link the namespaces.  Pass
the token from West to the `skupper link create` command in East.

<div class="code-label session-1">East</div>

    skupper link create ~/west.token

If your console sessions are on different machines, you might need to
use `sftp` or a similar tool to transfer the token.

### Check the link

Use the `skupper status` command again to see if things have changed.
If the link is made, you should see the following output:

<div class="code-label session-2">West</div>

    $ skupper status
    Skupper is enabled in namespace 'west'. It is linked to 1 other site.

<div class="code-label session-1">East</div>

    $ skupper status
    Skupper is enabled in namespace 'east'. It is linked to 1 other site.

## Step 5: Expose your services

You now have a Skupper network capable of multi-cluster communication,
but no services are attached to it.  This step uses the `skupper
expose` command to make a Kubernetes deployment on one namespace
available on all the linked namespaces.

In the examples below, we use the Hello World application to
demonstrate service exposure.  The same steps apply for your own
application.

### Deploy the frontend and backend services

Use `kubectl create deployment` to start the frontend in West.

<div class="code-label session-2">West</div>

    kubectl create deployment frontend --image quay.io/skupper/hello-world-frontend

Likewise, use `kubectl create deployment` to start the backend in
East.

<div class="code-label session-1">East</div>

    kubectl create deployment backend --image quay.io/skupper/hello-world-backend --replicas 3

### Expose the backend service

At this point, we have the frontend and backend services running, but
the frontend has no way to contact the backend.  The frontend and
backend are in different namespaces (and perhaps different clusters),
and the backend has no public ingress.

Use the `skupper expose` command in East to make the `backend` service
available in West.

<div class="code-label session-1">East</div>

    skupper expose deployment/backend --port 8080

### Check the backend service

Use `kubectl get` in West to make sure the `backend` service from East
is present.  You should see output like this:

<div class="code-label session-2">West</div>

    $ kubectl get service/backend
    NAME         TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)       AGE
    backend      ClusterIP      10.96.175.18    <none>          8080/TCP      1m30s

### Test your application

Now we're ready to try it out.  Use `kubectl get` in West to look up
the external IP of the frontend service.  Then use `curl` or a similar
tool to request the `/api/health` endpoint at that address.

**Note:** The `<external-ip>` field in the following commands is
a placeholder.  The actual value is an IP address.

<div class="code-label session-2">West</div>

<pre><code>kubectl get service/frontend
curl http://<strong>&lt;external-ip&gt;</strong>:8080/api/health
</code></pre>

Sample output:

<pre><code>$ kubectl get service/frontend
NAME         TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
frontend     LoadBalancer   10.103.232.28   <strong>&lt;external-ip&gt;</strong>   8080:30407/TCP   15s

$ curl http://<strong>&lt;external-ip&gt;</strong>:8080/api/health
OK
</code></pre>

If everything is in order, you can now access the web interface by
navigating to this URL in your browser:

<pre><code>http://<strong>&lt;external-ip&gt;</strong>:8080/</pre></code>

The frontend assigns each new user a name.  Click **Say hello** to
send a greeting to the backend and get a greeting in response.

<img style="width: 100%;" src="/images/hello-world-frontend.png" width=""/>

### Summary

Our simple HTTP application has two services.  We deployed each
service to a different Kubernetes cluster.

Ordinarily, a multi-cluster deployment of this sort means that the
services have no way to communicate unless they are exposed to the
public internet.

By introducing Skupper into each namespace, we were able to create a
virtual application network that connects the services across cluster
boundaries.

See the [Hello World example][example] for more detail.

[example]: https://github.com/skupperproject/skupper-example-hello-world/blob/main/README.md#what-just-happened

## The condensed version

<div class="code-label">Skupper command installation</div>

    curl https://skupper.io/install.sh | sh

<div class="code-label session-2">West: Setup</div>

    export KUBECONFIG=~/.kube/config-west
    [Configure cluster access]
    kubectl create namespace west
    kubectl config set-context --current --namespace west
    skupper init
    skupper token create ~/west.token
    kubectl create deployment frontend --image quay.io/skupper/hello-world-frontend
    kubectl expose deployment/frontend --port 8080 --type LoadBalancer

<div class="code-label session-1">East: Setup</div>

    export KUBECONFIG=~/.kube/config-east
    [Configure cluster access]
    kubectl create namespace east
    kubectl config set-context --current --namespace east
    skupper init --ingress none
    skupper link create ~/west.token
    kubectl create deployment backend --image quay.io/skupper/hello-world-backend --replicas 3
    skupper expose deployment/backend --port 8080

<div class="code-label session-2">West: Testing</div>

    kubectl get service/frontend
    [Look up the external IP of the frontend service]
    curl http://<external-ip>:8080/api/health
    [Navigate to http://<external-ip>:8080/ in your browser]

## Cleaning up

To remove Skupper and the other resources from this exercise, use
the following commands:

<div class="code-label session-2">West</div>

    skupper delete
    kubectl delete service/frontend
    kubectl delete deployment/frontend

<div class="code-label session-1">East</div>

    skupper delete
    kubectl delete deployment/backend

## Next steps

Now that you know how to connect services running on multiple
clusters, here are a few more things to look at:

 - [Check out the HTTP Hello World example in more detail](https://github.com/skupperproject/skupper-example-hello-world)
 - [See how you can connect any TCP-based service](https://github.com/skupperproject/skupper-example-tcp-echo)
 - [Explore the examples](/examples/index.html)
 - [Configuring Skupper sites using YAML](/docs/declarative/index.html)
