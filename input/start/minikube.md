# Using Skupper with Minikube

## Prerequisites

Skupper requires cluster-external network access in order to form
connections between clusters.  Run `minikube tunnel` in the background
to enable this access.

    minikube tunnel

## Logging in

Minikube does not offer a dedicated login command, but you can re-run
the `minikube start` command in each console you wish to configure.

<div class="code-label session-1">Console for US East</div>

    export KUBECONFIG=$HOME/.kube/config-us-east
    minikube start

<div class="code-label session-2">Console for EU North</div>

    export KUBECONFIG=$HOME/.kube/config-eu-north
    minikube start

## More information

* [Installing Kubernetes with Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/)
* [Getting started with Minikube on Linux](https://opensource.com/article/18/10/getting-started-minikube)
* [Getting started with Kubernetes](https://kubernetes.io/docs/setup/)
