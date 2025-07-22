---
title: Examples
---

# Skupper examples

These examples provide step-by-step instructions to install and use
Skupper for common multi-cluster and edge deployment scenarios.

## Featured applications

Skupper works with your existing application code, no changes
required.  These examples highlight Skupper's ability to deploy
conventional applications across multiple sites.


<div class="examples">

<section>

#### Hello World

A minimal multi-service HTTP application deployed across sites using Skupper

<a href="https://github.com/skupperproject/skupper-example-hello-world"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Patient Portal

A database-backed web application deployed across sites using Skupper

<a href="https://github.com/skupperproject/skupper-example-patient-portal"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Trade Zoo

A Kafka-based trading application deployed across sites using Skupper

<a href="https://github.com/skupperproject/skupper-example-trade-zoo"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Bookinfo

Deploy the Istio Bookinfo application across sites using Skupper

<a href="https://github.com/skupperproject/skupper-example-bookinfo"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Online Boutique

Deploy the gRPC-based Online Boutique application across sites using Skupper

<a href="https://github.com/skupperproject/skupper-example-grpc"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### HTTP load balancing

Use Skupper to balance HTTP requests across sites

<a href="https://github.com/skupperproject/skupper-example-http-load-balancing"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

</div>

## Connectivity scenarios

Skupper helps you overcome tough networking obstacles.  See how
you can securely connect services in sites behind firewalls or
NAT without changing your existing networking.


<div class="examples">

<section>

#### Public to private

<div style="padding-bottom: 0.8em;">
  <span class="material-symbols-outlined">cloud</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">business</span>
</div>
Connect from the cloud to services running on-prem


<a href="https://github.com/skupperproject/skupper-example-public-to-private"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Private to private

<div style="padding-bottom: 0.8em;">
  <span class="material-symbols-outlined">business</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">cloud</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">business</span>
</div>
Connect services in isolated on-prem sites


<a href="https://github.com/skupperproject/skupper-example-private-to-private"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### DMZ

<div style="padding-bottom: 0.8em;">
  <span class="material-symbols-outlined">cloud</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">shield</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">business</span>
</div>
Connect services separated by firewalls and a DMZ


<a href="https://github.com/skupperproject/skupper-example-dmz"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

</div>

## Platforms

Skupper works with services running as pods on Kubernetes, as
containers, or as ordinary processes on bare metal hosts or VMs.


<div class="examples">

<section>

#### Kubernetes

Connect services running as pods in Kubernetes


<a href="https://github.com/skupperproject/skupper-example-hello-world"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Podman

Connect services running as containers


<a href="https://github.com/skupperproject/skupper-example-podman"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Bare metal or VM

Connect services running as system processes

<a href="https://github.com/skupperproject/skupper-example-gateway"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

</div>

## Interfaces

Skupper provides a command-line interface for interactive
control and a YAML interface for declarative configuration.  The
Skupper web console helps you observe your application network.


<div class="examples">

<section>

#### Command line

Hello World deployed across sites using the Skupper CLI


<a href="https://github.com/skupperproject/skupper-example-hello-world"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### YAML

Hello World deployed across sites using Skupper YAML

<a href="https://github.com/skupperproject/skupper-example-yaml"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Web console

Explore an application network using the Skupper web console

<a href="https://github.com/skupperproject/skupper-example-console"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

</div>

## Administration

Skupper gives administrators tools to manage Skupper networks in
large organizations.


<div class="examples">

<section>

#### Policy

Use Skupper cluster policy to restrict site linking and service exposure

<a href="https://github.com/skupperproject/skupper-example-policy"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Ansible

Use Skupper Ansible to automate network deployment

<a href="https://github.com/skupperproject/skupper-example-ansible"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

</div>

## Database examples

With Skupper you can locate your data wherever you need it to
be, while accessing it from wherever your services are running.


<div class="examples">

<section>

#### MongoDB

Deploy a MongoDB replica set across sites using Skupper

<a href="https://github.com/skupperproject/skupper-example-mongodb-replica-set"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### MySQL

Access a MySQL database in a private data center from the public cloud

<a href="https://github.com/skupperproject/skupper-example-mysql"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### PostgreSQL

Access a PostgreSQL database in a private data center from the public cloud

<a href="https://github.com/skupperproject/skupper-example-postgresql"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

</div>

## Messaging examples

Skupper helps you access message queues and connect event-driven
applications spread across isolated network locations.


<div class="examples">

<section>

#### ActiveMQ

Access an ActiveMQ message broker using Skupper

<a href="https://github.com/skupperproject/skupper-example-activemq"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Kafka

Access a Kafka cluster using Skupper

<a href="https://github.com/skupperproject/skupper-example-kafka"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### RabbitMQ

Access a RabbitMQ message broker using Skupper

<a href="https://github.com/skupperproject/skupper-example-rabbitmq"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

</div>

## Protocol examples

Skupper supports any TCP-based protocol.  These examples show
how you can access services based on widely used internet
protocols.


<div class="examples">

<section>

#### TCP

Access a TCP server using Skupper

<a href="https://github.com/skupperproject/skupper-example-tcp"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### HTTP

Access an HTTP server using Skupper

<a href="https://github.com/skupperproject/skupper-example-http"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### FTP

Access an FTP server using Skupper

<a href="https://github.com/skupperproject/skupper-example-ftp"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

</div>

## More examples

<div class="examples">

<section>

#### Camel

Using Skupper to access private on-prem data from Camel

<a href="https://github.com/skupperproject/skupper-example-camel-integration"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### iPerf

Perform real-time network throughput measurements using iPerf3

<a href="https://github.com/skupperproject/skupper-example-iperf"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

<section>

#### Prometheus

Gather Prometheus metrics from endpoints deployed across multiple clusters

<a href="https://github.com/skupperproject/skupper-example-prometheus"><span class="fab fa-github fa-lg"></span> Example</a>

</section>

</div>

