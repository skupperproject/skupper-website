# Using Skupper with Google Kubernetes Engine (GKE)

## Prerequisites

* You must have [access to a GKE cluster][overview].
* You must [install and set up the Google Cloud SDK (`gcloud`)][installation].

[overview]: https://cloud.google.com/kubernetes-engine
[installation]: https://cloud.google.com/sdk/docs/install

## Cluster access

Use the `gcloud` command and the Google Cloud console to log in:

1. Go to [console.cloud.google.com](https://console.cloud.google.com/) and sign in.
1. Select **Kubernetes Engine** in the menu on the left.
1. Navigate to your cluster.
1. Select the **Connect** link at the top of the page.
1. Copy the provided `gcloud` command.
1. Paste the `gcloud` command into your console session.

See [Configuring cluster access for kubectl][cluster-access] for more
information.

[cluster-access]: https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl

## Enabling outbound connections

By default, private GKE clusters do not allow outbound connections to
external IP addresses.  To link a private GKE cluster to a remote site
with Skupper, you need to [enable outbound connections using Cloud
NAT][nat-gke].

See the [Cloud NAT overview][nat-overview] for more information.

[nat-gke]: https://cloud.google.com/nat/docs/gke-example
[nat-overview]: https://cloud.google.com/nat/docs/overview

## More information

* [Google Cloud SDK getting started guide](https://cloud.google.com/sdk/docs/quickstart)
* [Google GKE website](https://cloud.google.com/kubernetes-engine)
* [Google GKE documentation](https://cloud.google.com/kubernetes-engine/docs)
