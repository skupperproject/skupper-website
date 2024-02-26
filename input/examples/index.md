---
title: Examples
extra_headers: <link rel="stylesheet" href="index.css" type="text/css" async="async"/><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0"/>
---

# Skupper examples

These examples provide step-by-step instructions to install and use
Skupper for common multi-cluster and edge deployment scenarios.

<h2 id="featured-applications">Featured applications</h2>

<p>Skupper works with your existing application code, no changes
required.  These examples highlight Skupper's ability to deploy
conventional applications across multiple sites.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-hello-world">Hello World</a></h3>
<p>A minimal multi-service HTTP application deployed across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-hello-world"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-patient-portal">Patient Portal</a></h3>
<p>A database-backed web application deployed across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-patient-portal"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-trade-zoo">Trade Zoo</a></h3>
<p>A Kafka-based trading application deployed across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-trade-zoo"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-bookinfo">Bookinfo</a></h3>
<p>Deploy the Istio Bookinfo application across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-bookinfo"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=H80GLl-KdTc"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-grpc">Online Boutique</a></h3>
<p>Deploy the gRPC-based Online Boutique application across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-grpc"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-http-load-balancing">HTTP load balancing</a></h3>
<p>Use Skupper to balance HTTP requests across sites</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-http-load-balancing"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=4GmXT3nj8lc"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
</div>

<h2 id="platforms">Platforms</h2>

<p>Skupper works with services running as pods on Kubernetes, as
containers, or as ordinary processes on bare metal hosts or VMs.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-hello-world">Kubernetes</a></h3>
<p>Connect services running as pods in Kubernetes
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-hello-world"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-podman">Podman</a></h3>
<p>Connect services running as containers
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-podman"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-gateway">Bare metal or VM</a></h3>
<p>Connect services running as system processes</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-gateway"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="interfaces">Interfaces</h2>

<p>Skupper provides a command-line interface for interactive
control and a YAML interface for declarative configuration.  The
Skupper web console helps you observe your application network.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-hello-world">Command line</a></h3>
<p>Hello World deployed across sites using the Skupper CLI
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-hello-world"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-yaml">YAML</a></h3>
<p>Hello World deployed across sites using Skupper YAML</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-yaml"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-console">Web console</a></h3>
<p>Explore an application network using the Skupper web console</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-console"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="connectivity-scenarios">Connectivity scenarios</h2>

<p>Skupper helps you overcome tough networking obstacles.  See how
you can securely connect services in sites behind firewalls or
NAT without changing your existing networking.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-public-to-private">Public to private</a></h3>
<p><div style="padding-bottom: 0.8em;">
  <span class="material-symbols-outlined">cloud</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">business</span>
</div>
Connect from the cloud to services running on-prem
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-public-to-private"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-private-to-private">Private to private</a></h3>
<p><div style="padding-bottom: 0.8em;">
  <span class="material-symbols-outlined">business</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">cloud</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">business</span>
</div>
Connect services in isolated on-prem sites
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-private-to-private"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-dmz">DMZ</a></h3>
<p><div style="padding-bottom: 0.8em;">
  <span class="material-symbols-outlined">cloud</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">shield</span>
  <span class="material-symbols-outlined">horizontal_rule</span>
  <span class="material-symbols-outlined">business</span>
</div>
Connect services separated by firewalls and a DMZ
</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-dmz"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="database-examples">Database examples</h2>

<p>With Skupper you can locate your data wherever you need it to
be, while accessing it from wherever your services are running.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-mongodb-replica-set">MongoDB</a></h3>
<p>Deploy a MongoDB replica set across sites using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-mongodb-replica-set"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-mysql">MySQL</a></h3>
<p>Access a MySQL database in a private data center from the public cloud</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-mysql"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-postgresql">PostgreSQL</a></h3>
<p>Access a PostgreSQL database in a private data center from the public cloud</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-postgresql"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=Oa0aVpb0v7U"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
</div>

<h2 id="messaging-examples">Messaging examples</h2>

<p>Skupper helps you access message queues and connect event-driven
applications spread across isolated network locations.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-activemq">ActiveMQ</a></h3>
<p>Access an ActiveMQ message broker using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-activemq"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-kafka">Kafka</a></h3>
<p>Access a Kafka cluster using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-kafka"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=W7aUOgCTyOg"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-rabbitmq">RabbitMQ</a></h3>
<p>Access a RabbitMQ message broker using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-rabbitmq"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="protocol-examples">Protocol examples</h2>

<p>Skupper supports any TCP-based protocol.  These examples show
how you can access services based on widely used internet
protocols.
</p>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-tcp">TCP</a></h3>
<p>Access a TCP server using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-tcp"><span class="fab fa-github fa-lg"></span> Example</a>
<a href="https://www.youtube.com/watch?v=ZQo9cB0-1go"><span class="fab fa-youtube fa-lg"></span> Video</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-http">HTTP</a></h3>
<p>Access an HTTP server using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-http"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-ftp">FTP</a></h3>
<p>Access an FTP server using Skupper</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-ftp"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

<h2 id="other-examples">Other examples</h2>

<div class="examples">

<div>
<h3><a href="https://github.com/skupperproject/skupper-example-camel-integration">Camel</a></h3>
<p>Using Skupper to access private on-prem data from Camel</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-camel-integration"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-iperf">iPerf</a></h3>
<p>Perform real-time network throughput measurements using iPerf3</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-iperf"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-prometheus">Prometheus</a></h3>
<p>Gather Prometheus metrics from endpoints deployed across multiple clusters</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-prometheus"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
<div>
<h3><a href="https://github.com/skupperproject/skupper-example-policy">Policy</a></h3>
<p>Use Skupper cluster policy to restrict site linking and service exposure</p>
<nav class="inline-links">
<a href="https://github.com/skupperproject/skupper-example-policy"><span class="fab fa-github fa-lg"></span> Example</a>
</nav>
</div>
</div>

