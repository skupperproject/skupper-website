# Skupper connectivity

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
        layer 7 network.  It uses the network to forward local service
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
      <p><strong>Hybrid-cloud:</strong> Deploy your application across
        public and private clusters.</p>

      <p>For example, you can host your database services on a private
        cluster and retain full connectivity with services running on
        the public cloud.</p>
    </div>
  </div>
</div>

<div class="topology">
  <div>
    <div>
      {{include("includes/five-clusters.svg")}}
    </div>
    <div>
      <p><strong>Edge-to-edge:</strong> Distribute your application across
        geographic regions.</p>

      <p>For instance, you can connect multiple retail locations to a
      central office.  Once connected, each edge location can contact
      any other edge.  You can add and remove locations on demand.</p>
    </div>
  </div>
</div>

<div class="topology">
  <div>
    <div>
      {{include("includes/many-clusters.svg")}}
    </div>
    <div>
      <p><strong>Scale out:</strong> Skupper supports very large
        networks of connected clusters.</p>

      <p>Skupper uses redundant network paths and smart routing to
        provide highly available connectivity at scale.</p>
    </div>
  </div>
</div>
