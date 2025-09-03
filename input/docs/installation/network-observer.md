# Installing the Skupper Network Observer

The Network console provides data and visualizations of the traffic
flow between sites.

#### Prerequisites

- A Kubernetes site

#### Procedure

1. Determine which site in your network is best to enable the Network
   console using the following criteria:

   - Does the application network cross a firewall? For example, if
     you want the console to be available only inside the firewall,
     you need to locate the Network console on a site inside the
     firewall.
   - Is there a site that processes more traffic than other sites? For
     example, if you have a frontend component that calls a set of
     services from other sites, it might make sense to locate the
     Network console on that site to minimize data traffic.
   - Is there a site with more or cheaper resources that you want to
     use? For example, if you have two sites, A and B, and resources
     are more expensive on site A, you might want to locate the
     Network console on site B.

1. Change context to a site namespace.

1. Deploy the network observer helm chart:
   ~~~
   helm install skupper-network-observer oci://quay.io/skupper/helm/network-observer --version {{skupper_version}}
   ~~~

   The output is similar to the following:
   ~~~
   Pulled: quay.io/skupper/helm/network-observer:2.0.0
   Digest: sha256:557c8a3f4b5d8bb6e779a81e6214fa87c2ad3ad0c957a5c08b8dd3cb20fc7cfe
   NAME: skupper-network-observer
   LAST DEPLOYED: Sun Mar  9 19:47:09 2025
   NAMESPACE: default
   STATUS: deployed
   REVISION: 1
   TEST SUITE: None
   NOTES:
   You have installed the skupper network observer!

   Accessing the console:
   The network-observer application is exposed as a service inside of your
   cluster. To access the application externally you must either enable an
   ingress of some sort or use port forwarding to access the service
   temporarily.
   Expose the application at https://127.0.0.1:8443 with the command:
   kubectl --namespace default port-forward service/skupper-network-observer 8443:443

   Basic Authentication is enabled.

   Users are configured in the skupper-network-observer-auth secret.
   This secret has been prepopulated with a single user "skupper" and a randomly
   generated password stored in plaintext. It is recommended that these
   credentials be rotated and replaced with a secure password hash (bcrypt.)

   Retrieve the password with this command:
   kubectl --namespace default \
         get secret skupper-network-observer-auth \
         -o jsonpath='{.data.htpasswd}' | base64 -d | sed 's/\(.*\):{PLAIN}\(.*\)/\1 \2\n/'
   ~~~
1. Expose the `skupper-network-observer` service to make the Network
   console available, for example on OpenShift:

   ~~~
   oc expose skupper-network-observer
   ~~~

## Skupper Network Observer

The skupper network observer is an application that attaches to the skupper
network in order to expose skupper network telemetry. When installed alongside
a skupper site it will collect operational data from ALL sites in the network
and expose them via the API and metrics that back the [Skupper
Console](https://github.com/skupperproject/skupper-console) web application.

This chart bootstraps a skupper network observer deployment on a
[Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh)
package manager.

### Prerequisites

- A Skupper Version 2 Site running in the same Kubernetes Namespace the network
observer is to be installed in.
- The Skupper Controller running and managing the Site.

### Usage

To deploy the Skupper Network Observer to a namespace using Helm

~~~
helm install skupper-network-observer oci://quay.io/skupper/helm/network-observer
~~~

### Non-Helm Usage with preconfigured manifest yaml

Without Helm, the Skupper Network Observer can be installed using one of the manifests generated from the chart published alongside a Skupper release.

**skupper-network-observer.yaml**

The most basic Skupper Network Observer deployment. Exposes the console and API as a ClusterIP Service in the namespace without authentication.

~~~
kubectl apply -f skupper-network-observer.yaml; # install the network observer
kubectl port-forward services/skupper-network-observer 8443:443 # access the service at https://localhost:8443 via kube-proxy
~~~

**skupper-network-observer-httpbasic.yaml**

Similar to skupper-network-observer.yaml, but secured with http basic auth. Requires additional action to add authenticated users.

~~~
kubectl apply -f skupper-network-observer-httpbasic.yaml;
# Create a htpasswd file with user provided credentials
htpasswd -c /tmp/htpasswd my-user;
# Update the secret containing the authenticated users and hashed credentials
kubectl patch secret skupper-network-observer-auth \
  -p '{"data":{"htpasswd":"'$(base64 -w0 /tmp/htpasswd)'"}}';

# access the service at https://localhost:8443 via kube-proxy
# should be prompted for http basic auth.
kubectl port-forward services/skupper-network-observer 8443:443
~~~

**skupper-network-observer-openshift.yaml**

An OpenShift ready deployment manifest accessible by route.

### Configuration

By default, deploys the network-observer with skupper-issued TLS certificates,
no ingress, and HTTP Basic authentication with a randomly generated
credentials.

#### Ingress

By default the network-observer does not include an ingress. As a convenience,
the chart contains options that can help expose the service externally.

- Configure an ingress by setting `ingress.enabled=true` and setting appropriate
values under `ingress`.

Example values.yaml using the nginx ingress nginx controller with a
user-provided TLS certificate

~~~
ingress:
  enabled: true
  className: "nginx"
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "https"
  hosts:
    - host:  skupper-net-01.mycluster.local
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: skupper-net-01-tls
      hosts:
        - skupper-net-01.mycluster.local
~~~

- Configure an OpenShift route by setting `route.enabled=true`.
- Expose the service as type LoadBalancer `service.type=LoadBalancer`.

#### TLS

TLS is mandatory for this deployment. It can be configured as user provided, provided
by OpenShift or by the skupper controller.

To use an existing TLS secret, overwrite `tls.secretName`.

To use an OpenShift generated service certificate, set
`tls.openshiftIssued=true` and `tls.skupperIssued=false`. An annotation will be
added to the service that should prompt OpenShift to provision a TLS secret.

#### Authentication

The network observer pod contains a reverse proxy that handles authentication
and TLS termination for the read only application that binds only to localhost.
When authentication strategy is "basic", nginx is configured as the proxy, and
can be configured with user-provided htpasswd file contents or a secret name.
When authentication strategy is "openshift" an oauth2 proxy is used instead, and
is configured to use the cluster identity provider for authentication. OpenShift
auth only works with ingress type Route.

To set a secure basic auth credentials run:

~~~
# Use htpasswd to generate a new password file
htpasswd -B -c passwords \
    my-username;

# Add a new secret with that password file
kubectl create secret generic my-custom-auth \
    --from-file=htpasswd=passwords;

# Point the chart at the new secret
helm install ... \
    --set auth.basic.create=false \
    --set auth.basic.secretName=my-custom-auth

# Rotate the credentials with a new htpasswd file by patching
# the existing secret with updated credentials in ./passwords
kubectl patch secrets \
    my-custom-auth -p '{"data":{"htpasswd":"'$(base64 -w0 ./passwords)'"}}'

~~~
