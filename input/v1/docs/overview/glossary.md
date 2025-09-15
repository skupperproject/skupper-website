---
title: Glossary
---
# Glossary

An explanation of common terms used with Skupper.

* **service network**\
A network of Skupper sites linked together to share services.
* **service**\
In Skupper, the Kubernetes [service](https://kubernetes.io/docs/concepts/services-networking/service/)  concept is extended to  allow communication with sites outside the cluster.
When you define a service using Skupper, that service appears as a native service in other sites.
* **site**\
A Skupper site is an Skupper installation.
You _link_ sites to form a service network and share services. You can create sites in a Kubernetes namespace or for a Linux user.
* **link**\
A secure connection between sites that enables communication and service sharing between those sites.
* **gateway**\
A system service running on a Linux machine that enables you expose services, for example a database, on the service network.
