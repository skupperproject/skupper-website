---
title: Using Skupper Podman
---
# Using Skupper Podman

Using the `skupper` command-line interface (CLI) allows you to create and manage Skupper sites from the context of the current Linux user.
Skupper Podman allows you to create a site using containers, without requiring Kubernetes.

A typical workflow is to create a site, link sites together, and expose services to the service network.

## About Skupper Podman

Skupper Podman is available with the following precedence:

* **`skupper --platform podman <command>`**\
Use this option to avoid changing mode, for example, if you are working on Kubernetes and Podman simultaneously.
* **`export SKUPPER_PLATFORM=podman`**\
Use this command to use Skupper Podman for the current session, for example, if you have two terminals set to different contexts. To set the environment to target Kubernetes sites:

  ```bash
  $ export SKUPPER_PLATFORM=kubernetes
  ```
* **`skupper switch podman`**\
If you enter this command, all subsequent command target Podman rather than Kubernetes for all terminal sessions.

To determine which mode is currently active:
```bash
$ skupper switch

podman
```

To switch back to target Kubernetes sites: `skupper switch kubernetes`

<dl><dt><strong>📌 NOTE</strong></dt><dd>

Services exposed on remote sites are not automatically available to Podman sites.
This is the equivalent to Kubernetes sites created using `skupper init --enable-service-sync false`.

To consume an exposed service on a Podman site, check that it exists using `skupper service status` on the original site and use that information to create the service on the Podman site:
```bash
$ skupper service create <name> <port>
```
</dd></dl>

## Creating a site using Skupper podman

A service network consists of Skupper sites.
This section describes how to create a site in on a Linux host using the default settings.
See [Using the Skupper CLI](../cli/index.html) for information about using the Skupper CLI to create Podman sites.

* The latest `skupper` CLI is installed.
* Podman is installed, see https://podman.io/

  By default, Podman v4 uses Netavark which works with Skupper.
  If you are using CNI, for example, if you upgrade from Podman v3, you must also install the `podman-plugins` package.
  For example, `dnf install podman-plugins` for RPM based distributions.

  **📌 NOTE**\
  CNI will be deprecated in the future in preference of Netavark.
* Podman service endpoint.

  Use `systemctl status podman.socket` to make sure the Podman API Socket is running.

  Use `systemctl --user enable --now podman.socket` to start the  Podman API Socket.

  See [Podman socket activation](https://github.com/containers/podman/blob/main/docs/tutorials/socket_activation.md) for information about enabling this endpoint.
  1. Set your session to use Skupper Podman:

     ```bash
     $ export SKUPPER_PLATFORM=podman
     ```

     To verify the `skupper` mode:

     ```bash
     $ skupper switch

     podman
     ```
  2. Create a Skupper site:

     The simplest Skupper site allows you to link to other sites, but does not support linking _to_ the current site.

     ```bash
     $ skupper init

     It is recommended to enable lingering for <username>, otherwise Skupper may not start on boot.
     Skupper is now installed for user '<username>'.  Use 'skupper status' to get more information.
     ```

     If you do not require that other sites can link to the site you are creating:

     ```bash
     $ skupper init --ingress none
     ```

     In this guide we assume you have enabled ingress using the first command.
     This allows you create tokens that allow links from every network interface on the host.

     **📌 NOTE**\
     When creating a token you can specify the ingress host.

     You can also restrict ingress to an IP address or hostname when initializing as described in the [Skupper Podman CLI reference](../podman-reference/index.html) documentation.
  3. Check the status of your site:

     ```bash
     $ skupper status
     Skupper is enabled for "<username>" with site name "<machine-name>-<username>" in interior mode. It is not connected to any other sites. It has no exposed services.
     ```

     **📌 NOTE**\
     You can only create one site per user. If you require a host to support many sites, create a user for each site.

## Linking sites using Skupper Podman

A service network consists of Skupper sites.
This section describes how to link sites to form a service network.

Linking two sites requires a single initial directional connection. However:

* Communication between the two sites is bidirectional, only the initial linking is directional.
* The choice of direction for linking is typically determined by accessibility. For example, if you are linking a virtual machine running in the cloud with a Linux host running behind a firewall, you must link from the Linux host to the cloud virtual machine because that route is accessible.

1. Generate a token on one site:

   ```bash
   $ skupper token create <filename>
   ```

   The `metadata` section of the resulting YAML file shows which interface is available for linking.

   To specify the interface, use `ifconfig` to determine the IP address of the interface you want to use.
   You can then specify that IP address when creating the token:

   ```bash
   $ skupper token create <filename> --ingress-host <IP Address>
   ```
2. Create a link from the other site:

   ```bash
   $ skupper link create <filename>
   ```

After you have linked to a network, you can check the link status:
```bash
$ skupper link status
```

## Specifying link cost

When linking sites, you can assign a cost to each link to influence the traffic flow.
By default, link cost is set to `1` for a new link.
In a service network, the routing algorithm attempts to use the path with the lowest total cost from client to target server.

* If you have services distributed across different sites, you might want a client to favor a particular target or link.
In this case, you can specify a cost of greater than `1` on the alternative links to reduce the usage of those links.

  **📌 NOTE**\
  The distribution of open connections is statistical, that is, not a round robin system.
* If a connection only traverses one link, then the path cost is equal to the link cost.
If the connection traverses more than one link, the path cost is the sum of all the links involved in the path.
* Cost acts as a threshold for using a path from client to server in the network.
When there is only one path, traffic flows on that path regardless of cost.

  **📌 NOTE**\
  If you start with two targets for a service, and one of the targets is no longer available, traffic flows on the remaining path regardless of cost.
* When there are a number of paths from a client to server instances or a service, traffic flows on the lowest cost path until the number of connections exceeds the cost of an alternative path.
After this threshold of open connections is reached, new connections are spread across the alternative path and the lowest cost path.

* You have set your Kubernetes context to a site that you want to link _from_.
* A token for the site that you want to link _to_.

1. Create a link to the service network:

   ```bash
   $ skupper link create <filename> --cost <integer-cost>
   ```

   where `<integer-cost>` is an integer greater than 1 and traffic favors lower cost links.

   **📌 NOTE**\
   If a service can be called without traversing a link, that service is considered local, with an implicit cost of `0`.

   For example, create a link with cost set to `2` using a token file named `token.yaml`:

   ```bash
   $ skupper link create token.yaml --cost 2
   ```
2. Check the link cost:

   ```bash
   $ skupper link status link1 --verbose
   ```

   The output is similar to the following:

   ```bash
    Cost:          2
    Created:       2022-11-17 15:02:01 +0000 GMT
    Name:          link1
    Namespace:     default
    Site:          default-0d99d031-cee2-4cc6-a761-697fe0f76275
    Status:        Connected
   ```
3. Observe traffic using the console.

   If you have a console on a site, log in and navigate to the processes for each server.
   You can view the traffic levels corresponding to each client.

   **📌 NOTE**\
   If there are multiple clients on different sites, filter the view to each client to determine the effect of cost on traffic.
   For example, in a two site network linked with a high cost with servers and clients on both sites, you can see that a client is served by the local servers while a local server is available.

### Exposing services on the service network from a Linux host

After creating a service network, exposed services can communicate across that network.

The general flow for working with services is the same for Kubernetes and Podman sites.

The `skupper` CLI has two options for exposing services that already exist on a host:

* `expose` supports simple use cases, for example, a host with a single service.
See [Exposing simple services on the service network](#exposing-simple-services-on-the-service-network) for instructions.
* `service create` and `service bind` is a more flexible method of exposing services, for example, if you have multiple services for a host.
See [Exposing complex services on the service network](#exposing-complex-services-on-the-service-network) for instructions.

#### Exposing simple services on the service network
This section describes how services can be enabled for a service network for simple use cases.

* A Skupper Podman site

1. Run a server, for example:

   ```bash
   $ podman run --name backend-target --network skupper --detach --rm -p 8080:8080 quay.io/skupper/hello-world-backend
   ```

   This step is not Skupper-specific, that is, this process is unchanged from standard processes for your host.
2. Create a service that can communicate on the service network:

   ```bash
   $ skupper expose [host <hostname|ip>]
   ```

   where

   * `<host>` is the name of the host where the server is running.
   For example, the name of the container if you run the server as a container.
   * `<ip>` is the IP address where the server is running

   For the example deployment in step 1, you create a service using the following command:
   ```
   $ skupper expose host backend-target --address backend --port 8080
   ```

   Options for this command include:

   * `--port <port-number>`:: Specify the port number that this service is available on the service network.
   NOTE: You can specify more than one port by repeating this option.
   * `--target-port <port-number>`:: Specify the port number of pods that you want to expose.
   * `--protocol <protocol>` allows you specify the protocol you want to use, `tcp`, `http` or `http2`
3. Create the service on another site in the service network:

   ```bash
   $ skupper service create backend 8080
   ```

#### Exposing complex services on the service network

This section describes how services can be enabled for a service network for more complex use cases.

* A Skupper Podman site

1. Run a server, for example:

   ```bash
   $ podman run --name backend-target --network skupper --detach --rm -p 8080:8080 quay.io/skupper/hello-world-backend
   ```

   This step is not Skupper-specific, that is, this process is unchanged from standard processes for your host.
2. Create a service that can communicate on the service network:

   ```bash
   $ skupper service create <name> <port>
   ```

   where

   * `<name>` is the name of the service you want to create
   * `<port>` is the port the service uses

   For the example deployment in step 1, you create a service using the following command:
   ```bash
   $ skupper service create hello-world-backend 8080
   ```
3. Bind the service to a cluster service:

   ```bash
   $ skupper service bind <service-name> <target-type> <target-name>
   ```

   where

   * `<service-name>` is the name of the service on the service network
   * `<target-type>` is the object you want to expose, `host` is the only current valid value.
   * `<target-name>` is the name of the cluster service

   For the example deployment in step 1, you bind the service using the following command:
   ```bash
   $ skupper service bind hello-world-backend host hello-world-backend
   ```

#### Consuming simple services from the service network

Services exposed on Podman sites are not automatically available to other sites.
This is the equivalent to Kubernetes sites created using `skupper init --enable-service-sync false`.

* A remote site where a service is exposed on the service network
* A Podman site

1. Log into the host as the user associated with the Skupper site.
2. Create the local service:

   ```bash
   $ skupper service create <service-name> <port number>
   ```

### Deleting a Podman site

When you no longer want the Linux host to be part of the service network, you can delete the site.

<dl><dt><strong>📌 NOTE</strong></dt><dd>

This procedure removes all containers, volumes and networks labeled `application=skupper`.

To check the labels associated with running containers:

```bash
$ podman ps -a --format "{{ID}}  {{Image}}  {{Labels}}"
```
</dd></dl>

1. Make sure you are logged in as the user that created the site:

   ```bash
   $ skupper status
   Skupper is enabled for "<username>" with site name "<machine-name>-<username>".
   ```
2. Delete the site and all podman resources (containers, volumes and networks) labeled with "application=skupper":

   ```bash
   $ skupper delete
   Skupper is now removed for user "<username>".
   ```
