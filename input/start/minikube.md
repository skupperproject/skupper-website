# Using Skupper with Minikube

## Prerequisites

Skupper requires external network access in order to form connections
between clusters.  Make sure you have `minikube tunnel` running in the
background when using Skupper so that those connections are possible.

    minikube tunnel

## Logging in

Minikube does not offer a dedicated login command, but you can re-run
the `minikube start` command in each console you wish to configure.

<div class="code-label session-1">Console session for US East</div>

    export KUBECONFIG=$HOME/.kube/config-us-east
    minikube start

<div class="code-label session-2">Console session for EU North</div>

    export KUBECONFIG=$HOME/.kube/config-eu-north
    minikube start

<!-- ## More information -->

<!-- <ul class="column-list"> -->
<!--   <li><a href="https://kubernetes.io/docs/setup/learning-environment/minikube/">Minikube</a></li> -->
  <!-- <li><a href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">Vanilla Kubernetes (including Minikube)</a></li> -->
<!-- </ul> -->
