# Skupper

Skupper is an over-the-top, multi-platform application interconnect.
Skupper makes it easy to deploy private application networks that span
multiples sites and platforms.

<style>
ul {
    margin-bottom: -1em;
}
ul > li {
    margin-bottom: 1em;
}
</style>
<ul style="columns: 2;">
  <li><strong>Over-the-top</strong> - Skupper operates at the
  application layer, on top of existing IP networks.  Services connect
  across network boundaries without VPNs or special firewall
  rules.</li>

  <li><strong>Multi-platform</strong> - Skupper works on Kubernetes,
  Docker, Podman, and Linux.  It scales up to multi-tenant clusters
  and down to edge devices.</li>

  <li><strong>Application-centric</strong> - Skupper creates isolated
  application-focused networks with logical service addresses that
  enable application portability.</li>

  <li><strong>Secure</strong> - Skupper uses mutual TLS authentication
  and encryption to protect all communication.  Application services
  are never exposed on the public internet.</li>
</ul>

<nav class="links">
  <a href="docs/overview/index.html">Overview</a>
  <a href="concepts/index.html">Concepts</a>
  <a href="start/index.html">Getting started</a>
</nav>

<p>
  <iframe style="width: 20em; float: right; margin-left: 1em;" src="https://www.youtube.com/embed/pm8OP9bG2mU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen="allowfullscreen"></iframe>

  <strong>Skupper v2</strong> is the latest generation of Skupper.  It
  has a new declarative API based on CRDs, a new CLI, improved
  performance, and broader platform support.
</p>

<nav class="links">
  <a href="v2/index.html">V2 overview</a>
</nav>

**Skupper v1** resources are available [here](v1/).

## Use cases

<ul style="columns: 2;">
  <li><strong>Remote resource access</strong> - Access on-prem
  resources from the public cloud.  Access cloud resources from the
  private cloud.</li>

  <li><strong>Platform migration</strong> - Move application
  components one at a time to a new platform, with the ability to
  rollback at any time.</li>

  <li><strong>Application resiliency</strong> - High availability and
  disaster recovery.  Data distribution and load balancing.</li>

  <li><strong>Highly distributed applications</strong> - Multi-geo
  retail and logistics applications.  Edge applications with diverse
  compute environments.</li>
</ul>

<nav class="links">
  <!-- <a href="docs/introduction/use-cases.html">Use case overview</a> -->
  <a href="examples/index.html">Examples</a>
</nav>

## Installation

Install Skupper on Kubernetes:

~~~ shell
kubectl apply -f https://skupper.io/install.yaml
~~~

Install the Skupper CLI:

~~~ shell
curl https://skupper.io/install.sh | sh
~~~

<nav class="links">
  <a href="docs/install/index.html">Installing on Kubernetes</a>
  <a href="docs/install/index.html#installing-the-skupper-cli">Installing the CLI</a>
</nav>

## The Skupper API

<style>
div.side-by-side {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    font-size: 0.95em;
}
</style>
<div class="side-by-side">
  <div class="code-label">Site 1</div>
  <div class="code-label">Site 2</div>
  <pre><code>{{page.include("config/west.yaml")}}</code></pre>
  <pre><code>{{page.include("config/east.yaml")}}</code></pre>
</div>

Use the CLI to link the sites:

<div class="side-by-side">
  <div class="code-label">Site 1</div>
  <div class="code-label">Site 2</div>
  <pre><code>{{page.include("config/west-link.sh")}}</code></pre>
  <pre><code>{{page.include("config/east-link.sh")}}</code></pre>
</div>

<nav class="links">
  <a href="docs/kube-yaml/">Using the API on Kubernetes</a>
  <a href="docs/system-yaml/">Using the API on Linux</a>
  <a href="resources/">API reference</a>
</nav>

## The Skupper CLI

<div class="side-by-side">
  <div class="code-label">Site 1</div>
  <div class="code-label">Site 2</div>
  <pre><code>{{page.include("config/west.sh")}}</code></pre>
  <pre><code>{{page.include("config/east.sh")}}</code></pre>
</div>

<nav class="links">
  <a href="docs/kube-cli/">Using the CLI on Kubernetes</a>
  <a href="docs/system-cli/">Using the CLI on Linux</a>
  <a href="commands/">CLI reference</a>
</nav>
