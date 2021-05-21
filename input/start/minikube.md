# Using Skupper with Minikube

## Prerequisites

* You must [install Minikube and start a cluster][gs].

* You must have a version of `kubectl` compatible with your Minikube
  Kubernetes version.  You can also use the [`kubectl` built in to
  Minikube][kubectl].

[gs]: https://minikube.sigs.k8s.io/docs/start/
[kubectl]: https://minikube.sigs.k8s.io/docs/handbook/kubectl/

## Logging in

Minikube does not offer a dedicated login command, but you can re-run
the `minikube start` command in each console session you wish to
configure.  This initializes the required kubeconfigs in each case.

<div class="code-label session-2">Console for West</div>

    export KUBECONFIG=$HOME/.kube/config-west
    minikube start

<div class="code-label session-1">Console for East</div>

    export KUBECONFIG=$HOME/.kube/config-east
    minikube start

## Running minikube tunnel

Skupper requires IP connectivity to at least one cluster in order to
form links between clusters.  If you are using Minikube to test
Skupper, one of your Minikube clusters must have external network
access.  To enable network access, run `minikube tunnel` in the
background after running `minikube start`.

Make sure you run `minikube tunnel` with the same kubeconfig and
Minikube profile you used for `minikube start`.  In the Hello World
example, the tunnel is required only for the cluster containing the
West namespace.

    export KUBECONFIG=$HOME/.kube/config-west
    minikube tunnel

The tunnel must run continuously while you are using it, so you will
likely want to run it in its own console session, separate from the
console you use to interact with the West namespace.

See [Using minikube tunnel][tunnel] for more information.

[tunnel]: https://minikube.sigs.k8s.io/docs/handbook/accessing/#using-minikube-tunnel

## More information

* [Minikube website](https://minikube.sigs.k8s.io/community/)
* [Minikube documentation](https://minikube.sigs.k8s.io/docs/)
