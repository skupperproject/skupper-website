---
title: Getting started
---

# Getting started with Skupper

<nav class="toc">
  <a href="#prerequisites">Prerequisites</a>
  <a href="#step-1-install-the-skupper-command">Step 1: Install the <code>skupper</code> command</a>
  <a href="#step-2-initialize-your-namespaces">Step 2: Initialize your namespaces</a>
  <a href="#step-3-connect-your-namespaces">Step 3: Connect your namespaces</a>
  <a href="#step-4-expose-and-access-your-services">Step 4: Expose and access your services</a>
  <a href="#the-condensed-version">The condensed version</a>
  <a href="#next-steps">Next steps</a>
</nav>

## Prerequisites

To get started with Skupper, you must have access to at least two
Kubernetes namespaces.  Each namespace can be on any cluster you
choose.  (For convenience, you can put them all on one cluster.)  In
the steps below, replace `<ns1>` and `<ns2>` with your chosen
namespaces.

## Step 1: Install the `skupper` command

Get the latest release of the Skupper command-line tool for your
platform.  Extract the executable using tar or unzip and put it on
your path:

On Linux:

    $ curl -fL https://github.com/skupperproject/skupper-cli/releases/download/dummy/linux.tgz -o skupper.tgz
    $ tar -xf skupper.tgz --directory $HOME/bin
    $ export PATH=$PATH:$HOME/bin

On Mac:

    $ curl -fL https://github.com/skupperproject/skupper-cli/releases/download/dummy/darwin.zip -o skupper.zip
    $ unzip skupper.zip -d $HOME/bin
    $ cd ~/bin && ln -s release/darwin/skupper
    $ export PATH=$PATH:$HOME/bin

To test your installation, run the `skupper` command with no
arguments.  If it's working, it will print a usage summary.

    $ skupper
    usage: skupper <command> <args>
    [...]

You only need to do install the Skupper command once for each new
developer environment.

## Step 2: Initialize your namespaces

The `skupper init` command establishes the Skupper infrastructure in the
current namespace.

Namespace 1:

    $ export KUBECONFIG=XXX
    $ skupper init
    Skupper is now installed in '<ns1>'.  Use 'skupper status' to get more information.

Namespace 2:

    $ export KUBECONFIG=XXX
    $ skupper init
    Skupper is now installed in '<ns2>'.  Use 'skupper status' to get more information.

To check the status of each namespace, use the `skupper status`
command:

Namespace 1:

    $ skupper status
    Namespace '<ns1>' is ready.  It is connected to 0 other namespaces.

Namespace 2:

    $ skupper status
    Namespace '<ns2>' is ready.  It is connected to 0 other namespaces.

## Step 3: Connect your namespaces

After initialization, we have the infrastructure we need, but nothing
is connected.  To securely form a connection between namespaces, we
first need a secret that signifies permission to connect.  Use the
`skupper secret` command to generate a secret for another namespace:

Namespace 1:

    $ skupper secret ~/secret.yaml

With the secret in hand, we're ready to connect.  Pass the secret from
namespace 1 to the `skupper connect` command in namespace 2:

Namespace 2:

    $ skupper connect ~/secret.yaml

Let's see if the status has changed.  If the connection is made, you
should see the following:

Namespace 1:

    $ skupper status
    Namespace '<ns1>' is ready.  It is connected to 1 other namespace.

Namespace 2:

    $ skupper status
    Namespace '<ns2>' is ready.  It is connected to 1 other namespace.

## Step 4: Expose and access your services

We now have a network for cross-cluster communication, but our
services are not yet available there.  Use the `skupper expose`
command to ... .

Now we are ready to communicate across clusters.

Here we are using a simple hello world application with a frontend and
a backend.

Namespace 1:

    $ kubectl run hello-backend --image quay.io/skupper/hello-backend
    deployment.apps/hello-backend created
    $ skupper expose hello-backend --protocol http

Namespace 2:

    $ kubectl run hello-frontend --image quay.io/skupper/hello-frontend
    deployment.apps/hello-frontend created
    $ curl <hello-frontend-url>
    Hello from hello-backend!

## The condensed version

Namespace 1:

    $ export KUBECONFIG=XXX
    $ skupper init
    $ skupper secret ~/secret.yaml
    $ kubectl run hello-backend --image quay.io/skupper/hello-backend
    $ skupper expose hello-backend --protocol http

Namespace 2:

    $ export KUBECONFIG=XXX
    $ skupper init
    $ skupper connect ~/secret.yaml
    $ kubectl run hello-frontend --image quay.io/skupper/hello-frontend
    $ curl <hello-frontend-url>

## Next steps

[...]
