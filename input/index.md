---
title: Skuba
body_template: none
extra_headers: <link rel="stylesheet" href="{{site_url}}/index.css" type="text/css" async="async"/>
---

<header>
  <div>
    <nav id="-top-left-nav">
      <a href="{{site_url}}/index.html" class="nameplate">{{circle(20)}} Skuba</a>
      <a href="{{site_url}}/get-started/index.html">{{circle(20)}} Get started</a>
      <a href="{{site_url}}/docs/index.html">{{circle(20)}} Documentation</a>
    </nav>
    <nav id="-top-right-nav">
      <a href="https://github.com/skubaproject"><img class="inline-icon" src="{{site_url}}/images/github.svg"/> GitHub</a>
    </nav>
  </div>
</header>

<section id="-intro-section">
  <div>
    <h1 class="nameplate">Skuba</h1>

    {{include("includes/globe.svg")}}

    <h2>Multi-site application networking for Kubernetes</h2>

    <p>Skuba connects services from multiple Kubernetes clusters to a
      secure Layer 7 interconnect.  It works with any IP network
      topology, including subnets behind firewalls or NAT, so you can
      host your services anywhere.</p>

    <div>
      <h3>Level up your networking with</h3>
      
      <ul>
        <li>Secure interconnection among multiple clusters, data centers, and regions</li>
        <li>Transparent TCP and HTTP communication across public and private IP networks</li>
        <li>Dynamic HTTP load balancing that responds to changes in service capacity</li>
        <li>Centralized network administration and easy cluster onboarding</li>
        <li>New communication powers: multicast and cost-based routing</li>
      </ul>
    </div>
  </div>
</section><svg id="-wave" height="6em" width="100%" xmlns="http://www.w3.org/2000/svg">
  <path d="M 0 0 L 0 50 Q 400 100, 800 50 T 1600 50 T 2400 50 T 3200 50 L 3200 0 Z" fill="#fff"/>
</svg>

<section>
  <div class="video">
    <iframe width="320" height="180" src="https://www.youtube.com/embed/AjPau5QYtYs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    <div>
      <h2>Connect multi-site services to a shared database</h2>
      <p>{{lipsum_25}}</p>
    </div>
  </div>
</section>

<section>
  <div class="video">
    <div>
      <h2>Load-balance API calls across clusters</h2>
      <p>{{lipsum_25}}</p>
    </div>
    <iframe width="320" height="180" src="https://www.youtube.com/embed/AjPau5QYtYs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
  </div>
</section>

<section>
  <div class="video">
    <iframe width="320" height="180" src="https://www.youtube.com/embed/AjPau5QYtYs" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    <div>
      <h2>Centrally manage your global application network</h2>
      <p>{{lipsum_25}}</p>
    </div>
  </div>
</section>

<footer>
  <div>
  </div>
</footer>
