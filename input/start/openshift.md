---
title: Getting started
---

# Getting started with Skupper on OpenShift

## Overview

To show Skupper in action, we need an application to work with.  This
guide uses an HTTP Hello World application with a frontend service and
a backend service.  The frontend uses the backend to process requests.
In this scenario, the frontend is deployed in the `west`
Project, and the backend is deployed in the `east` Project.

<img style="margin: 2em; width: 80%;" src="{{site_url}}/images/hello-world-entities-openshift.svg"/>

These instructions are specific to OpenShift and use a declaritive YAML-based deployment.
See [Getting Started on Kubernetes](./index.html) for more generic and CLI based instructions.

## Prerequisites

You must have access to at least two OpenShift Projects.  In the
steps below, replace `west` and `east` with your chosen Projects.

Each Project can reside on **any cluster you choose**, and **you are
not limited to two**.  You can have one on your laptop, another on
Amazon, another on Google, and so on.  For convenience, you can have
them all on one cluster.

<!-- need OpenShift references here -->

These instructions require the OpenShift client, version 3.11 or later.

See the [download page](https://access.redhat.com/downloads/content/290) for
more information.

## Step 1: Deploy Skupper in your environment

The `skupper` templates can configure the current Project or all Projects in a cluster to run Skupper.

### Deploy Skupper in both Projects

To configure Skupper for both Projects:

    $ oc new-project east
    $ oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/master/cmd/site-controller/deploy-watch-current-ns.yaml
    $ oc new-project west
    $ oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/master/cmd/site-controller/deploy-watch-current-ns.yaml


After completion, you should see a deployment named `skupper-site-controller` in each Project.


### Create a Skupper site in both Projects

To create a Skupper site, you must apply a ConfigMap, for example:

```
apiVersion: v1
data:
  cluster-local: "false"
  console: "true"
  console-authentication: internal
  console-password: "barney"
  console-user: "rubble"
  edge: "false"
  name: east-site
  router-console: "true"
  service-controller: "true"
  service-sync: "true"
kind: ConfigMap
metadata:
  name: skupper-site
```

To apply the ConfigMap:

    $ oc apply -f <filename>

Create and apply a ConfigMap for both Projects, using a different value for `data:name` for each site.

For more information about each parameter, see the [Site Controller README](https://github.com/skupperproject/skupper/blob/master/cmd/site-controller/README.md).



## Step 2: Configure access to multiple Projects

Skupper is designed for use with multiple Projects, typically on
different clusters and uses your kubeconfig and
current context to select the Project where it operates.

To avoid getting your wires crossed, you must use a distinct
kubeconfig or context for each Project.  The easiest way is to use
separate console sessions.

### Configure separate console sessions

Start a console session for each of your Projects.  Set the
`KUBECONFIG` environment variable to a different path in each session.

<div class="code-label session-2">Console for West</div>

    export KUBECONFIG=$HOME/.kube/config-west

<div class="code-label session-1">Console for East</div>

    export KUBECONFIG=$HOME/.kube/config-east

### Log in to your clusters

The methods for logging in vary by OpenShift provider.  Find the
instructions for your chosen provider or providers and use them to
authenticate and establish access for each console session.

<div class="code-label session-2">Console for West</div>

    $ <login-command-for-your-provider>

<div class="code-label session-1">Console for East</div>

    $ <login-command-for-your-provider>

See the following links for more information:

<ul class="column-list">
  <li><a href="minikube.html#logging-in">Minikube</a></li>
  <li><a href="https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html">Amazon Elastic OpenShift Service</a></li>
  <li><a href="https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#connect-to-the-cluster">Azure OpenShift Service</a></li>
  <li><a href="https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-oc">Google OpenShift Engine</a></li>
  <li><a href="https://docs.openshift.com/container-platform/4.1/cli_reference/getting-started-cli.html#cli-logging-in_cli-developer-commands">Red Hat OpenShift</a> or <a href="https://docs.okd.io/latest/cli_reference/get_started_cli.html#basic-setup-and-login">OKD</a></li>
</ul>

### Set the current Projects

Use `oc create Project` to create the Projects you wish to
use.  Use `oc config set-context` to set the current Project
for each session.

<div class="code-label session-2">Console for West</div>

    oc create Project west
    oc config set-context --current --Project west

<div class="code-label session-1">Console for East</div>

    oc create Project east
    oc config set-context --current --Project east

### Check your configurations

Once you have logged in and set the current Projects, use the
`skupper status` command to check that each Project is correctly
configured.  You should see the following output:

<div class="code-label session-2">Console for West</div>

    $ skupper status
    skupper not enabled for west

<div class="code-label session-1">Console for East</div>

    $ skupper status
    skupper not enabled for east

## Step 3: Install the Skupper router in each Project

The `skupper init` command installs the Skupper router in the current
Project.

### Install the router

Run the `skupper init` command in the West Project.

<div class="code-label session-2">West</div>

    $ skupper init
    Skupper is now installed in Project 'west'.  Use 'skupper status' to get more information.

Now run the `skupper init` command in the East Project.

<div class="code-label session-1">East</div>

    $ skupper init --edge
    Skupper is now installed in Project 'east'.  Use 'skupper status' to get more information.

Using the `--edge` argument in East disables network ingress at the
Skupper router layer.  In our scenario, East needs to establish one
outbound connection to West.  It does not need to accept any incoming
connections.  As a result, no network ingress is required in East.

### Check the installation

To check the status of each Project, use the `skupper status`
command.

<div class="code-label session-2">West</div>

    $ skupper status
    Skupper enabled for Project 'west'. It is not connected to any other sites.

<div class="code-label session-1">East</div>

    $ skupper status
    Skupper enabled for Project 'east'. It is not connected to any other sites.

## Step 4: Connect your Projects

After installation, you have the infrastructure you need, but your
Projects are not connected.  Creating a connection requires use of
two `skupper` commands in conjunction, `skupper connection-token` and
`skupper connect`.

The `skupper connection-token` command generates a secret token that
signifies permission to connect.  The token also carries the
connection details.  The `skupper connect` command then uses the
connection token to establish a connection to the Project that
generated it.

**Note:** The connection token is truly a *secret*.  Anyone who has
the token can connect to your Project.  Make sure that only those
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
    Skupper enabled for Project 'west'. It is connected to 1 other site.

<div class="code-label session-1">East</div>

    $ skupper status
    Skupper enabled for Project 'east'. It is connected to 1 other site.

## Step 5: Expose your services

You now have a Skupper network capable of multi-cluster communication,
but no services are attached to it.  This step uses the `skupper
expose` command to make a OpenShift deployment on one Project
available on all the connected Projects.

In the examples below, we use the Hello World application to
demonstrate service exposure.  The same steps apply for your own
application.

### Deploy the frontend and backend services

Use `oc create deployment` to start the frontend in West.

<div class="code-label session-2">West</div>

    oc create deployment hello-world-frontend --image quay.io/skupper/hello-world-frontend

Likewise, use `oc create deployment` to start the backend in
East.

<div class="code-label session-1">East</div>

    oc create deployment hello-world-backend --image quay.io/skupper/hello-world-backend

### Expose the backend service

At this point, we have the frontend and backend services running, but
the frontend has no way to contact the backend.  The frontend and
backend are in different Projects (and perhaps different clusters),
and the backend has no public ingress.

Use the `skupper expose` command in East to make `hello-world-backend`
available in West.

<div class="code-label session-1">East</div>

    skupper expose deployment hello-world-backend --port 8080 --protocol http

### Check the backend service

Use `oc get services` in West to make sure the
`hello-world-backend` service from East is represented.  You should
see output like this (along with some other services):

<div class="code-label session-2">West</div>

    $ oc get services
    NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)       AGE
    hello-world-backend    ClusterIP      10.96.175.18    <none>          8080/TCP      1m30s

### Test your application

To test our Hello World, we need external access to the frontend (not
the backend).  Use `oc expose` with `--type LoadBalancer` to make
the frontend accessible using a conventional OpenShift ingress.

<div class="code-label session-2">West</div>

    oc expose deployment hello-world-frontend --port 8080 --type LoadBalancer

It takes a moment for the external IP to become available.  If you are
using Minikube, [you need to run `minikube
tunnel`](minikube.html#prerequisites) for this to work.

Now use `curl` to see it in action.  The embedded `oc get`
command below looks up the IP address for the frontend service and
generates a URL for use with `curl`.

<div class="code-label session-2">West</div>

    curl $(oc get service hello-world-frontend -o jsonpath='http://{.status.loadBalancer.ingress[0].ip}:8080/')

**Note:** If the embedded `oc get` command fails to get the IP,
you can find it manually by running `oc get services` and looking
up the external IP of the `hello-world-frontend` service.

You should see output like this:

    I am the frontend.  The backend says 'Hello from hello-world-backend-869cd94f69-wh6zt (1)'.

### Summary

Our simple HTTP application has two services.  We deployed each
service to a different OpenShift cluster.

Ordinarily, a multi-cluster deployment of this sort means that the
services have no way to communicate unless they are exposed to the
public internet.

By introducing Skupper into each Project, we were able to create a
virtual application network that connects the services across cluster
boundaries.

See the [Hello World
example](https://github.com/skupperproject/skupper-example-hello-world/blob/master/README.md#what-just-happened)
for more detail.

## The condensed version

<div class="code-label">Skupper command installation</div>

    curl -fL https://github.com/skupperproject/skupper-cli/releases/download/{{skupper_cli_release}}/skupper-cli-{{skupper_cli_release}}-linux-amd64.tgz | tar -xzf -

<div class="code-label session-2">West: Setup</div>

    export KUBECONFIG=~/.kube/config-west
    <provider-login-command>
    oc create Project west
    oc config set-context --current --Project west
    skupper init
    skupper connection-token ~/secret.yaml
    oc create deployment hello-world-frontend --image quay.io/skupper/hello-world-frontend
    oc expose deployment hello-world-frontend --port 8080 --type LoadBalancer

<div class="code-label session-1">East: Setup</div>

    export KUBECONFIG=~/.kube/config-east
    <provider-login-command>
    oc create Project east
    oc config set-context --current --Project east
    skupper init --edge
    skupper connect ~/secret.yaml
    oc create deployment hello-world-backend --image quay.io/skupper/hello-world-backend
    skupper expose deployment hello-world-backend --port 8080 --protocol http

<div class="code-label session-2">West: Testing</div>

    curl $(oc get service hello-world-frontend -o jsonpath='http://{.status.loadBalancer.ingress[0].ip}:8080/')

## Cleaning up

To remove Skupper and the other resources from this exercise, use
the following commands:

<div class="code-label session-2">West</div>

    skupper delete
    oc delete service/hello-world-frontend
    oc delete deployment/hello-world-frontend

<div class="code-label session-1">East</div>

    skupper delete
    oc delete deployment/hello-world-backend

## Next steps

Now that you know how to connect services running on multiple
clusters, here are a few more things to look at:

 - [Check out the HTTP Hello World example in more detail](https://github.com/skupperproject/skupper-example-hello-world)
 - [See how you can connect any TCP-based service](https://github.com/skupperproject/skupper-example-tcp-echo)
 - [Explore the examples]({{site_url}}/examples/index.html)
