---
title: Security
---

# Skupper security

The Skupper network is secured through mutual tls, with each router
deployment uniquely identified by its own certificate.  The proxies
also use mutual TLS with the routers in the network they are connected
to.

One option is to use end-to-end authentication between application
clients and servers.

## TLS from router to router

The Skupper network is secured through mutual tls, with each router
deployment uniquely identified by its own certificate.

XXX

## TLS from clients to routers

Could use openshift service certificates for proxy. Clients would then
automatically have the CA made available to them. Application would
still need to enable TLS, i.e. not completely transparent. Also only
available on openshift.

The deployer could also generate a certificate for each proxy and
place the CA certificate with which it could be verified in a secret
linked to the service in some way. Alternatively the CA key and cert
could be passed into the deployer.

## TLS from routers to clients

Have application give the secret to use for credentials in the service
definition? Or else allow application to be configured with
credentials it uses? Former seems more workable.

These approaches could even allow mutual tls between the application
and proxies. (Though with the application having to be concerned with
managing credentials and using them on both client and
server. I.e. this can be a way of retaining the benefits of mutual tls
from direct communication when moving to intermediated
communication. That is a separate case, but possibly still a useful
one, from the objective of trying to absolve the application from
needing to be directly concerned with security).

## Access control and resource limits

XXX

## Access from external clients

The second case to consider is access from external clients. This will
require an 'ingress proxy'. The proxy could be enhanced to allow it to
be configured to do authentication, remove the need for the
application itself to handle this.

## More information

 - [Skupper overview](overview.html)
 - [Skupper connectivity](connectivity.html)
 - [Skupper routing](routing.html)
