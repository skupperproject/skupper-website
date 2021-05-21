# Using Skupper with Minikube

## Logging in

Minikube does not offer a dedicated login command, but you can re-run
the `minikube start` command in each console you wish to configure.

<div class="code-label session-2">Console for West</div>

    export KUBECONFIG=$HOME/.kube/config-west
    minikube start

<div class="code-label session-1">Console for East</div>

    export KUBECONFIG=$HOME/.kube/config-east
    minikube start

## Running minikube tunnel

Skupper requires cluster-external network access in order to form
links between clusters.  Run `minikube tunnel` in the background
to enable this access.

Make sure you run `minikube tunnel` with the same kubeconfig and
Minikube profile you used for `minikube start`.  In the Hello World
example, the tunnel is required only for the cluster containing the
West namespace.

    export KUBECONFIG=$HOME/.kube/config-west
    minikube tunnel

## More information

* [Installing Kubernetes with Minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/)
* [Getting started with Minikube on Linux](https://opensource.com/article/18/10/getting-started-minikube)
* [Getting started with Kubernetes](https://kubernetes.io/docs/setup/)
