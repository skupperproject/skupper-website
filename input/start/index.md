---
title: Getting started
---

# Getting started with Skupper

To show Skupper in action, we need an application to work with.  This
guide uses an HTTP Hello World application with a frontend service and
a backend service.  The frontend uses the backend to process requests.
In this scenario, the frontend is deployed in the `hello-world-west`
namespace, and the backend is deployed in the `hello-world-east`
namespace.

<img style="margin: 2em; width: 80%;" src="{{site.prefix}}/images/hello-world-entities.svg"/>

While these instructions use this particular application for
demonstration purposes, the steps are the same for any Skupper
deployment.

## Prerequisites

You must have access to at least two Kubernetes namespaces.  In the
steps below, you can replace `hello-world-west` and `hello-world-east`
with your chosen namespaces.

Each namespace can reside on any cluster you choose.  You can have one
on your laptop and another on EKS or OpenShift.  For convenience, you
can have them all on one cluster.

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

[kubectl-install]: https://kubernetes.io/docs/tasks/tools/#kubectl

## Step 1: Configure access to multiple namespaces

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

#### Configure separate console sessions

Start a console session for each of your namespaces.  Set the
`KUBECONFIG` environment variable to a different path in each session.

<div class="code-label session-2">Console for West</div>

    export KUBECONFIG=$HOME/.kube/config-hello-world-west

<div class="code-label session-1">Console for East</div>

    export KUBECONFIG=$HOME/.kube/config-hello-world-east

**Note:** On Windows, use the `set` command instead of `export`:

<div class="code-label">Windows</div>

    set KUBECONFIG=%UserProfile%\.kube\config-<namespace>

#### Configure cluster access

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

#### Set the current namespaces

Use `kubectl create namespace` to create the namespaces you wish to
use (or use existing namespaces).  Use `kubectl config set-context` to
set the current namespace for each session.

<div class="code-label session-2">Console for West</div>

    kubectl create namespace hello-world-west
    kubectl config set-context --current --namespace hello-world-west

<div class="code-label session-1">Console for East</div>

    kubectl create namespace hello-world-east
    kubectl config set-context --current --namespace hello-world-east

<!-- #### Check your configurations -->

<!-- Once you have logged in and set the current namespaces, use the -->
<!-- `skupper status` command to check that each namespace is correctly -->
<!-- configured.  You should see the following output: -->

<!-- <div class="code-label session-2">Console for West</div> -->

<!--     $ skupper status -->
<!--     Skupper is not enabled in namespace 'hello-world-west' -->

<!-- <div class="code-label session-1">Console for East</div> -->

<!--     $ skupper status -->
<!--     Skupper is not enabled in namespace 'hello-world-east' -->

## Step 2: Install Skupper on your clusters

To use Skupper on your Kubernetes, you need to deploy the Skupper
controller and custom resource definitions (CRDs).

Use `kubectl apply` with the [install
YAML](https://skupper.io/install.yaml) to install Skupper on each
cluster:

<div class="code-label session-2">West</div>

    kubectl apply -f https://skupper.io/install.yaml

<div class="code-label session-1">East</div>

    kubectl apply -f https://skupper.io/install.yaml

For other installation options, see [Installing Skupper on
Kubernetes]({{site.prefix}}/docs/install/index.html).

## Step 3: Install the Skupper CLI

This guide uses the Skupper command-line interface (CLI) to deploy a
Skupper network.  You need to install the `skupper` command only once
for each development environment.

Use the [install script][install-script] to download and extract the
command:

<div class="code-label">Linux or Mac</div>

    curl https://skupper.io/install.sh | sh

The script installs the command under your home directory.  It prompts
you to add the command to your path if necessary.

For other installation options, see [Installing the Skupper
CLI]({{site.prefix}}/docs/install/index.html#installing-the-skupper-cli).

[install-script]: https://github.com/skupperproject/skupper-website/blob/main/docs/install.sh

## Step 4: Create your sites

The `skupper site create` command sets up a Skupper site in the
current namespace.

**Note:** If you are using Minikube, [you need to start `minikube
tunnel`](minikube.html#running-minikube-tunnel) before you install
Skupper.

#### Create the site

Run the `skupper site create` command in the West namespace.

<div class="code-label session-2">West</div>

    $ skupper site create west --enable-link-access
    Waiting for status...
    Site "west" is ready.

Now run the `skupper site create` command in the East namespace.

<div class="code-label session-1">East</div>

    $ skupper site create east
    Waiting for status...
    Site "east" is ready.

#### Check the installation

To check the status of each namespace, use the `skupper site status`
command.

<div class="code-label session-2">West</div>

    $ skupper site status
    NAME    STATUS  MESSAGE
    west    Ready   OK

<div class="code-label session-1">East</div>

    $ skupper site status
    NAME    STATUS  MESSAGE
    east    Ready   OK

## Step 5: Link your sites

After installation, you have the infrastructure you need, but your
sites are not linked.  Creating a link requires use of two `skupper`
commands in conjunction, `skupper token issue` and `skupper token
redeem`.

The `skupper token issue` command generates a secret token that
signifies permission to create a link.  The token also carries the
link details.  The `skupper token redeem` command then uses the link
token to create a link to the site that generated it.

**Note:** The link token is truly a *secret*.  Anyone who has
the token can link to your namespace.  Make sure that only those
you trust have access to it.

#### Issue a token

In West, use the `skupper token issue` command to generate a token.

<div class="code-label session-2">West</div>

    skupper token issue $HOME/west.token

#### Use the token to create a link

With the token in hand, you are ready to link the sites.  Pass
the token from West to the `skupper tokek redeem` command in East.

<div class="code-label session-1">East</div>

    skupper token redeem $HOME/west.token

If your console sessions are on different machines, you might need to
use `sftp` or a similar tool to transfer the token.

#### Check the link

Use the `skupper link status` command to see if the link is
established.  You should see the following output:

<div class="code-label session-1">East</div>

    $ skupper link status
    NAME                       STATUS  COST    MESSAGE
    hello-world-west-9b55e1b1  Ready   1       OK

## Step 6: Expose your services

You now have a Skupper network capable of multi-cluster communication,
but no services are attached to it.  This step uses the `skupper
listener` and `skupper connector` commands to make a Kubernetes
deployment on one namespace available on all the linked namespaces.

In this guide, we use the Hello World application to demonstrate
service exposure.  The same steps apply for your own application.

#### Deploy the frontend and backend services

Use `kubectl create deployment` to start the frontend in West.

<div class="code-label session-2">West</div>

    kubectl create deployment frontend --image quay.io/skupper/hello-world-frontend

Likewise, use `kubectl create deployment` to start the backend in
East.

<div class="code-label session-1">East</div>

    kubectl create deployment backend --image quay.io/skupper/hello-world-backend --replicas 3

#### Expose the backend service

At this point, we have the frontend and backend services running, but
the frontend has no way to connect to the backend.  The frontend and
backend are in different namespaces (and perhaps different clusters),
and the backend has no public ingress.

In West, use the skupper listener create command to create a listener
for the backend. In East, use the skupper connector create command to
create a matching connector.

Use the `skupper connector create` command in East to create a
connector for the target workload.

<div class="code-label session-1">East</div>

    $ skupper connector create backend 8080
    Waiting for create to complete...
    Connector "backend" is configured.

Use the `skupper listener create` command in West to create a matching
listener.

<div class="code-label session-2">West</div>

    $ skupper listener create backend 8080
    Waiting for create to complete...
    Listener "backend" is configured.

The commands shown above use the name argument, `backend`, to also set
the default routing key and workload.  You can use the `--routing-key`
and `--workload` options to set specific values.

#### Check the backend service

Use `kubectl get` in West to make sure the `backend` service from East
is present.  You should see output like this:

<!-- XXX skupper listener status -->

<div class="code-label session-2">West</div>

    $ kubectl get service/backend
    NAME         TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)       AGE
    backend      ClusterIP      10.96.175.18    <none>          8080/TCP      1m30s

#### Test your application

To test our Hello World, we need external access to the frontend.
Use `kubectl port-forward` to make the frontend available at
`localhost:8080`.

<div class="code-label session-2">West</div>

    kubectl port-forward deployment/frontend 8080:8080

If everything is in order, you can now access the web interface by
navigating to this URL in your browser:

    http://localhost:8080/

The frontend assigns each new user a name.  Click **Say hello** to
send a greeting to the backend and get a greeting in response.

<!-- XXX Replace image -->

<img style="width: 100%;" src="{{site.prefix}}/images/hello-world-frontend.png"/>

## Summary

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

#### The steps in condensed form

<div class="code-label">Skupper CLI installation</div>

    curl https://skupper.io/install.sh | sh

<div class="code-label session-2">West: Setup</div>

    export KUBECONFIG=$HOME/.kube/config-hello-world-west
    [Configure cluster access]
    kubectl create namespace hello-world-west
    kubectl config set-context --current --namespace hello-world-west
    kubectl create deployment frontend --image quay.io/skupper/hello-world-frontend
    kubectl apply -f https://skupper.io/install.yaml
    skupper site create west --enable-link-access
    skupper token issue ~/west.token
    skupper listener create backend 8080

<div class="code-label session-1">East: Setup</div>

    export KUBECONFIG=$HOME/.kube/config-hello-world-east
    [Configure cluster access]
    kubectl create namespace hello-world-east
    kubectl config set-context --current --namespace hello-world-east
    kubectl create deployment backend --image quay.io/skupper/hello-world-backend --replicas 3
    kubectl apply -f https://skupper.io/install.yaml
    skupper site create east
    skupper token redeem ~/west.token
    skupper connector create backend 8080

<div class="code-label session-2">West: Testing</div>

    kubectl port-forward deployment/frontend 8080:8080
    curl http://localhost:8080/api/health
    [Navigate to http://localhost:8080/ in your browser]

## Cleaning up

To remove Skupper and the other resources from this exercise, use
the following commands:

<div class="code-label session-2">West</div>

    skupper site delete --all
    kubectl delete deployment/frontend

<div class="code-label session-1">East</div>

    skupper site delete --all
    kubectl delete deployment/backend

## Next steps

Now that you know how to connect services running on multiple
clusters, here are a few more things to look at:

 - [Check out the HTTP Hello World example in more detail](https://github.com/skupperproject/skupper-example-hello-world)
 - [See how you can connect any TCP-based service](https://github.com/skupperproject/skupper-example-tcp-echo)
 - [Explore the examples]({{site.prefix}}/examples/index.html)
