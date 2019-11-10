# Skupper connectivity

<p style="font-size: 1.2em; line-height: 1.4em;">Skupper represents a
  new approach to connecting services across multiple Kubernetes
  clusters.  See how Skupper can give you the flexibility to deploy
  your services where you need them.</p>

<div class="topology">
  <div>
    <div id="-one-cluster">
      {{include("includes/one-cluster.svg")}}
    </div>
    <div>
      <p>Kubernetes <strong>services</strong> provide a virtual
        network address for each element of your distributed
        application.  Service "A" can contact service "B", "B" can
        contact "C", and so on.</p>

      <p>But if you want to deploy your application across multiple
        clusters, your options are limited.  You have to either expose
        your services to the public internet or set up a VPN.</p>

      <p>Skupper offers a third way.  It connects clusters to a secure
        layer 7 network.  It uses that network to forward local service
        traffic to remote clusters.</p>
    </div>
  </div>
</div>

<div class="topology">
  <div>
    <div>
      {{include("includes/two-clusters.svg")}}
    </div>
    <div>
      <p><strong>Secure hybrid cloud communication.</strong> Deploy
        your application across public and private clusters.</p>

      <p>You can host your database on a private cluster and retain
        full connectivity with services running on the public cloud.
        All communication is secured by mutual TLS authentication and
        encryption.</p>
    </div>
  </div>
</div>

<div class="topology">
  <div>
    <div>
      {{include("includes/five-clusters.svg")}}
    </div>
    <div>
      <p><strong>Edge-to-edge connectivity.</strong> Distribute
        application services across geographic regions.</p>

      <p>You can connect multiple retail sites to a central office.
        Once connected, each edge location can contact any other edge.
        You can add and remove sites on demand.</p>
    </div>
  </div>
</div>

<div class="topology">
  <div>
    <div>
      {{include("includes/many-clusters.svg")}}
    </div>
    <div>
      <p><strong>Scale up and out.</strong> Build large, robust
        networks of connected clusters.</p>

      <p>Skupper uses redundant network paths and smart routing to
        provide highly available connectivity at scale.</p>
    </div>
  </div>
</div>

<!-- ## More information -->

<!--  - [Skupper routing](routing.html) -->
<!--  - [Skupper architecture](architecture.html) -->
