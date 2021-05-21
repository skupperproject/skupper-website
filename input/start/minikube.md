# Using Skupper with Minikube

## Developer tools

The `minikube` command-line tool allows you to create and operate
local Kubernetes clusters.

See the [Minikube getting started guide][gs] for more information.

[gs]: https://minikube.sigs.k8s.io/docs/start/

## Logging in

Minikube does not offer a dedicated login command, but you can re-run
the `minikube start` command in each console session you wish to
configure.

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

The tunnel must run continuously while you are using it, so you will
likely want to run it in its own console session.

See [Using minikube tunnel][tunnel] for more information.

[tunnel]: https://minikube.sigs.k8s.io/docs/handbook/accessing/#using-minikube-tunnel

## More information

* [Minikube website](https://minikube.sigs.k8s.io/community/)
* [Minikube documentation](https://minikube.sigs.k8s.io/docs/)
