---
title: Getting started
---

# Getting started with Skupper

<nav class="toc">
  <a href="#prerequisites">Prerequisites</a>
  <a href="#step-1-install-the-skupper-command">Step 1: Install the <code>skupper</code> command</a>
  <a href="#step-2-configure-access-to-multiple-namespaces">Step 2: Configure access to multiple namespaces</a>
  <a href="#step-3-initialize-your-namespaces">Step 3: Initialize your namespaces</a>
  <a href="#step-4-connect-your-namespaces">Step 4: Connect your namespaces</a>
  <a href="#step-5-expose-and-access-your-services">Step 5: Expose and access your services</a>
  <a href="#the-condensed-version">The condensed version</a>
  <a href="#next-steps">Next steps</a>
</nav>

## Prerequisites

To get started with Skupper, you must have access to at least two
Kubernetes namespaces.  Each namespace can be on any cluster you
choose.  (For convenience, you can put them all on one cluster.)  In
the steps below, replace `<ns1>` and `<ns2>` with your chosen
namespaces.

;; https://kubernetes.io/docs/tasks/tools/install-minikube/

## Step 1: Install the `skupper` command

Get the latest release of the Skupper command-line tool for your
platform.  Extract the executable using tar or unzip and put it on
your path:

On Linux:

    $ curl -fL https://github.com/skupperproject/skupper-cli/releases/download/dummy2/linux.tgz -o skupper.tgz
    $ tar -xf skupper.tgz --directory $HOME/bin
    $ export PATH=$PATH:$HOME/bin

On Mac:

    $ curl -fL https://github.com/skupperproject/skupper-cli/releases/download/dummy2/darwin.zip -o skupper.zip
    $ unzip skupper.zip -d $HOME/bin
    $ cd ~/bin && ln -s release/darwin/skupper
    $ export PATH=$PATH:$HOME/bin

To test your installation, run the `skupper` command with no
arguments.  If it's working, it will print a usage summary.

    $ skupper
    usage: skupper <command> <args>
    [...]

You only need to install the Skupper command once for each new
developer environment.

## Step 2: Configure access to multiple namespaces

You will be working with multiple namespaces, typically on distinct
clusters.  To avoid getting your wires crossed, you must set your
development environment to operate with a distinct configuration for
each namespace.  The easiest way is to use separate console sessions:

<p class="code-block-label">Console session for namespace 1</p>

    $ export KUBECONFIG=$HOME/.kube/config-<ns1>
    $ <provider-login-command>

<p class="code-block-label">Console session for namespace 2</p>

    $ export KUBECONFIG=$HOME/.kube/config-<ns2>
    $ <provider-login-command>

The methods for logging in and setting the active namespace are
specific to your Kubernetes provider.  See the following links for
more information:

 - Amazon EKS
 - Google GKE
 - Red Hat OpenShift
 - [Vanilla Kubernetes](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)

## Step 3: Initialize your namespaces

The `skupper init` command establishes the Skupper infrastructure in the
current namespace.

<p class="code-block-label">Namespace 1</p>

    $ skupper init
    Skupper is now installed in '<ns1>'.  Use 'skupper status' to get more information.

<p class="code-block-label">Namespace 2</p>

    $ skupper init
    Skupper is now installed in '<ns2>'.  Use 'skupper status' to get more information.

To check the status of each namespace, use the `skupper status`
command:

<p class="code-block-label">Namespace 1</p>

    $ skupper status
    Namespace '<ns1>' is ready.  It is connected to 0 other namespaces.

<p class="code-block-label">Namespace 2</p>

    $ skupper status
    Namespace '<ns2>' is ready.  It is connected to 0 other namespaces.

## Step 4: Connect your namespaces

After initialization, we have the infrastructure we need, but nothing
is connected.  To securely form a connection between namespaces, we
first need a secret that signifies permission to connect.  Use the
`skupper secret` command to generate a secret for another namespace:

<p class="code-block-label">Namespace 1</p>

    $ skupper secret ~/secret.yaml

With the secret in hand, we're ready to connect.  Pass the secret from
namespace 1 to the `skupper connect` command in namespace 2:

<p class="code-block-label">Namespace 2</p>

    $ skupper connect ~/secret.yaml

Let's see if the status has changed.  If the connection is made, you
should see the following:

<p class="code-block-label">Namespace 1</p>

    $ skupper status
    Namespace '<ns1>' is ready.  It is connected to 1 other namespace.

<p class="code-block-label">Namespace 2</p>

    $ skupper status
    Namespace '<ns2>' is ready.  It is connected to 1 other namespace.

You can connect as many namespaces as you wish.  Once a namespace is
connected, it can access services on any other connected namespace.

## Step 5: Expose and access your services

We now have a network for cross-cluster communication, but our
services are not yet exposed on the network.  Use the `skupper expose`
command to make a Kubernetes service or deployment available on the
network:

    $ skupper expose (<service>|<deployment>) --protocol (http|tcp)

For example, here are the commands for a simple HTTP hello world
application with a frontend and a backend:

<p class="code-block-label">Namespace 1</p>

    $ kubectl run hello-backend --image quay.io/skupper/hello-backend
    deployment.apps/hello-backend created
    $ skupper expose hello-backend --protocol http

<p class="code-block-label">Namespace 2</p>

    $ kubectl run hello-frontend --image quay.io/skupper/hello-frontend
    deployment.apps/hello-frontend created
    $ curl <hello-frontend-url>
    Hello from hello-backend!

## The condensed version

<p class="code-block-label">Namespace 1</p>

    $ export KUBECONFIG=~/.kube/config-<ns1>
    $ skupper secret ~/secret.yaml
    $ kubectl run hello-backend --image quay.io/skupper/hello-backend
    $ skupper expose hello-backend --protocol http

<p class="code-block-label">Namespace 2</p>

    $ export KUBECONFIG=~/.kube/config-<ns2>
    $ skupper init
    $ skupper connect ~/secret.yaml
    $ kubectl run hello-frontend --image quay.io/skupper/hello-frontend
    $ curl <hello-frontend-url>
    Hello from hello-backend!

## Next steps

[...]
