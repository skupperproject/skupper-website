---
title: Troubleshooting a service network
---
# Troubleshooting a service network

Typically, you can create a service network without referencing this troubleshooting guide.
However, this guide provides some tips for situations when the service network does not perform as expected.

See [Resolving common problems](#resolving-common-problems) if you have encountered a specific issue using the `skupper` CLI.

A typical troubleshooting workflow is to check all the sites and create debug tar files.

## Checking sites

Using the `skupper` command-line interface (CLI) provides a simple method to get started with troubleshooting Skupper.

1. Check the site status:

   ```bash
   $ skupper status --namespace west

   Skupper is enabled for namespace "west" in interior mode. It is connected to 2 other sites. It has 1 exposed services.
   ```

   The output shows:

   * A site exists in the specified namespace.
   * A link exists to two other sites.
   * A service is exposed on the service network and is accessible from this namespace.
2. Check the service network:

   ```bash
   $ skupper network status
   Sites:
   ├─ [local] a960b766-20bd-42c8-886d-741f3a9f6aa2(west)
   │  │ namespace: west
   │  │ site name: west
   │  │ version: 1.5.1
   │  ╰─ Linked sites:
   │     ├─ 496ca1de-0c80-4e70-bbb4-d0d6ec2a09c0(east)
   │     │  direction: outgoing
   │     ╰─ 484cccc3-401c-4c30-a6ed-73382701b18a()
   │        direction: incoming
   ├─ [remote] 496ca1de-0c80-4e70-bbb4-d0d6ec2a09c0(east)
   │  │ namespace: east
   │  │ site name: east
   │  │ version: 1.5.1
   │  ╰─ Linked sites:
   │     ╰─ a960b766-20bd-42c8-886d-741f3a9f6aa2(west)
   │        direction: incoming
   ╰─ [remote] 484cccc3-401c-4c30-a6ed-73382701b18a()
      │ site name: vm-user-c3d98
      │ version: 1.5.1
      ╰─ Linked sites:
         ╰─ a960b766-20bd-42c8-886d-741f3a9f6aa2(west)
            direction: outgoing
   ```

   **📌 NOTE**\
   If the output is not what you expected, you might want to [check links](#checking-links) before proceeding.

   The output shows:

   * There are 3 sites on the service network, `vm-user-c3d98`, `east` and `west`.
   * Details for each site, for example the namespace names.
3. Check the status of services exposed on the service network:

   ```bash
   $ skupper service status
   Services exposed through Skupper:
   ╰─ backend (tcp port 8080)
      ╰─ Targets:
         ╰─ app=backend name=backend
   ```

   The output shows the `backend` service and the related target of that service.

   **📌 NOTE**\
   The related targets for services are only displayed when the target is available on the current cluster.
4. List the Skupper events for a site:

   ```bash
   $ skupper debug events
   NAME                         COUNT                                                          AGE
   GatewayQueryRequest          3                                                              9m12s
                                3     gateway request                                          9m12s
   SiteQueryRequest             3                                                              9m12s
                                3     site data request                                        9m12s
   ServiceControllerEvent       9                                                              10m24s
                                2     service event for west/frontend                          10m24s
                                1     service event for west/backend                           10m26s
                                1     Checking service for: backend                            10m26s
                                2     Service definitions have changed                         10m26s
                                1     service event for west/skupper-router                    11m4s
   DefinitionMonitorEvent       15                                                             10m24s
                                2     service event for west/frontend                          10m24s
                                1     service event for west/backend                           10m26s
                                1     Service definitions have changed                         10m26s
                                5     deployment event for west/frontend                       10m34s
                                1     deployment event for west/skupper-service-controller     11m4s
   ServiceControllerUpdateEvent 1                                                              10m26s
                                1     Updating skupper-internal                                10m26s
   ServiceSyncEvent             3                                                              10m26s
                                1     Service interface(s) added backend                       10m26s
                                1     Service sync sender connection to                        11m4s
                                      amqps://skupper-router-local.west.svc.cluster.local:5671
                                      established
                                1     Service sync receiver connection to                      11m4s
                                      amqps://skupper-router-local.west.svc.cluster.local:5671
                                      established
   IpMappingEvent               5                                                              10m34s
                                1     172.17.0.7 mapped to frontend-6b4688bf56-rp9hc           10m34s
                                2      mapped to frontend-6b4688bf56-rp9hc                     10m54s
                                1     172.17.0.4 mapped to                                     11m4s
                                      skupper-service-controller-6c97c5cf5d-6nzph
                                1     172.17.0.3 mapped to skupper-router-547dffdcbf-l8pdc     11m4s
   TokenClaimVerification       1                                                              10m59s
                                1     Claim for efe3a241-3e4f-11ed-95d0-482ae336eb38 succeeded 10m59s

   ```
   The output shows sites being linked and a service being exposed on a service network.
   However, this output is most useful when reporting an issue and is included in the Skupper debug tar file.
5. List the Kubernetes events for a site:

   ```bash
   kubectl get events | grep "service/skupper"
   10m         Normal    ServiceSyncEvent               service/skupper                                   Service sync receiver connection to amqps://skupper-router-local.private1.svc.cluster.local:5671 established
   10m         Normal    ServiceSyncEvent               service/skupper                                   Service sync sender connection to amqps://skupper-router-local.private1.svc.cluster.local:5671 established
   10m         Normal    ServiceControllerCreateEvent   service/skupper                                   Creating service productcatalogservice
   7m59s       Normal    TokenHandler                   service/skupper                                   Connecting using token link1
   7m54s       Normal    TokenHandler                   service/skupper                                   Connecting using token link2
   ```

   The output shows events relating to Kubernetes resources.

* [Checking links](#checking-links)

## Checking links

You must link sites before you can expose services on the service network.

**📌 NOTE**\
By default, tokens expire after 5 minutes and you can only use a token once.
Generate a new token if the link is not connected.
You can also generate tokens using the `-token-type cert` option for permanent reusable tokens.

This section outlines some advanced options for checking links.

1. Check the link status:

   ```bash
   $ skupper link status --namespace east

   Links created from this site:
   -------------------------------
   Link link1 is connected
   ```

   A link exists from the specified site to another site, meaning a token from another site was applied to the specified site.

   **📌 NOTE**\
   Running `skupper link status` on a connected site produces output only if a token was used to create a link.

   If you use this command on a site where you did not create the link, but there is an incoming link to the site:
   ```
   $ skupper link status --namespace west

   Links created from this site:
   -------------------------------
   There are no links configured or connected

   Currently connected links from other sites:
   ----------------------------------------
   A link from the namespace east on site east(536695a9-26dc-4448-b207-519f56e99b71) is connected
   ```
2. Check the verbose link status:

   ```bash
   $ skupper link status link1 --verbose --namespace east

    Cost:          1
    Created:       2022-10-24 12:50:33 +0100 IST
    Name:          link1
    Namespace:     east
    Site:          east-536695a9-26dc-4448-b207-519f56e99b71
    Status:        Connected
   ```

   The output shows detail about the link, including a timestamp of when the link was created and the associated relative cost of using the link.

   The status of the link must be `Connected` to allow service traffic.

* [Checking sites](#checking-sites)

## Checking gateways

By default, `skupper gateway` creates a service type gateway and these gateways run properly after a machine restart.

However, if you create a docker or podman type gateway, check that the container is running after a machine restart.
For example:

1. Check the status of Skupper gateways:

   ```
   $ skupper gateway status

   Gateway Definition:
   ╰─ machine-user type:podman version:1.5
      ╰─ Bindings:
         ╰─ mydb:3306 tcp mydb:3306 localhost 3306

   ```
   This shows a podman type gateway.
2. Check that the container is running:

   ```
   $ podman ps
   CONTAINER ID  IMAGE                                           COMMAND               CREATED         STATUS             PORTS                   NAMES
   4e308ef8ee58  quay.io/skupper/skupper-router:1.5             /home/skrouterd/b...  26 seconds ago  Up 27 seconds ago                          machine-user

   ```
   This shows the container running.

   **📌 NOTE**\
   To view stopped containers, use `podman ps -a` or `docker ps -a`.
3. Start the container if necessary:

   ```

   $ podman start machine-user

   ```

## Checking policies

As a developer you might not be aware of the Skupper policy applied to your site.
Follow this procedure to explore the policies applied to the site.

1. Log into a namespace where a Skupper site has been initialized.
2. Check whether incoming links are permitted:

   ```bash
   $ kubectl exec deploy/skupper-service-controller -- get policies incominglink

   ALLOWED POLICY ENABLED ERROR                                                   ALLOWED BY
   false   true           Policy validation error: incoming links are not allowed
   ```

   In this example incoming links are not allowed by policy.
3. Check other policies:

   ```bash
   $ kubectl exec deploy/skupper-service-controller -- get policies
   Validates existing policies

   Usage:
     get policies [command]

   Available Commands:
     expose       Validates if the given resource can be exposed
     incominglink Validates if incoming links can be created
     outgoinglink Validates if an outgoing link to the given hostname is allowed
     service      Validates if service can be created or imported
   ```

   As shown, there are commands to check each policy type by specifying what you want to do, for example, to check if you can expose an nginx deployment:

   ```bash
   $ kubectl  exec deploy/skupper-service-controller -- get policies expose deployment nginx
   ALLOWED POLICY ENABLED ERROR                                                       ALLOWED BY
   false   true           Policy validation error: deployment/nginx cannot be exposed
   ```

   If you allowed an nginx deployment, the same command shows that the resource is allowed and displays the name of the policy CR that enabled it:

   ```bash
   $ kubectl  exec deploy/skupper-service-controller -- get policies expose deployment nginx
   ALLOWED POLICY ENABLED ERROR                                                       ALLOWED BY
   true    true                                                                       allowedexposedresources
   ```

## Creating a Skupper debug tar file

The debug tar file contains all the logs from the Skupper components for a site and provides detailed information to help debug issues.

1. Create the debug tar file:

   ```
   $  skupper debug dump my-site

   Skupper dump details written to compressed archive:  `my-site.tar.gz`
   ```
2. You can expand the file using the following command:

   ```bash
   $ tar -xvf kind-site.tar.gz

   k8s-versions.txt
   skupper-versions.txt
   skupper-router-deployment.yaml
   skupper-router-867f5ddcd8-plrcg-skstat-g.txt
   skupper-router-867f5ddcd8-plrcg-skstat-c.txt
   skupper-router-867f5ddcd8-plrcg-skstat-l.txt
   skupper-router-867f5ddcd8-plrcg-skstat-n.txt
   skupper-router-867f5ddcd8-plrcg-skstat-e.txt
   skupper-router-867f5ddcd8-plrcg-skstat-a.txt
   skupper-router-867f5ddcd8-plrcg-skstat-m.txt
   skupper-router-867f5ddcd8-plrcg-skstat-p.txt
   skupper-router-867f5ddcd8-plrcg-router-logs.txt
   skupper-router-867f5ddcd8-plrcg-config-sync-logs.txt
   skupper-service-controller-deployment.yaml
   skupper-service-controller-7485756984-gvrf6-events.txt
   skupper-service-controller-7485756984-gvrf6-service-controller-logs.txt
   skupper-site-configmap.yaml
   skupper-services-configmap.yaml
   skupper-internal-configmap.yaml
   skupper-sasl-config-configmap.yaml
   ```

   These files can be used to provide support for Skupper, however some items you can check:

   * **versions**\
   See `*versions.txt` for the versions of various components.
   * **ingress**\
   See `skupper-site-configmap.yaml` to determine the `ingress` type for the site.
   * **linking and services**\
   See the `skupper-service-controller-*-events.txt` file to view details of token usage and service exposure.

## Improving Skupper router performance

If you encounter Skupper router performance issues, you can scale the Skupper router to address those concerns.

**📌 NOTE**\
Currently, you must delete and recreate a site to reconfigure the Skupper router.

For example, use this procedure to increase throughput, and if you have many clients, latency.

1. Delete your site or create a new site in a different namespace.

   Note all configuration and delete your existing site:

   ```bash
   $ skupper delete
   ```

   As an alternative, you can create a new namespace and configure a new site with optimized Skupper router performance.
   After validating the performance improvement, you can delete and recreate your original site.
2. Create a site with optimal performance CPU settings:

   ```bash
   $ skupper init --router-cpu 5
   ```
3. Recreate your configuration from step 1, recreating links and services.

**📌 NOTE**\
While you can address availability concerns by scaling the number of routers, typically this is not necessary.

## Resolving common problems

The following issues and workarounds might help you debug simple scenarios when evaluating Skupper.

**Cannot initialize skupper**

If the `skupper init` command fails, consider the following options:

* Check the load balancer.

  If you are evaluating Skupper on minikube, use the following command to create a load balancer:

  ```bash
  $ minikube tunnel
  ```

  For other Kubernetes flavors, see the documentation from your provider.
* Initialize without ingress.

  This option prevents other sites from linking to this site, but linking outwards is supported.
  Once a link is established, traffic can flow in either direction.
  Enter the following command:

  ```bash
  $ skupper init --ingress none
  ```

  <dl><dt><strong>📌 NOTE</strong></dt><dd>

  See the [Skupper Podman CLI reference](../podman-reference/index.html) documentation for `skupper init`.
  </dd></dl>

**Cannot link sites**

To link two sites, one site must be accessible from the other site.
For example, if one site is behind a firewall and the other site is on an AWS cluster, you must:

1. Create a token on the AWS cluster site.
2. Create the link on the site inside the firewall.

<dl><dt><strong>📌 NOTE</strong></dt><dd>

By default, a token is valid for only 15 minutes and can only be used once.
See [Using Skupper tokens](../cli/tokens.html) for more information on creating different types of tokens.
</dd></dl>

**Cannot access Skupper console**

Starting with Skupper release 1.3, the console is not enabled by default.
To use the new console, see [Using the Skupper console](../console/index.html).

Use `skupper status` to find the console URL.

Use the following command to display the password for the `admin` user:doctype: article

```
$ kubectl get secret/skupper-console-users -o jsonpath={.data.admin} | base64 -d
```

**Cannot create a token for linking clusters**

There are several reasons why you might have difficulty creating tokens:

* **Site not ready**

  After creating a site, you might see the following message when creating a token:
  ```bash
  Error: Failed to create token: Policy validation error: Skupper is not enabled in namespace
  ```

  Use `skupper status` to verify the site is working and try to create the token again.
* **No ingress**

  You might see the following note after using the `skupper token create` command:
  ```bash
  Token written to <path> (Note: token will only be valid for local cluster)
  ```

  This output indicates that the site was deployed without an ingress option. For example `skupper init --ingress none`.
  You must specify an ingress to allow sites on other clusters to link to your site.

  You can also use the `skupper token create` command to check if an ingress was specified when the site was created.