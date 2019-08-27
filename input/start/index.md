---
title: Getting started
---

# Getting started with Skupper

<nav class="toc">
  <a href="#prerequisites">Prerequisites</a>
  <a href="#step-1-install-the-skupper-command">Step 1: Install the <code>skupper</code> command</a>
  <a href="#step-2-initialize-your-namespaces">Step 2: Initialize your namespaces</a>
  <a href="#step-3-connect-your-namespaces">Step 3: Connect your namespaces</a>
  <a href="#step-4-access-your-services">Step 4: Access your services</a>
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
platform: Extract the executable using tar or unzip.  Put the binary
on your path.  (You only need to do this once for each new developer
environment.)

On Linux:

    $ curl -fL https://github.com/skupperproject/skupper-cli/releases/download/dummy/linux.tgz -o skupper.tgz
    $ tar -xf skupper.tgz --directory ~/bin

On Mac:

    $ curl -fL https://github.com/skupperproject/skupper-cli/releases/download/dummy/darwin.zip -o skupper.zip
    $ unzip skupper.zip -d ~/bin
    $ cd ~/bin && ln -s release/darwin/skupper

To test your installation, run the `skupper` command with no
arguments.  If it's working, it will print a usage summary.

    $ skupper
    usage: skupper <command> <args>
    [...]

## Step 2: Initialize your namespaces

The `skupper init` command establishes the Skupper infrastructure in a
target namespace.

    $ skupper --context <ns1> init --auto-expose
    Skupper is now installed in '<ns1>'.  See 'skupper --context <ns1> status' for more information.
    $ skupper --context <ns2> init
    Skupper is now installed in '<ns2>'.  See 'skupper --context <ns2> status' for more information.

To check the status of each namespace, use the `skupper status`
command:

    $ skupper --context <ns1> status
    Namespace '<ns1>' is ready.  It is connected to 0 other namespaces.
    $ skupper --context <ns2> status
    Namespace '<ns2>' is ready.  It is connected to 0 other namespaces.

;;The `--hub` option sets up Skupper on that namespace to accept connections from other namespaces.

## Step 3: Connect your namespaces

After initialization, we have the infrastructure we need, but nothing
is connected.  To securely form a connection between namespaces, we
first need a secret that signifies permission to connect.  Use the
`skupper secret` command to generate a secret for another namespace:

    $ skupper --context <ns1> secret ~/secret.yaml

With the secret in hand, we're ready to connect.  Pass the secret to
the `skupper connect` command:

    $ skupper --context <ns2> connect ~/secret.yaml

Let's see if the status has changed.  If the connection is made, you
should see the following:

    $ skupper --context <ns1> status
    Namespace '<ns1>' is ready.  It is connected to 1 other namespace.
    $ skupper --context <ns2> status
    Namespace '<ns2>' is ready.  It is connected to 1 other namespace.

## Step 4: Access your services

Now we are ready to communicate across clusters.

    $ kubectl --context <ns1> run hello-world-backend --image quay.io/skupper/hello-world-backend
    deployment.apps/hello-world created
    $ kubectl --context <ns2> run hello-world-frontend --image quay.io/skupper/hello-world-frontend
    $ [...]

## The condensed version

Namespace 1:

    $ skupper -c <ns1> init --auto-expose
    $ skupper -c <ns1> secret ~/secret.yaml
    $ skupper -c

Namespace 2:

    $ skupper -c <ns2> init
    $ skupper -c <ns2> connect ~/secret.yaml

## Next steps

[...]
