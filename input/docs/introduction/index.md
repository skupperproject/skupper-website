# Skupper overview

Skupper is an over-the-top, multi-platform service interconnect.  Its
core purpose is to provide secure communication between application
components in disparate environments where general network
connectivity is difficult or undesirable.

## Application networks

Skupper solves communication challenges with something called an
application network (also known as a virtual application network or
VAN).  To understand the value of Skupper, it is helpful to understand
what an application network is.

An application network is made up of sites.  These are places where
you have workloads running.  They can be on different platforms and in
different parts of the world.

The sites are securely linked to form a network.  Each site has an
application router that is responsible for forwarding service traffic
across the network.

![overview-clouds](../images/overview-clouds.png)

XXX An application network connects the services in your hybrid cloud into
a virtual network so that they can communicate with each other as if
they were all running in the same site.  In this diagram, an
application network connects three services, each of which is running
in a different cloud:

- XXX What the application sees.
- XXX How it is isolated.
- XXX The routers are in user space.

## Comparing Skupper to other solutions

**VPNs** - Unlike VPNs, Skupper does not expose IP networks.  Instead,
Skupper exposes only the specific network interfaces (socket
listeners) of application components.

**Service meshes** - Unlike service meshes, Skupper does not attempt
to manage all aspects of service communication.  Instead, Skupper
focuses on flexible, multi-platform connectivity.

Compared to other solutions, Skupper is notably very easy to set up.
Because it operates over-the-top, it does not require any changes to
your existing networking.

## Components

The Skupper router, Skupper controller, and Skupper Network Observer
are indeed **key components** within the Skupper architecture, each
playing a distinct role in establishing and managing the Virtual
Application Network (VAN).

Here's an overview of these components:

### The Skupper router

The Skupper router provides the data plane of an application network.

The router is responsible for routing application connections and
requests between sites.  All inter-site communication is secured using
mutual TLS (mTLS), and the router operates without elevated
privileges, enhancing security.

The router employs a global addressing system, sharing
information about named destinations with peer routers to efficiently
determine the next nearest router for a given service.

The router also provides dynamic load balancing based on service
capacity and supports cost- and locality-aware traffic forwarding.  It
supports redundant network paths for high availability.

### The Skupper controller

*   **Skupper Controller** (often referred to as the Kubernetes control plane or operator for non-Kubernetes sites):
    *   The Skupper controller is responsible for **managing Kubernetes resources** such as Services, Deployments, Secrets, and ConfigMaps. In Skupper v2, this is achieved through a **declarative API using Custom Resource Definitions (CRDs)** for sites, links, listeners, and connectors.
    *   The **Skupper Operator** manages the Skupper infrastructure, simplifying deployment and updates of Skupper components within a Kubernetes or OpenShift cluster.
    *   In Skupper v2, there is a **unified controller** designed to combine the functionalities of the previous site and service controllers, and the "service-sync" mechanism of v1 is replaced with explicit listeners and connectors.
    *   The controller also handles aspects like **policy control**, allowing cluster administrators to restrict Skupper usage.
    * The API!
    * Configuring the data plane (the router)

### The Skupper CLI

The Skupper Command Line Interface (CLI) is a **primary tool for interacting with and administering Skupper deployments**, allowing users to manage various aspects of the Virtual Application Network (VAN). It is designed to provide a consistent experience across different platforms, including Kubernetes, container engines like Podman and Docker, and bare-metal hosts.

Here's a detailed look at the Skupper CLI:

*   **Core Functionality for Site Management and Connectivity:**
    *   **Site Configuration:** Commands like `skupper init` are used to **create a Skupper site** and establish a Certificate Authority (CA) without requiring elevated privileges. In Skupper v2, configuration parameters are moving to standard Kubernetes resources.
    *   **Site Linking:** The CLI facilitates linking Skupper sites. `skupper token create` generates **credentials (tokens)**, which are then used with `skupper link create` to establish a secure connection between sites. These tokens are typically single-use and time-limited, though options exist for unlimited use.
    *   **Service Exposure:** `skupper expose` makes services available across the Skupper network. It **does not create an L3 connection** between namespaces but rather translates service protocols (TCP, HTTP1, HTTP2) into AMQP for secure inter-site communication. For more complex scenarios, `skupper service create` defines a service, and `skupper service bind` links that service to a cluster service (e.g., deployment, statefulset).
    *   **Load Balancing:** The CLI supports configuring load balancing. For instance, `skupper service create` with `--mapping tcp` can enable **connection-level load balancing** instead of HTTP load balancing. Multiple `skupper service bind` commands for a single service can also be used for load balancing.
    *   **Network Status and Monitoring:** Administrator-level network monitoring is available through the CLI. Commands like `skupper network status` provide an overview of the Skupper network.

*   **Troubleshooting and Debugging:**
    *   The CLI offers several commands for **diagnosing issues**. These include `skupper status` (for site status), `skupper service status -v` (for exposed services), and `skupper debug events` (for Skupper events).
    *   The `skupper debug dump` command is crucial, creating a tarball that includes logs, configuration, and Kubernetes resource YAML for Skupper-related components, aiding in issue reporting.

*   **Evolution with Skupper v2 and Non-Kubernetes Platforms:**
    *   **Revamped and CRD-based:** Skupper v2 introduces a **revamped CLI that is CRD-based and blocking**, replacing the previous "service-sync" mechanism with explicit listeners and connectors.
    *   **Non-Kubernetes Support:** For non-Kubernetes environments like Podman and Linux (using systemd), new commands such as `skupper system install`, `skupper system apply`, `skupper system start`, and `skupper system reload` are being developed to manage Skupper infrastructure. The `localhost` is often the default host value for `skupper connector create` on non-Kube platforms.
    *   **YAML Integration:** The CLI is designed to **generate and apply YAML configurations** for resources like sites, links, listeners, and connectors.
    *   **Improvements in v2:** Skupper v2 aims for a simplified CLI using the new model, with an OpenShift console plugin offering similar capabilities. There have been efforts to improve CLI usability, including a "big CLI redesign" in 2024.

*   **Usability and Development Considerations:**
    *   The CLI integrates with Kubernetes contexts, and understanding `kubectl` or `oc` contexts is important when working with multiple clusters.
    *   Discussions around CLI design emphasize consistency, conventional naming, and avoiding arbitrary differences. For example, the utility of a `skupper token status` command in v2 has been debated, focusing on whether it should indicate if a token is valid and redeemable.
    *   There is an ongoing effort to improve documentation for CLI commands, including overviews of concepts, resources, and command usage.

### The Skupper Network Observer

*   **Skupper Network Observer** (previously known as vFlow or Vanflow/flow-collector):
    *   This component is responsible for **publishing and collecting events and metrics** within the Skupper network. It plays a crucial role in **observability**.
    *   It **ingests events** from protocol observers within the Skupper router (e.g., HTTP/1 and HTTP/2 observers) and **exposes them as Prometheus metrics**. These metrics are then used in the Skupper console for network monitoring.
    *   In Skupper v2, observability components are designed to be **deployed separately from site components**, offering more flexibility.

Beyond these core components, a Skupper deployment also involves **Skupper sites** (representing deployment locations like Kubernetes clusters or Podman environments), **links** (connecting sites), **listeners** (enabling a site to receive connections for a service), and **connectors** (allowing a service on one site to connect to a service on another).
