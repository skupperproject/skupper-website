---
title: Getting started
---

# Getting started with Skupper

<nav class="toc">
  <div><a href="#prerequisites">Prerequisites</a></div>
  <div><a href="#step-1-install-the-skupper-command-line-tool-in-your-environment">Step 1: Install the Skupper command-line tool in your environment</a></div>
  <div><a href="#step-2-configure-access-to-multiple-namespaces">Step 2: Configure access to multiple namespaces</a></div>
  <div><a href="#step-3-install-the-skupper-resources-in-each-namespace">Step 3: Install the Skupper resources in each namespace</a></div>
  <div><a href="#step-4-connect-your-namespaces">Step 4: Connect your namespaces</a></div>
  <div><a href="#step-5-expose-your-services">Step 5: Expose your services</a></div>
  <div><a href="#the-condensed-version">The condensed version</a></div>
  <div><a href="#cleaning-up">Cleaning up</a></div>
  <div><a href="#next-steps">Next steps</a></div>
</nav>

## Prerequisites

To get started with Skupper, you must have access to at least two
Kubernetes namespaces.  In the steps below, replace `us-east` and
`eu-north` with your chosen namespaces.

Each namespace can reside on **any cluster you choose**, and **you are
not limited to two**.  You can have one on your laptop, another on
Amazon, another on Google, and so on.  For convenience, you can have
them all on one cluster.

Skupper works with any flavor of Kubernetes.  Here are some of your
options for setting up Kubernetes clusters:

<ul class="column-list">
  <li><a href="minikube.html">Minikube</a></li>
  <li><a href="https://aws.amazon.com/eks/getting-started/">Amazon Elastic Kubernetes Service</a></li>
  <li><a href="https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes">Azure Kubernetes Service</a></li>
  <li><a href="https://cloud.google.com/kubernetes-engine/docs/quickstart">Google Kubernetes Engine</a></li>
  <li><a href="https://www.openshift.com/learn/get-started/">Red Hat OpenShift</a> or <a href="https://www.okd.io/">OKD</a></li>
  <li><a href="https://kubernetes.io/docs/concepts/cluster-administration/cloud-providers/">More providers</a></li>
  <!-- <li><a href="eks.html">Amazon Elastic Kubernetes Service</a></li> -->
  <!-- <li><a href="aks.html">Azure Kubernetes Service</a></li> -->
  <!-- <li><a href="gke.html">Google Kubernetes Engine</a></li> -->
  <!-- <li><a href="openshift.html">Red Hat OpenShift</a> or <a href="okd.html">OKD</a></li> -->
</ul>

These instructions require `kubectl` version 1.15 or later.  See the
[kubectl installation
guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/) for
more information.

## Step 1: Install the Skupper command-line tool in your environment

The `skupper` command-line tool is the primary entrypoint for
installing and configuring the Skupper infrastructure.  You need to
install the `skupper` command only once for each development
environment.

### Download and extract the command

To get the latest release of the Skupper command for your platform,
download it from GitHub and extract the executable using `tar` or
`unzip`.

<div class="code-label">Linux</div>

    curl -fL https://github.com/skupperproject/skupper-cli/releases/download/{{skupper_cli_release}}/linux.tgz | tar -xzf -

<div class="code-label">macOS</div>

    curl -fL https://github.com/skupperproject/skupper-cli/releases/download/{{skupper_cli_release}}/darwin.zip -o skupper.zip
    unzip skupper.zip

This produces an executable file named `skupper` in your current
directory.

### Place the command on your path

The subsequent steps assume `skupper` is on your path.  For example,
this is how you might install it in your home directory:

    mkdir -p $HOME/bin
    export PATH=$PATH:$HOME/bin
    mv skupper $HOME/bin

### Check the command

To test your installation, run the `skupper --version` command.  You
should see output like this:

    $ skupper --version
    skupper version {{skupper_cli_release}}

## Step 2: Configure access to multiple namespaces

Skupper is designed for use with multiple namespaces, typically on
different clusters.  The `skupper` command uses your kubeconfig and
current context to select the namespace where it operates.

To avoid getting your wires crossed, you must use a distinct
kubeconfig or context for each namespace.  The easiest way is to use
separate console sessions.

### Configure separate console sessions

Start a console session for each of your namespaces.  Set the
`KUBECONFIG` environment variable to a different path in each session.

<div class="code-label session-1">Console for US East</div>

    export KUBECONFIG=$HOME/.kube/config-us-east

<div class="code-label session-2">Console for EU North</div>

    export KUBECONFIG=$HOME/.kube/config-eu-north

### Log in to your clusters

The methods for logging in vary by Kubernetes provider.  Find the
instructions for your chosen provider or providers and use them to
authenticate and establish access for each console session.

<div class="code-label session-1">Console for US East</div>

    $ <login-command-for-your-provider>

<div class="code-label session-2">Console for EU North</div>

    $ <login-command-for-your-provider>

See the following links for more information:

<ul class="column-list">
  <li><a href="minikube.html#logging-in">Minikube</a></li>
  <li><a href="https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html">Amazon Elastic Kubernetes Service</a></li>
  <li><a href="https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#connect-to-the-cluster">Azure Kubernetes Service</a></li>
  <li><a href="https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl">Google Kubernetes Engine</a></li>
  <li><a href="https://docs.openshift.com/container-platform/4.1/cli_reference/getting-started-cli.html#cli-logging-in_cli-developer-commands">Red Hat OpenShift</a> or <a href="https://docs.okd.io/latest/cli_reference/get_started_cli.html#basic-setup-and-login">OKD</a></li>
</ul>

### Set the current namespaces

Use `kubectl create namespace` to create the namespaces you wish to
use.  Use `kubectl config set-context` to set the current namespace
for each session.

<div class="code-label session-1">Console for US East</div>

    kubectl create namespace us-east
    kubectl config set-context --current --namespace us-east

<div class="code-label session-2">Console for EU North</div>

    kubectl create namespace eu-north
    kubectl config set-context --current --namespace eu-north

### Check your configurations

Once you have logged in and set the current namespaces, use the
`skupper status` command to check that each namespace is correctly
configured.  You should see the following output:

<div class="code-label session-1">Console for US East</div>

    $ skupper status
    Skupper is not installed in 'us-east'.  Use 'skupper init' to install.

<div class="code-label session-2">Console for EU North</div>

    $ skupper status
    Skupper is not installed in 'eu-north'.  Use 'skupper init' to install.

## Step 3: Install the Skupper resources in each namespace

The `skupper init` command installs the Skupper router, proxy, and
related resources in the current namespace.

    skupper init [--id <installation-name>]

### Install the resources

Run `skupper init` once for each namespace you wish to connect.

<div class="code-label session-1">US East</div>

    skupper init

<div class="code-label session-2">EU North</div>

    skupper init

### Check the installation

To check the status of each namespace, use the `skupper status`
command.

<div class="code-label session-1">US East</div>

    $ skupper status
    Namespace 'us-east' is ready.  It is connected to 0 other namespaces.

<div class="code-label session-2">EU North</div>

    $ skupper status
    Namespace 'eu-north' is ready.  It is connected to 0 other namespaces.

## Step 4: Connect your namespaces

After installation, you have the infrastructure you need, but your
namespaces are not connected.  Creating a connection requires use of
two `skupper` commands in conjunction, `skupper connection-token` and
`skupper connect`.

The `skupper connection-token` command generates a secret token that
signifies permission to connect.  The token also carries the
connection details.  The `skupper connect` command uses the connection
token to establish a connection to the namespace that generated it.

**Note:** The connection token is truly a *secret*.  Anyone who has
the token can connect to your namespace.  Make sure that only those
you trust have access to it.

### Generate a connection token

On `us-east`, use the `skupper connection-token` command to generate a
token.

<div class="code-label session-1">US East</div>

    skupper connection-token $HOME/secret.yaml

### Use the token to form a connection

With the token in hand, you are ready to connect.  Pass the token from
`us-east` to the `skupper connect` command on `eu-north`.

<div class="code-label session-2">EU North</div>

    skupper connect $HOME/secret.yaml

If your console sessions are on different machines, you may need to
use `scp` or a similar tool to transfer the token.

### Check the connection

Use the `skupper status` command again to see if things have changed.
If the connection is made, you should see the following output:

<div class="code-label session-1">US East</div>

    $ skupper status
    Namespace 'us-east' is ready.  It is connected to 1 other namespace.

<div class="code-label session-2">EU North</div>

    $ skupper status
    Namespace 'eu-north' is ready.  It is connected to 1 other namespace.

## Step 5: Expose your services

You now have a Skupper network capable of multi-cluster communication,
but no services are attached to it.  This step uses the `kubectl
annotate` command to make a Kubernetes service on one namespace
available on all the connected namespaces.

    kubectl annotate <service> skupper.io/proxy=(http|tcp)

To demonstrate service exposure, we need an application to work with.
This guide uses an HTTP Hello World application with a frontend service
and a backend service.  The frontend uses the backend to process
requests.  In this scenario, the frontend is deployed in the
`eu-north` namespace, and the backend is deployed in the `us-east`
namespace.

<img style="margin: 2em; width: 80%;" src="{{site_url}}/images/hello-world-entities.svg"/>

### Deploy your application

Use `kubectl create deployment` and `kubectl expose` to
start the backend on `us-east` and create a service for it.

<div class="code-label session-1">US East</div>

    kubectl create deployment hello-world-backend --image quay.io/skupper/hello-world-backend
    kubectl expose deployment/hello-world-backend --port 8080

Then, use `kubectl create deployment` to start the frontend on
`eu-north`.  Use `kubectl expose` with `--type LoadBalancer` to make
the frontend externally accessible.

<div class="code-label session-2">EU North</div>

    kubectl create deployment hello-world-frontend --image quay.io/skupper/hello-world-frontend
    kubectl expose deployment/hello-world-frontend --port 8080 --type LoadBalancer

### Expose the service

At this point, we have the frontend and backend services running, but
the frontend has no way to contact the backend.  The frontend and
backend are in different namespaces (and perhaps different clusters),
and the backend has no public ingress.

Skupper uses an annotation to select services for availability on the
Skupper network.  Use the `kubectl annotate` command on `us-east` to
make `hello-world-backend` available on `eu-north`.

<div class="code-label session-1">US East</div>

    kubectl annotate service/hello-world-backend skupper.io/proxy=http

### Check the service

Use `kubectl get services` on `eu-north` to make sure the
`hello-world-backend` service from `us-east` is represented.  You
should see output like this:

<div class="code-label session-2">EU North</div>

    $ kubectl get services
    NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)          AGE
    [...]
    hello-world-backend    ClusterIP      10.106.92.175    <none>           8080/TCP         11h
    hello-world-frontend   LoadBalancer   10.111.133.137   10.111.133.137   8080:31313/TCP   6m31s
    [...]

### Test your application

Now your multi-cluster application is up and running.  Use `curl` to
see it in action.

<div class="code-label session-2">EU North</div>

    curl $(kubectl get service/hello-world-frontend -o jsonpath='http://{.status.loadBalancer.ingress[0].ip}:{.spec.ports[0].port}/')

You should see output like this:

    I am the frontend.  The backend says 'Hello 1'.

The embedded `kubectl` command above looks up the IP address and port
for the frontend service and generates a URL for use with `curl`.

## The condensed version

<div class="code-label">Skupper command installation</div>

    curl -fL https://github.com/skupperproject/skupper-cli/releases/download/{{skupper_cli_release}}/linux.tgz | tar -xzf -

<div class="code-label session-1">US East</div>

    export KUBECONFIG=~/.kube/config-us-east
    <provider-login-command>
    kubectl create namespace us-east
    kubectl config set-context --current --namespace us-east
    skupper init
    skupper connection-token ~/secret.yaml
    kubectl create deployment hello-world-backend --image quay.io/skupper/hello-world-backend
    kubectl expose deployment/hello-world-backend --port 8080
    kubectl annotate service/hello-world-backend skupper.io/proxy=http

<div class="code-label session-2">EU North</div>

    export KUBECONFIG=~/.kube/config-eu-north
    <provider-login-command>
    kubectl create namespace eu-north
    kubectl config set-context --current --namespace eu-north
    skupper init
    skupper connect ~/secret.yaml
    kubectl create deployment hello-world-frontend --image quay.io/skupper/hello-world-frontend
    kubectl expose deployment/hello-world-frontend --port 8080 --type LoadBalancer
    curl $(kubectl get service/hello-world-frontend -o jsonpath='http://{.status.loadBalancer.ingress[0].ip}:{.spec.ports[0].port}/')

## Cleaning up

To remove Skupper and the other resources from this exercise, use
the following commands:

<div class="code-label session-1">US East</div>

    skupper delete
    kubectl delete service/hello-world-backend
    kubectl delete deployment/hello-world-backend

<div class="code-label session-2">EU North</div>

    skupper delete
    kubectl delete service/hello-world-frontend
    kubectl delete deployment/hello-world-frontend

## Next steps

Now that you know how to connect services running on multiple
clusters, here are a few more things to look at:

 - [Check out the HTTP Hello World example in more detail](https://github.com/skupperproject/skupper-example-hello-world)
 - [See how you can connect any TCP-based service](https://github.com/skupperproject/skupper-example-tcp-echo)
 - [Explore the examples]({{site_url}}/examples/index.html)
