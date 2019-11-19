# Skupper routing

<div class="benefits">
  <p>Skupper uses layer 7 addressing and routing to connect services.
    See how the power of application-layer addressing can bring new
    capabilities to your applications.</p>

  <div class="pattern">
    <div>
      <div>
        {{include("includes/many-clusters.svg")}}
      </div>
      <div>
        <p><strong>Multi-cluster services.</strong>  Deploy a single
        logical service across multiple clusters.</p>

        <p>Skupper can route requests to instances of a single service
          running on multiple clusters.  If a provider or data center
          fails, the service instances running at unaffected sites can
          scale to meet the need and maintain availability.</p>
      </div>
    </div>
  </div>

  <div class="pattern">
    <div>
      <div>
        {{include("includes/many-clusters.svg")}}
      </div>
      <div>
        <p><strong>Global load balancing.</strong>  Balance requests
          across clusters according to service capacity.</p>

        <p>The Skupper network has cross-cluster visibility.  It can see
          which services are already loaded and which have spare
          capacity, and it directs requests accordingly.</p>

        <p>You can assign a cost to each inter-cluster connection.  This
          enables you to configure a preference for one resource over
          another.  If demand is normal, you can keep all traffic on
          your private cloud.  If demand peaks, you can dynamically
          spill over to public cloud resources.</p>
      </div>
    </div>
  </div>

  <p>Skupper also provides <b><a href="connectivity.html">new options for
    deploying your application</a></b>.</p>

  <p>To learn more about how Skupper achieves this and other benefits,
    see the <b><a href="index.html">Skupper architecture
    overview</a></b>.</p>
</div>
