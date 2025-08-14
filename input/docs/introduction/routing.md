# Skupper routing

Skupper uses layer 7 addressing and routing to connect services.
See how the power of application-layer addressing can bring new capabilities to your applications.

**Multi-cluster services**

Deploy a single logical service across multiple clusters.

Skupper can route requests to instances of a single service running on multiple clusters.
If a provider or data center fails, the service instances running at unaffected sites can scale to meet the need and maintain availability.

**Dynamic load balancing**

Balance requests across clusters according to service capacity.

The Skupper network has cross-cluster visibility.
It can see which services are already loaded and which have spare capacity, and it directs requests accordingly.

You can assign a cost to each inter-cluster connection.
This enables you to configure a preference for one resource over another.
If demand is normal, you can keep all traffic on your private cloud.
If demand peaks, you can dynamically spill over to public cloud resources.

**Reliable networks**

Skupper uses redundant network paths and smart routing to provide highly available connectivity at scale.

## Load balancing and failover

Skupper enables load balancing and failover across servers located across the application network.
Specifically, Skupper balances **active TCP connections** across workloads deployed in distinct sites.
If a workload at one site becomes unavailable, traffic is automatically rerouted to available sites.
For example, if you deploy the same backend code on two sites and expose the backend on the application network, concurrent requests from a third site to the backend service are processed by both sites.

In an application network, the routing algorithm attempts to use the path with the lowest total **cost** from client to target server.

**Understanding link cost**

Link cost is a configurable value when creating links between sites.
In the earlier example, the link cost from the client to each server is the same by default (1).
However, if one server is more powerful and has better latency, it processes TCP requests more quickly, resulting in more traffic being directed to that server.
Skupper determines the perceived cost with the context of knowing the configured cost and the current number of open TCP connections and  directs traffic to the server with the lowest cost.

* Local workloads have a link cost of 0.
* If connecting to a workload requires traversing two or more links, the total of all link costs constitutes the link cost.

**📌 NOTE**
Traffic load is based on the number of concurrent TCP connections, so 'round robin' behavior should not be expected.

**Using Skupper load balancing to achieve failover**

You can configure the network so that a specific location handles all traffic until failure.
After failure at that location, all traffic is handled by a different location.
To achieve this behavior, you set the cost from the client to the backup server high, for example 9999,  as described in {cost-link}.

**📌 NOTE**
Link cost is configured for all services between two sites.
It is currently not possible to set different costs for distinct services.
