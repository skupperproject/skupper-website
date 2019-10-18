# Skupper connectivity

<section class="topology">
  <div>
    <div id="-one-cluster">
      {{include("includes/one-cluster.svg")}}
    </div>
    <div>
      <p>Kubernetes <strong>services</strong> provide a virtual
        network address and name for each functional element of your
        distributed application.</p>

      <p>As long as your application remains inside a single cluster,
        services are powerful and convenient.  But when you want to
        use multiple clusters, XXX.</p>

      <p>Skupper enables services to span multiple clusters.</p>
    </div>
  </div>
</section>

<section class="topology">
  <div>
    <div>
      {{include("includes/two-clusters.svg")}}
    </div>
    <div>
      <p>Hybrid-cloud XXX</p>
    </div>
  </div>
</section>

<section class="topology">
  <div>
    <div>
      {{include("includes/five-clusters.svg")}}
    </div>
    <div>
      <p>Edge XXX</p>
    </div>
  </div>
</section>

<section class="topology">
  <div>
    <div>
      {{include("includes/many-clusters.svg")}}
    </div>
    <div>
      <p>Skupper scales XXX</p>
    </div>
  </div>
</section>
