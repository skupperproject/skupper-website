# Using Skupper with Azure Kubernetes Service (AKS)

## Prerequisites

* You must have [access to an AKS cluster][overview].
* You must [install and set up the Azure CLI (`az`)][installation].

[overview]: https://azure.microsoft.com/en-us/services/kubernetes-service/#overview
[installation]: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

## Cluster access

Use the `az` command and the Azure Portal to log in:

1. Go to [portal.azure.com](https://portal.azure.com/)
1. Select **Kubernetes services**.
1. Navigate to your cluster.
1. Select **Connect**.
1. Copy the provided `az` commands into your console session.

See [Connect to the cluster][cluster-access] for more information.

[cluster-access]: https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough#connect-to-the-cluster

## More information

* [Azure CLI getting started guide](https://docs.microsoft.com/en-us/cli/azure/get-started-with-azure-cli)
* [Azure AKS website](https://azure.microsoft.com/en-us/services/kubernetes-service/#overview)
* [Azure AKS documentation](https://docs.microsoft.com/en-us/azure/aks/)
