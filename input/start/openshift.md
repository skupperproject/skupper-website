---
title: Getting started
---

# Getting started with Skupper on OpenShift

These instructions are specific to OpenShift and use a declaritive YAML-based deployment, 
however you can use YAML with other Kubernetes variants.
See [Getting Started on Kubernetes](./index.html) for more generic and CLI based instructions.

## Overview

To show Skupper in action, we need an application to work with.  This
guide uses an HTTP Hello World application with a frontend service and
a backend service.  The frontend uses the backend to process requests.
In this scenario, the frontend is deployed in the `west`
Project, and the backend is deployed in the `east` Project.

<img style="margin: 2em; width: 80%;" src="{{site_url}}/images/hello-world-entities-openshift.svg"/>

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
    $ oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/0.3/cmd/site-controller/deploy-watch-current-ns.yaml
    $ oc new-project west
    $ oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/0.3/cmd/site-controller/deploy-watch-current-ns.yaml


After completion, you should see a deployment named `skupper-site-controller` in each Project.


### Create a Skupper site in both Projects

To create a Skupper site, you must apply a ConfigMap, for example:

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

To apply the ConfigMap:

    $ oc apply -f <filename>

Create and apply a ConfigMap for **both** Projects, using a different value for `data:name` for each site.

For more information about each parameter, see the [Site Controller README](https://github.com/skupperproject/skupper/blob/master/cmd/site-controller/README.md).

After completion, you should see deployments named `skupper-service-controller` and `skupper-router` in each Project.


## Step 2: Connect the OpenShift Projects

### Create a token request YAML file

Requesting tokens requires the following format YAML file:

    apiVersion: v1
    kind: Secret
    metadata:
      labels:
        skupper.io/type: connection-token-request
      name: west-secret

Save as `token-request.yaml`.

### Generate a connection token

Change to the `west` Project and request a token:

    $ oc project west
    $ oc apply -f token-request.yaml

To verify this step, check that a secret named `west-secret` is created.


### Pass the connection token

    $ oc get secret  --export -o yaml west-secret > west-secret.yaml

Change to the `east` Project and apply the token:

    $ oc project east
    $ oc apply -f west-secret.yaml



## Step 3: Expose your services

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

Create annotations of the backend deployment:
----
key: skupper.io/proxy
value: http

key: skupper.io/port
value: 8080

----

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

<div class="code-label session-2">West: Setup</div>

    oc new-project west
    oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/0.3/cmd/site-controller/deploy-watch-current-ns.yaml
    oc apply -f /home/pwright/token-request.yaml
    oc get secret  --export -o yaml west-secret > west-secret.yaml
    oc create deployment --port 8080 hello-world-backend --image quay.io/skupper/hello-world-frontend
    oc expose deployment hello-world-frontend --port 8080 --type LoadBalancer

    
<div class="code-label session-1">East: Setup</div>

    oc new-project east
    oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/0.3/cmd/site-controller/deploy-watch-current-ns.yaml
    oc apply -f west-secret.yaml
    oc create deployment --port 8080 hello-world-backend --image quay.io/skupper/hello-world-backend
    oc annotate deployment/hello-world-backend skupper.io/proxy="http"
    oc annotate deployment/hello-world-backend skupper.io/port="8080"



<div class="code-label session-2">West: Testing</div>

  

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
