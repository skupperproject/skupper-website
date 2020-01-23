---
title: Examples
---

# Skupper examples

## Introductory examples

### [Hello World](https://github.com/skupperproject/skupper-example-hello-world)

A simple multi-service HTTP application that can be deployed across
multiple Kubernetes clusters using Skupper.  This is our most
elemental HTTP example.

### [Communicating over TCP between two clusters](https://github.com/skupperproject/skupper-example-tcp-echo)

Our most basic TCP example.  It demonstrates TCP communication
tunneled through a Skupper network from a private to a public
namespace and back again.

## HTTP examples

### [Load balancing HTTP requests across clusters](https://github.com/skupperproject/skupper-example-http-load-balancing)

See how to deploy a set of HTTP server processes across multiple clusters and
observe anycast application routing over a Virtual Application
Network.

### [Deploying the Istio Bookinfo example across clusters](https://github.com/skupperproject/skupper-example-bookinfo)

See how you can use Skupper to distribute the microservices of the
Istio Bookinfo application to multiple public and private clouds.

## TCP examples

### [Accessing a PostgreSQL database in the private cloud](https://github.com/skupperproject/skupper-example-postgresql)

Learn how to share a PostgreSQL database across multiple Kubernetes
clusters that are located in different public and private cloud
providers.

### [Deploying a MongoDB replica set across clusters](https://github.com/skupperproject/skupper-example-mongodb-replica-set)

Learn how to share a MongoDB database across multiple Kubernetes
clusters that are located in different public and private cloud
providers.

<!-- ## Measuring TCP throughput with iperf -->

<!-- Learn how to perform real-time network throughput measurements on an -->
<!-- application router network using the `iperf3` tool. -->

<!-- <nav class="links"> -->
<!--   <a href="https://github.com/skupperproject/skupper-example-iperf">Tutorial</a> -->
<!--   <a href="https://github.com/skupperproject/skupper-example-iperf">Example code</a> -->
<!-- </nav> -->

<!-- <h2 class="example-category">Performance and load testing</h2> -->
<!-- <h2 class="example-category">Minimal examples</h2> -->
<!-- <h2 class="example-category">TCP-based applications</h2> -->
<!-- <h2 class="example-category">HTTP-based applications</h2> -->
