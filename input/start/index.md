---
title: Getting started
---

# Getting started with Skupper

<nav class="toc">
  <a href="#prerequisites">Prerequisites</a>
  <a href="#step-1-install-the-skupper-command">Step 1: Install the Skupper command</a>
  <a href="#step-2-configure-access-to-multiple-namespaces">Step 2: Configure access to multiple namespaces</a>
  <a href="#step-3-establish-the-skupper-infrastructure-in-each-namespace">Step 3: Establish the Skupper infrastructure in each namespace</a>
  <a href="#step-4-connect-your-namespaces">Step 4: Connect your namespaces</a>
  <a href="#step-5-expose-your-services">Step 5: Expose your services</a>
  <a href="#the-condensed-version">The condensed version</a>
  <a href="#next-steps">Next steps</a>
</nav>

## Prerequisites

To get started with Skupper, you must have access to at least two
Kubernetes namespaces.  In the steps below, replace `<ns1>` and
`<ns2>` with your chosen namespaces.

Each namespace can reside on **any cluster you choose**, and **you are
not limited to two**.  You can have one on your laptop, another on
Amazon, another on Google, and so on.  For convenience, you can have
them all on one cluster.

Skupper works with any flavor of Kubernetes.  Here are some of your
options for setting up namespaces:

 - [Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/)
 - [Amazon EKS](https://aws.amazon.com/eks/getting-started/)
 - [Google GKE](https://cloud.google.com/kubernetes-engine/docs/quickstart)
 - [Microsoft AKS](https://docs.microsoft.com/en-us/azure/aks/intro-kubernetes)
 - [Red Hat OpenShift](https://www.openshift.com/learn/get-started/)

## Step 1: Install the Skupper command

The `skupper` command-line tool is the primary entrypoint for
installing and configuring the Skupper infrastructure.  You need to
install the `skupper` command only once for each development
environment.

### Download and extract the command

To get the latest release of the Skupper command for your platform,
download it from GitHub and extract the executable using `tar` or
`unzip`.

<div class="code-block-label">Linux</div>

    curl -fL https://github.com/skupperproject/skupper-cli/releases/download/{{skupper_cli_release}}/linux.tgz | tar -xzf -

<div class="code-block-label">macOS</div>

    curl -fL https://github.com/skupperproject/skupper-cli/releases/download/{{skupper_cli_release}}/darwin.zip -o skupper.zip
    unzip skupper.zip

This produces an executable file named `skupper` in your current
directory.

### Place the command on your path

The subsequent steps assume `skupper` is on your path.  As an
example, this is how you might install it in your home directory:

    mkdir -p ~/bin
    export PATH=$PATH:~/bin
    mv skupper ~/bin

### Check the command

To test your installation, run the `skupper` command with no
arguments.  You should see a usage summary.

    $ skupper
    Usage:
      skupper [command]

    Available Commands:
    [...]

## Step 2: Configure access to multiple namespaces

Skupper is designed for use with multiple namespaces, typically on
different clusters.  The `skupper` command uses your kubeconfig and
current context to select the namespace where it operates.

To avoid getting your wires crossed, you must use a distinct
kubeconfig or context for each namespace.  The easiest way is to use
separate console sessions.

### Configure separate console sessions

Start a console session for each of your namespaces.  Set the
`KUBECONFIG` environment variable to a different path in each session:

<div class="code-block-label">Console session for namespace 1</div>

    export KUBECONFIG=~/.kube/config-<ns1>

<div class="code-block-label">Console session for namespace 2</div>

    export KUBECONFIG=~/.kube/config-<ns2>

### Log in and set your namespaces

The methods for logging in and setting the current namespace are
specific to your Kubernetes provider.  See the following links for
more information:

 - [Vanilla Kubernetes (including Minikube)](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
 - [Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
 - [Google GKE](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl)
 - [Microsoft AKS](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#connect-to-the-cluster)
 - [Red Hat OpenShift](https://docs.openshift.com/container-platform/4.1/cli_reference/getting-started-cli.html#cli-logging-in_cli-developer-commands)

### Check your configurations

Once you have logged in, use the `skupper status` command to check
that each namespace is correctly configured.  You should see the
following output:

<div class="code-block-label">Namespace 1</div>

    $ skupper status
    Skupper is not installed in '<ns1>'.  Use 'skupper init' to install.

<div class="code-block-label">Namespace 2</div>

    $ skupper status
    Skupper is not installed in '<ns2>'.  Use 'skupper init' to install.

## Step 3: Establish the Skupper infrastructure in each namespace

The `skupper init` command installs the Skupper router, proxy, and
related resources in the current namespace.

    skupper init [--id <installation-name>]

### Install the infrastructure

Run `skupper init` once for each namespace you wish to connect.

<div class="code-block-label">Namespace 1</div>

    skupper init

<div class="code-block-label">Namespace 2</div>

    skupper init

You should see output like this:

    Skupper is now installed in '<ns>'.  Use 'skupper status' to get more information.

### Check the infrastructure

To check the status of each namespace, use the `skupper status`
command.

<div class="code-block-label">Namespace 1</div>

    $ skupper status
    Namespace '<ns1>' is ready.  It is connected to 0 other namespaces.

<div class="code-block-label">Namespace 2</div>

    $ skupper status
    Namespace '<ns2>' is ready.  It is connected to 0 other namespaces.

## Step 4: Connect your namespaces

After installation, you have the infrastructure you need, but your
namespaces are not connected.  Creating a connection requires use of
two `skupper` commands in conjunction:

    skupper connection-token <output-token-file>
    skupper connect <input-token-file>

The `skupper connection-token` command generates a secret token that
signifies permission to connect.  The token also carries the
connection details.  Anyone who has it can use the `skupper connect`
command to establish a connection from another namespace.

### Generate a connection token

Use the `skupper connection-token` command to generate a token.

<div class="code-block-label">Namespace 1</div>

    skupper connection-token ~/secret.yaml

### Use the token to form a connection

With the token in hand, you are ready to connect.  Pass the token from
namespace 1 to the `skupper connect` command in namespace 2.

<div class="code-block-label">Namespace 2</div>

    skupper connect ~/secret.yaml

### Check the connection

Use the `skupper status` command again to see if things have changed.
If the connection is made, you should see the following output:

<div class="code-block-label">Namespace 1</div>

    $ skupper status
    Namespace '<ns1>' is ready.  It is connected to 1 other namespace.

<div class="code-block-label">Namespace 2</div>

    $ skupper status
    Namespace '<ns2>' is ready.  It is connected to 1 other namespace.

## Step 5: Expose your services

You now have a network capable of multi-cluster communication, but no
services are attached to it.  This step uses the `kubectl annotate`
command to make a Kubernetes service on one namespace available on all
the connected namespaces.

    kubectl annotate <service> skupper.io/proxy=(http|tcp)

### Deploy your application

To demonstrate service exposure, we need an application to work with.
This guide uses an HTTP Hello World application with a backend and a
frontend.  Use `kubectl run` and `kubectl expose` to start the backend
on namespace 1 and create a service for it.

<div class="code-block-label">Namespace 1</div>

    kubectl run hello-world-backend --image quay.io/skupper/hello-world-backend --port 8080
    kubectl expose deployment/hello-world-backend

Use `kubectl run` to start the frontend on namespace 2.  Use `kubectl
expose` with `--type LoadBalancer` to make the frontend externally
accessible.

<div class="code-block-label">Namespace 2</div>

    kubectl run hello-world-frontend --image quay.io/skupper/hello-world-frontend --port 8080
    kubectl expose deployment/hello-world-frontend --type LoadBalancer

### Expose the service

Use the `kubectl annotate` command on namespace 1 to make
`hello-world-backend` available on namespace 2.

<div class="code-block-label">Namespace 1</div>

    kubectl annotate service/hello-world-backend skupper.io/proxy=http

### Check the service

Use `kubectl get services` on namespace 2 to make sure the
`hello-world-backend` service from namespace 1 is represented.  You
should see output like this:

<div class="code-block-label">Namespace 2</div>

    $ kubectl get services
    NAME                   TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)          AGE
    [...]
    hello-world-backend    ClusterIP      10.106.92.175    <none>           8080/TCP         11h
    hello-world-frontend   LoadBalancer   10.111.133.137   10.111.133.137   8080:31313/TCP   6m31s
    [...]

Note: If you are using Minikube and the external IP shows `<pending>`,
you need to use the `minikube tunnel` command to provide ingress.

### Test your application

Now your multi-cluster application is up and running.  Use `curl` to
see it in action.

<div class="code-block-label">Namespace 2</div>

    curl $(kubectl get service/hello-world-frontend -o jsonpath='http://{.status.loadBalancer.ingress[0].ip}:{.spec.ports[0].port}/')

You should see output like this:

    I am the frontend.  The backend says 'Hello 1'.

## The condensed version

<div class="code-block-label">Skupper command installation</div>

    curl -fL https://github.com/skupperproject/skupper-cli/releases/download/{{skupper_cli_release}}/linux.tgz | tar -xzf -

<div class="code-block-label">Namespace 1</div>

    export KUBECONFIG=~/.kube/config-<ns1>
    <provider-login-command>
    skupper init
    skupper connection-token ~/secret.yaml
    kubectl run hello-world-backend --image quay.io/skupper/hello-world-backend --port 8080
    kubectl expose deployment/hello-world-backend
    kubectl annotate deployment/hello-world-backend skupper.io/proxy=http

<div class="code-block-label">Namespace 2</div>

    export KUBECONFIG=~/.kube/config-<ns2>
    <provider-login-command>
    skupper init
    skupper connect ~/secret.yaml
    kubectl run hello-world-frontend --image quay.io/skupper/hello-world-frontend --port 8080
    kubectl expose deployment/hello-world-frontend --type LoadBalancer
    curl $(kubectl get service/hello-world-frontend -o jsonpath='http://{.status.loadBalancer.ingress[0].ip}:{.spec.ports[0].port}/')

## Next steps

Now that you know how to connect services running on multiple
clusters, here are a few more things to look at:

 - [Use and modify the HTTP Hello World example](https://github.com/skupperproject/skupper-example-hello-world)
 - [See how you can connect any TCP-based service](https://github.com/skupperproject/skupper-example-tcp-echo)
 - [Explore the examples]({{site_url}}/examples/index.html)
