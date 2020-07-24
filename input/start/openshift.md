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
not limited to two**.  For convenience, you can have
them all on one cluster.

See the [OpenShift website](https://www.openshift.com/) for more information.

These instructions require the OpenShift client, version 3.11 or later.

See the [download page](https://access.redhat.com/downloads/content/290) for
more information.

You do not need `cluster-admin` privileges.

## Step 1: Configure the backend Project to use Skupper

### Create the backend project and deploy Skupper

To deploy the site controller:

    $ oc new-project east
    $ oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/0.3/cmd/site-controller/deploy-watch-current-ns.yaml


### Create a Skupper site in the east Project

To create a Skupper site, you must apply a ConfigMap.

Create a file named `east-site.yml`

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

Note that the `data:name` value of `east-site`.

To apply the ConfigMap:

    $ oc apply -f east-site.yml

For more information about each parameter, see the [Site Controller README](https://github.com/skupperproject/skupper/blob/master/cmd/site-controller/README.md).

After completion, you should see deployments named `skupper-service-controller` and `skupper-router`.

## Step 2: Configure the frontend Project to use Skupper

### Create the frontend project and deploy Skupper

To deploy the site controller:

    $ oc new-project west
    $ oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/0.3/cmd/site-controller/deploy-watch-current-ns.yaml


### Create a Skupper site in the west Project

To create a Skupper site, you must apply a ConfigMap.

Create a file named `west-site.yml`

    apiVersion: v1
    data:
      cluster-local: "false"
      console: "true"
      console-authentication: internal
      console-password: "barney"
      console-user: "rubble"
      edge: "false"
      name: west-site
      router-console: "true"
      service-controller: "true"
      service-sync: "true"
    kind: ConfigMap
    metadata:
      name: skupper-site

Note that the `data:name` value of `west-site`.

To apply the ConfigMap:

    $ oc apply -f west-site.yml

For more information about each parameter, see the [Site Controller README](https://github.com/skupperproject/skupper/blob/master/cmd/site-controller/README.md).

After completion, you should see deployments named `skupper-service-controller` and `skupper-router`.

## Step 3: Connect the OpenShift Projects

To connect the OpenShift Projects, you must create a token in one project
and pass it to the other project.

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

Download the token and register it with the other project.

    $ oc get secret  --export -o yaml west-secret > west-secret.yaml

Change to the `east` Project and apply the token:

    $ oc project east
    $ oc apply -f west-secret.yaml


You now have a Skupper network capable of multi-cluster communication,
but no services are exposed to that network.

## Step 4: Deploy the services and expose the backend service to the Skupper network



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

To expose the backend service, create annotations of the backend deployment of the `east` Project:

    oc annotate deployment/hello-world-backend skupper.io/proxy="http"
    oc annotate deployment/hello-world-backend skupper.io/port="8080"

If you check the services in the OpenShift console of the `west` project, you should now see `hello-world-backend`.

## Step 5: Test your Skupper network

Create a route in the `west` Project from the `hello-world-frontend` service using either of the following methods:

* [Using the console](https://docs.openshift.com/container-platform/3.7/dev_guide/routes.html#creating-routes)
* Using the `oc` command:
    oc expose svc/hello-world-frontend --hostname=www.example.com


Test the resulting url, you should see output like this:

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

<div class="code-label session-1">East: Setup</div>

    oc new-project east
    oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/0.3/cmd/site-controller/deploy-watch-current-ns.yaml
    oc apply -f east-site.yaml
    oc apply -f west-secret.yaml
    oc create deployment --port 8080 hello-world-backend --image quay.io/skupper/hello-world-backend
    oc annotate deployment/hello-world-backend skupper.io/proxy="http"
    oc annotate deployment/hello-world-backend skupper.io/port="8080"

<div class="code-label session-2">West: Setup</div>

    oc new-project west
    oc apply -f https://raw.githubusercontent.com/skupperproject/skupper/0.3/cmd/site-controller/deploy-watch-current-ns.yaml
    oc apply -f west-site.yaml
    oc apply -f /home/pwright/token-request.yaml
    oc get secret  --export -o yaml west-secret > west-secret.yaml
    oc create deployment --port 8080 hello-world-backend --image quay.io/skupper/hello-world-frontend
    
     

## Next steps

Now that you know how to connect services running on multiple
clusters, here are a few more things to look at:

 - [Check out the HTTP Hello World example in more detail](https://github.com/skupperproject/skupper-example-hello-world)
 - [See how you can connect any TCP-based service](https://github.com/skupperproject/skupper-example-tcp-echo)
 - [Explore the examples]({{site_url}}/examples/index.html)
