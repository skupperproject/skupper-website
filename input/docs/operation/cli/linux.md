# Using the Skupper CLI with Linux

## Creating a site on a local system using the CLI

Using the skupper command-line interface (CLI) allows you to create and manage Skupper sites from the context of the current user.

A typical workflow is to create a site, link sites together, and expose services to the application network.

A *local system* includes Docker, Podman or Linux system.

If you require more than one site, specify a unique namespace when using  `skupper`, for example `skupper --namespace second-site ...`.

### Checking the Skupper CLI and environment

Installing the skupper command-line interface (CLI) provides a simple method to get started with Skupper.

1. Follow the instructions for [Installing Skupper](https://skupper.io/releases/index.html).

2. Verify the installation.
   ```bash
   skupper version

   COMPONENT               VERSION
   cli                     {{skupper_version}}
   ```

3. For podman sites:

   Make sure the Podman socket is available. To enable it:
   ```bash
   systemctl --user enable --now podman.socket
   ```
   Enable lingering to ensure the site persists over logouts:
   ```bash
   loginctl enable-linger <username>
   ```

### Creating a simple site using the CLI on local systems

**Prerequisites**

* The `skupper` CLI is installed.

**Procedure**

1. Set the `SKUPPER_PLATFORM` for type of site you want to install:

   * `podman`
   * `docker`
   * `linux`

2. Create a site:

   ```bash
   skupper site create <site-name>
   ```
   For example:
   ```bash
   skupper site create my-site

   Waiting for status...
   Site "my-site" is ready.
   ```
   While the site is created, the site is not running at this point.
   To run the site:
   ```bash
   skupper system setup
   ```

  📌 NOTE: On non-Kubernetes sites, you can create multiple sites per-user by specifying a *namespace*.

### Deleting a site using the CLI on local systems

**Prerequisites**

* The `skupper` CLI is installed.

**Procedure**

1. Enter the following command to delete a site:
   ```bash
   skupper system teardown
   ```

## Linking sites on local systems using the Skupper CLI

Using the Skupper command-line interface (CLI) allows you to create links between sites.
The link direction is not significant, and is typically determined by ease of connectivity. For example, if east is behind a firewall, linking from east to west is the easiest option.

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.


A *local system* includes Docker, Podman or Linux system.

In this release, the CLI does not support issuing or redeeming tokens.
In this release, the CLI does not support generating `link` resource files.

To link a local system site to a Kubernetes site, see [Linking sites on local systems using YAML](../system-yaml/site-linking.html)

[cli-ref]: https://skupperproject.github.io/refdog/commands/index.html

## Exposing services on the application network using the CLI

After creating an application network by linking sites, you can expose services from one site using connectors and consume those services on other sites using listeners.
A *routing key* is a string that matches one or more connectors with one or more listeners.
For example, if you create a connector with the routing key `backend`, you need to create a listener with the routing key `backend` to consume that service.

This section assumes you have created and linked at least two sites.

### Creating a connector using the CLI

A connector binds a local workload to listeners in remote sites.
Listeners and connectors are matched using routing keys.

For more information about connectors see [Connector concept][connector]

**Prerequisites**

* The `skupper` CLI is installed.
* The `SKUPPER_PLATFORM` environment variable is set to one of * `podman`,`docker` or `linux`.

**Procedure**

1. Create a server that you want to expose on the network.
   For example, run a HTTP server on port 8080.

2. Create a connector:
   ```bash
   skupper connector create <name> <port> [--routing-key <name>]
   ```
   For example:

   ```bash
   skupper connector create my-server 8080 --host localhost
   ```
3. Check the connector status:
   ```bash
   skupper connector status
   ```

   For example:

   ```
   $ skupper connector status
   NAME		STATUS	ROUTING-KEY	HOST		PORT
   my-server	Ok	my-server	localhost	8081

   ```
   **📌 NOTE**
   By default, the routing key name is set to the name of the connector.
   If you want to use a custom routing key, set the `--routing-key` to your custom name.

   Apply the configuration using:
   ```bash
   skupper system reload
   ```

There are many options to consider when creating connectors using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

### Creating a listener using the CLI

A listener binds a local connection endpoint to connectors in remote sites.
Listeners and connectors are matched using routing keys.

**Prerequisites**

* The `skupper` CLI is installed.
* The `SKUPPER_PLATFORM` environment variable is set to one of * `podman`,`docker` or `linux`.

**Procedure**

1. Identify a connector that you want to use.
   Note the routing key of that connector.

2. Create a listener:
   ```bash
   skupper connector create <name> <port> [--routing-key <name>]
   ```
   For example:
   ```
   $ skupper listener create my-server 8080
   File written to /home/user/.local/share/skupper/namespaces/default/input/resources/Listener-backend.yaml
   ```
   Apply the configuration using:
   ```bash
   skupper system reload
   ```

3. Check the listener status:
   ```bash
   skupper listener status
   ```

   For example:

   ```
   $ skupper listener status
   NAME		STATUS	ROUTING-KEY	HOST		PORT
   my-server	Ok	my-server	localhost	8081

   ```

   **📌 NOTE**
   There must be a matching connector for the service to operate.
   By default, the routing key name is the listener name.
   If you want to use a custom routing key, set the `--routing-key` to your custom name.

There are many options to consider when creating connectors using the CLI, see [CLI Reference][cli-ref], including *frequently used* options.

[connector]: https://skupperproject.github.io/refdog/concepts/connector.html
[listener]: https://skupperproject.github.io/refdog/concepts/listener.html
