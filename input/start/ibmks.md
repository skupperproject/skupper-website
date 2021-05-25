# Using Skupper with IBM Kubernetes Service

## Prerequisites

* You must have [access to an IBM Kubernetes Service cluster][start].
* You must [install the IBM Cloud CLI][install].
* You must [install the `container-service` plugin][plugin]

[start]: https://www.ibm.com/cloud/kubernetes-service
[install]: https://cloud.ibm.com/docs/cli?topic=cli-install-ibmcloud-cli
[plugin]: https://cloud.ibm.com/docs/containers?topic=containers-cs_cli_install#cs_cli_install_steps

## Logging in

### Logging in using the command line

Use the `ibmcloud login` command:

    $ ibmcloud login

It will prompt you for required credentials.

### Logging in using the console

Use the `ibmcloud` command and the IBM Cloud console to log in:

1. Go to [cloud.ibm.com](https://cloud.ibm.com/) and sign in.
1. Select **Kubernetes** in the menu on the left.
1. Navigate to your cluster.
1. Select **Actions** &gt; **Connect via CLI**.
1. Copy the provided `ibmcloud login` command and paste it into your console session.
1. Copy the provided `ibmcloud ks cluster config` command and paste it into your console session.

## Incoming site links

Clusters in the free tier do not support load balancers.  As a result,
they cannot accept incoming connections.  Since by default Skupper
attempts to set up an ingress for accepting incoming site links, this
causes `skupper init` to fail.

To avoid this, use the `--ingress none` option:

    skupper init --ingress none

The non-free clusters do not have this limitation.

## More information

* [IBM Kubernetes Service website](https://www.ibm.com/cloud/kubernetes-service)
* [IBM Kubernetes Service documentation](https://cloud.ibm.com/docs/containers)
