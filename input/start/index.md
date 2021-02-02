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
  <li><a href="https://aws.amazon.com/eks/getting-started/">Amazon Elastic Kubernetes Service</a></li>
  <li><a href="https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes">Azure Kubernetes Service</a></li>
  <li><a href="https://cloud.google.com/kubernetes-engine/docs/quickstart">Google Kubernetes Engine</a></li>
  <li><a href="https://cloud.ibm.com/docs/containers?topic=containers-getting-started">IBM Kubernetes Service</a></li>
  <li><a href="https://www.openshift.com/learn/get-started/">Red Hat OpenShift</a> or <a href="https://www.okd.io/">OKD</a></li>
  <li><a href="https://kubernetes.io/docs/concepts/cluster-administration/cloud-providers/">More providers</a></li>
  <!-- <li><a href="eks.html">Amazon Elastic Kubernetes Service</a></li> -->
  <!-- <li><a href="aks.html">Azure Kubernetes Service</a></li> -->
  <!-- <li><a href="gke.html">Google Kubernetes Engine</a></li> -->
  <!-- <li><a href="openshift.html">Red Hat OpenShift</a> or <a href="okd.html">OKD</a></li> -->
</ul>

These instructions require the proper version of `kubectl` for your
installation.  For Minikube installations see [Minikube
Prerequisites](minikube.html#prerequisites).  Other installations
require `kubectl` version 1.15 or later.

See the [kubectl installation
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

    curl -fL https://github.com/skupperproject/skupper/releases/download/{{skupper_release}}/skupper-cli-{{skupper_release}}-linux-amd64.tgz | tar -xzf -

<div class="code-label">Mac</div>

    curl -fL https://github.com/skupperproject/skupper/releases/download/{{skupper_release}}/skupper-cli-{{skupper_release}}-mac-amd64.tgz | tar -xzf -

This produces an executable file named `skupper` in your current
directory.

To download artifacts for other platforms, see [Skupper
releases](/releases/index.html).

### Place the command on your path

The subsequent steps assume `skupper` is on your path.  As an example,
this is how you might install it in your home directory:

    mkdir -p $HOME/bin
    export PATH=$PATH:$HOME/bin
    mv skupper $HOME/bin

### Check the command

To test your installation, run the `skupper --version` command.  You
should see output like this:

    $ skupper --version
    skupper version {{skupper_release}}

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

<div class="code-label session-2">Console for West</div>

    export KUBECONFIG=$HOME/.kube/config-west

<div class="code-label session-1">Console for East</div>

    export KUBECONFIG=$HOME/.kube/config-east

### Log in to your clusters

The methods for logging in vary by Kubernetes provider.  Find the
instructions for your chosen provider or providers and use them to
authenticate and establish access for each console session.

<div class="code-label session-2">Console for West</div>

    $ <login-command-for-your-provider>

<div class="code-label session-1">Console for East</div>

    $ <login-command-for-your-provider>

See the following links for more information:

<ul class="column-list">
  <li><a href="minikube.html#logging-in">Minikube</a></li>
  <li><a href="https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html">Amazon Elastic Kubernetes Service</a></li>
  <li><a href="https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#connect-to-the-cluster">Azure Kubernetes Service</a></li>
  <li><a href="https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl">Google Kubernetes Engine</a></li>
  <li><a href="https://cloud.ibm.com/docs/containers?topic=containers-access_cluster">IBM Kubernetes Service</a></li>
  <li><a href="https://docs.openshift.com/container-platform/4.1/cli_reference/getting-started-cli.html#cli-logging-in_cli-developer-commands">Red Hat OpenShift</a> or <a href="https://docs.okd.io/latest/cli_reference/get_started_cli.html#basic-setup-and-login">OKD</a></li>
</ul>

### Set the current namespaces

Use `kubectl create namespace` to create the namespaces you wish to
use.  Use `kubectl config set-context` to set the current namespace
for each session.

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
    skupper not enabled for west

<div class="code-label session-1">Console for East</div>

    $ skupper status
    skupper not enabled for east

## Step 3: Install the Skupper router in each namespace

The `skupper init` command installs the Skupper router in the current
namespace.

### Install the router

Run the `skupper init` command in the West namespace.

<div class="code-label session-2">West</div>

    $ skupper init
    Skupper is now installed in namespace 'west'.  Use 'skupper status' to get more information.

Now run the `skupper init` command in the East namespace.

<div class="code-label session-1">East</div>

    $ skupper init --cluster-local
    Skupper is now installed in namespace 'east'.  Use 'skupper status' to get more information.

Note that using `--cluster-local` in East is done simply to make
local development with Minikube easier.  It's not required if your two
namespaces are on different hosts or on public clusters.

### Check the installation

To check the status of each namespace, use the `skupper status`
command.

<div class="code-label session-2">West</div>

    $ skupper status
    Skupper enabled for namespace 'west'. It is not connected to any other sites.

<div class="code-label session-1">East</div>

    $ skupper status
    Skupper enabled for namespace 'east'. It is not connected to any other sites.

## Step 4: Connect your namespaces

After installation, you have the infrastructure you need, but your
namespaces are not connected.  Creating a connection requires use of
two `skupper` commands in conjunction, `skupper connection-token` and
`skupper connect`.

The `skupper connection-token` command generates a secret token that
signifies permission to connect.  The token also carries the
connection details.  The `skupper connect` command then uses the
connection token to establish a connection to the namespace that
generated it.

**Note:** The connection token is truly a *secret*.  Anyone who has
the token can connect to your namespace.  Make sure that only those
you trust have access to it.

### Generate a connection token

In West, use the `skupper connection-token` command to generate a
token.

<div class="code-label session-2">West</div>

    skupper connection-token $HOME/secret.yaml

### Use the token to form a connection

With the token in hand, you are ready to connect.  Pass the token from
West to the `skupper connect` command in East.

<div class="code-label session-1">East</div>

    skupper connect $HOME/secret.yaml

If your console sessions are on different machines, you might need to
use `scp` or a similar tool to transfer the token.  If you are using
Minikube, [you need to run `minikube
tunnel`](minikube.html#prerequisites) for this to work.

### Check the connection

Use the `skupper status` command again to see if things have changed.
If the connection is made, you should see the following output:

<div class="code-label session-2">West</div>

    $ skupper status
    Skupper enabled for namespace 'west'. It is connected to 1 other site.

<div class="code-label session-1">East</div>

    $ skupper status
    Skupper enabled for namespace 'east'. It is connected to 1 other site.

## Step 5: Expose your services

You now have a Skupper network capable of multi-cluster communication,
but no services are attached to it.  This step uses the `skupper
expose` command to make a Kubernetes deployment on one namespace
available on all the connected namespaces.

In the examples below, we use the Hello World application to
demonstrate service exposure.  The same steps apply for your own
application.

### Deploy the frontend and backend services

Use `kubectl create deployment` to start the frontend in West.

<div class="code-label session-2">West</div>

    kubectl create deployment hello-world-frontend --image quay.io/skupper/hello-world-frontend

Likewise, use `kubectl create deployment` to start the backend in
East.

<div class="code-label session-1">East</div>

    kubectl create deployment hello-world-backend --image quay.io/skupper/hello-world-backend

### Expose the backend service

At this point, we have the frontend and backend services running, but
the frontend has no way to contact the backend.  The frontend and
backend are in different namespaces (and perhaps different clusters),
and the backend has no public ingress.

Use the `skupper expose` command in East to make `hello-world-backend`
available in West.

<div class="code-label session-1">East</div>

    skupper expose deployment hello-world-backend --port 8080 --protocol http

### Check the backend service

Use `kubectl get services` in West to make sure the
`hello-world-backend` service from East is represented.  You should
see output like this (along with some other services):

<div class="code-label session-2">West</div>

    $ kubectl get services
    NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)       AGE
    hello-world-backend    ClusterIP      10.96.175.18    <none>          8080/TCP      1m30s

### Test your application

To test our Hello World, we need external access to the frontend (not
the backend).  Use `kubectl expose` with `--type LoadBalancer` to make
the frontend accessible using a conventional Kubernetes ingress.

<div class="code-label session-2">West</div>

    kubectl expose deployment hello-world-frontend --port 8080 --type LoadBalancer

It takes a moment for the external IP to become available.  If you are
using Minikube, [you need to run `minikube
tunnel`](minikube.html#prerequisites) for this to work.

Now use `curl` to see it in action.  The embedded `kubectl get`
command below looks up the IP address for the frontend service and
generates a URL for use with `curl`.

<div class="code-label session-2">West</div>

    curl $(kubectl get service hello-world-frontend -o jsonpath='http://{.status.loadBalancer.ingress[0].ip}:8080/')

**Note:** If the embedded `kubectl get` command fails to get the IP,
you can find it manually by running `kubectl get services` and looking
up the external IP of the `hello-world-frontend` service.

You should see output like this:

    I am the frontend.  The backend says 'Hello from hello-world-backend-869cd94f69-wh6zt (1)'.

### Summary

Our simple HTTP application has two services.  We deployed each
service to a different Kubernetes cluster.

Ordinarily, a multi-cluster deployment of this sort means that the
services have no way to communicate unless they are exposed to the
public internet.

By introducing Skupper into each namespace, we were able to create a
virtual application network that connects the services across cluster
boundaries.

See the [Hello World
example](https://github.com/skupperproject/skupper-example-hello-world/blob/master/README.md#what-just-happened)
for more detail.

## The condensed version

<div class="code-label">Skupper command installation</div>

    curl -fL https://github.com/skupperproject/skupper-cli/releases/download/{{skupper_release}}/skupper-cli-{{skupper_release}}-linux-amd64.tgz | tar -xzf -

<div class="code-label session-2">West: Setup</div>

    export KUBECONFIG=~/.kube/config-west
    <provider-login-command>
    kubectl create namespace west
    kubectl config set-context --current --namespace west
    skupper init
    skupper connection-token ~/secret.yaml
    kubectl create deployment hello-world-frontend --image quay.io/skupper/hello-world-frontend
    kubectl expose deployment hello-world-frontend --port 8080 --type LoadBalancer

<div class="code-label session-1">East: Setup</div>

    export KUBECONFIG=~/.kube/config-east
    <provider-login-command>
    kubectl create namespace east
    kubectl config set-context --current --namespace east
    skupper init --cluster-local
    skupper connect ~/secret.yaml
    kubectl create deployment hello-world-backend --image quay.io/skupper/hello-world-backend
    skupper expose deployment hello-world-backend --port 8080 --protocol http

<div class="code-label session-2">West: Testing</div>

    curl $(kubectl get service hello-world-frontend -o jsonpath='http://{.status.loadBalancer.ingress[0].ip}:8080/')

## Cleaning up

To remove Skupper and the other resources from this exercise, use
the following commands:

<div class="code-label session-2">West</div>

    skupper delete
    kubectl delete service/hello-world-frontend
    kubectl delete deployment/hello-world-frontend

<div class="code-label session-1">East</div>

    skupper delete
    kubectl delete deployment/hello-world-backend

## Next steps

Now that you know how to connect services running on multiple
clusters, here are a few more things to look at:

 - [Check out the HTTP Hello World example in more detail](https://github.com/skupperproject/skupper-example-hello-world)
 - [See how you can connect any TCP-based service](https://github.com/skupperproject/skupper-example-tcp-echo)
 - [Explore the examples](/examples/index.html)
 - [Configuring Skupper sites using YAML](/docs/declarative.html)
