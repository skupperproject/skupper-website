---
title: Skupper resources on Kubernetes
---
# Skupper resources on Kubernetes

The following sections describe the various Skupper resources on Kubernetes, for example, service accounts

## Service accounts, roles and role bindings

When you create a Skupper site, the following resources are created.

* **skupper-service-controller**\
A service account, role and role binding with this name are created to manage the Skupper service controller.
* **skupper-router**\
A service account, role and role binding with this name are created to manage the Skupper router.

## Deployments

Each Skupper site on Kubernetes consists of two deployments:

* **skupper-router**\
provides the data plane for the service network.
* **skupper-service-controller**\
provides the control plane for the service network.

## ConfigMaps

Do not edit these ConfigMap values directly.

* **skupper-site**\
site settings, including:

  * console authentication
  * ingress strategy

  This ConfigMap is the root object for all the skupper resources; deleting it will remove the Skupper deployment from the namespace.
* **skupper-services**\
internal representation of the services available on the service network.
* **skupper-internal**\
internal router configuration.
The service controller determines the values in this ConfigMap based on the services available on the service network.

## Secrets

Each site has two `kubernetes.io/tls` type secrets, **skupper-local-ca** and **skupper-site-ca**:

* **skupper-local-ca**\
issues certs for local access.

  The local certs are held in:

  * **skupper-local-client** used by the service controller.
  * **skupper-local-server** used by the router.
* **skupper-site-ca**\
issues certs for remote access.

  The site ca issued certs are **skupper-site-server** which holds the certs that identify the router to other routers that link to this site, **skupper-claims-server** which identifies the claims service, which is part of the service controller and is used when another site first established a link to exchange a restricted use token for a TLS certificate and **skupper-console-certs** which holds certs for the console.

The tokens used to establish links creates the following secrets with variable names:
+
* The site that issues a claim token generates a secret with a UUID name that contains details of any usage restrictions, for example, the number of times you can use the token to create a link and the amount of time the token is valid for.
* The site establishing the link will have a secret that contains the token claim or certificate.
These secrets are typically called `link1`, `link2`, and so on.

* **skupper-console-users**\
If you configure console authentication using the default `internal` mode, this secret is created and contains the username(s) and password(s) that can be used to access the console.
A username and password can be specified using `skupper init --console-user <username> --console-password <password>`.
If a username and password are not specified, an `admin` user is created with a generated password.

## Services

In addition to the services that are exposed on the service network, the following services are created:

* **skupper-router-local**\
The service controller uses this service to connect to and configure the router.
* **skupper-router**\
Other sites use this service to access the router over the inter-router or edge ports, although there may be other resources involved, for example, an ingress.
* **skupper**\
The console and claims-server are accessed through this service.
