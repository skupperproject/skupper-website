# Using Skupper with Minikube

## Prerequisites

See [Getting started with
Minikube](https://minikube.sigs.k8s.io/docs/start) for `minikube`
installation instructions.

The examples require `minikube` version 1.17.1 or greater.

Ensure that the version of `kubectl` is compatible with your
`minikube` installation.  See [Using Kubectl with
Minikube](https://minikube.sigs.k8s.io/docs/handbook/kubectl).

## Logging in

Minikube does not offer a dedicated login command, but you can re-run
the `minikube start` command in each console you wish to configure.

<div class="code-label session-2">Console for West</div>

    export KUBECONFIG=$HOME/.kube/config-west
    minikube start

<div class="code-label session-1">Console for East</div>

    export KUBECONFIG=$HOME/.kube/config-east
    minikube start

## Minikube tunnel

Skupper requires cluster-external network access in order to form
connections between clusters.  To enable network access run `minikube
tunnel` in the background after running `minikube start`.

In the Hello World example, the tunnel is required only for the
cluster containing the West namespace:

<div class="code-label session-2">Console for West</div>

    minikube tunnel &

Make sure you run `minikube tunnel` with the same kubeconfig and
Minikube profile you used for `minikube start`.

## More information

* [Installing Kubernetes with Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/)
* [Getting started with Minikube on Linux](https://opensource.com/article/18/10/getting-started-minikube)
* [Getting started with Kubernetes](https://kubernetes.io/docs/setup)
