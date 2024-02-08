---
title: Deployment options on Kubernetes
---
# Deployment options on Kubernetes

When you create a site on Kubernetes, there are many options you can use.  For example, you can set the number of pods and the resources allocated to each pod.
This guide focusses on the following goals:

* [Scaling for increased traffic](#scaling-for-increased-traffic)
* [Creating a high availability site](#creating-a-high-availability-site)

## Scaling for increased traffic

For optimal network latency and throughput, you can adjust the CPU allocation for the router using the `router-cpu` option.
Router CPU is the primary factor governing Skupper network performance.

**📌 NOTE**\
Increasing the number of routers does not improve network performance.  An incoming router-to-router link is associated with just one active router.  Additional routers do not receive traffic while that router is responding

1. Determine the router CPU allocation you require.

   By default, the router CPU allocation is `BestEffort` as described in [Pod Quality of Service Classes](https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/#besteffort).

   Consider the following CPU allocation options:

   |     |     |
   | --- | --- |
   | Router CPU | Description |
   | 1 | Helps avoid issues with `BestEffort` on low resource clusters |
   | 2 | Suitable for production environments |
   | 5 | Maximum performance |
2. If you are using the Skupper CLI, set the CPU allocation for the router using the `--router-cpu` option.  For example:

   ```bash
   $ skupper init --router-cpu 2
   ```
3. If you are using YAML, set the CPU allocation for the router by setting a value for the `router-cpu` attribute.  For example:

   ```YAML
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: "skupper-site"
   data:
     name: "my-site"
     router-cpu: 2
   ```

## Creating a high availability site

By default, Kubernetes restarts any router that becomes unresponsive.
(If you encounter router restarts, consider [Scaling for increased traffic](#scaling-for-increased-traffic) in order to improve responsiveness.)

If the cluster where you are running Skupper is very busy, it may take time for Kubernetes to schedule a new router pod.  You can "preschedule" a backup router by deploying two routers in a site.

1. If you are using the Skupper CLI, set the number of routers to `2` using the `--routers` option:

   ```bash
   $ skupper init --routers 2
   ```
2. If you are using YAML, set the number of routers to `2` by setting the `routers` attribute:

   ```YAML
   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: "skupper-site"
   data:
     name: "my-site"
     routers: 2
   ```

Setting the number of routers to more than two does not provide increased availability and can adversely affect performance.

Note that clients must reconnect when a router restarts or traffic is
redirected to a backup router.
