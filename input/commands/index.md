---
title: Commands
refdog_links:
  - title: Concepts
    url: /concepts/index.html
  - title: Resources
    url: /resources/index.html
---

# Skupper CLI commands

## Command index

<div class="index">

#### Site operations

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/site/index.html">Site</a></th><td>Overview of site commands</td></tr>
<tr><th><a href="{{site.prefix}}/commands/site/create.html">Site create</a></th><td>Create a site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/site/update.html">Site update</a></th><td>Change site settings</td></tr>
<tr><th><a href="{{site.prefix}}/commands/site/delete.html">Site delete</a></th><td>Delete a site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/site/status.html">Site status</a></th><td>Display the status of a site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/site/generate.html">Site generate</a></th><td>Generate a Site resource</td></tr>
</table>

#### Site linking

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/token/index.html">Token</a></th><td>Overview of token commands</td></tr>
<tr><th><a href="{{site.prefix}}/commands/token/issue.html">Token issue</a></th><td>Issue a token file redeemable for a link to the current site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/token/redeem.html">Token redeem</a></th><td>Redeem a token file in order to create a link to a remote site</td></tr>
</table>

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/link/index.html">Link</a></th><td>Overview of link commands</td></tr>
<tr><th><a href="{{site.prefix}}/commands/link/update.html">Link update</a></th><td>Change link settings</td></tr>
<tr><th><a href="{{site.prefix}}/commands/link/delete.html">Link delete</a></th><td>Delete a link</td></tr>
<tr><th><a href="{{site.prefix}}/commands/link/status.html">Link status</a></th><td>Display the status of links in the current site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/link/generate.html">Link generate</a></th><td>Generate a Link resource for use in a remote site</td></tr>
</table>

#### Service exposure

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/listener/index.html">Listener</a></th><td>Overview of listener commands</td></tr>
<tr><th><a href="{{site.prefix}}/commands/listener/create.html">Listener create</a></th><td>Create a listener</td></tr>
<tr><th><a href="{{site.prefix}}/commands/listener/update.html">Listener update</a></th><td>Update a listener</td></tr>
<tr><th><a href="{{site.prefix}}/commands/listener/delete.html">Listener delete</a></th><td>Delete a listener</td></tr>
<tr><th><a href="{{site.prefix}}/commands/listener/status.html">Listener status</a></th><td>Display the status of listeners in the current site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/listener/generate.html">Listener generate</a></th><td>Generate a Listener resource</td></tr>
</table>

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/connector/index.html">Connector</a></th><td>Overview of connector commands</td></tr>
<tr><th><a href="{{site.prefix}}/commands/connector/create.html">Connector create</a></th><td>Create a connector</td></tr>
<tr><th><a href="{{site.prefix}}/commands/connector/update.html">Connector update</a></th><td>Update a connector</td></tr>
<tr><th><a href="{{site.prefix}}/commands/connector/delete.html">Connector delete</a></th><td>Delete a connector</td></tr>
<tr><th><a href="{{site.prefix}}/commands/connector/status.html">Connector status</a></th><td>Display the status of connectors in the current site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/connector/generate.html">Connector generate</a></th><td>Generate a Connector resource</td></tr>
</table>

#### System operations

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/system/index.html">System</a></th><td>Overview of system commands</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/install.html">System install</a></th><td>Install local system infrastructure and configure the environment</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/uninstall.html">System uninstall</a></th><td>Remove local system infrastructure</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/start.html">System start</a></th><td>Start the Skupper router for the current site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/stop.html">System stop</a></th><td>Stop the Skupper router for the current site</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/reload.html">System reload</a></th><td>Reload the site configuration</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/apply.html">System apply</a></th><td>Create or update resources using files or standard input</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/delete.html">System delete</a></th><td>Delete resources using files or standard input</td></tr>
<tr><th><a href="{{site.prefix}}/commands/system/generate-bundle.html">System generate-bundle</a></th><td>Generate a self-contained site bundle for use on another machine</td></tr>
</table>

#### Debugging operations

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/debug/index.html">Debug</a></th><td>Overview of debug commands</td></tr>
<tr><th><a href="{{site.prefix}}/commands/debug/check.html">Debug check</a></th><td>Run diagnostic checks</td></tr>
<tr><th><a href="{{site.prefix}}/commands/debug/dump.html">Debug dump</a></th><td>Generate a debug dump file</td></tr>
</table>

#### Other operations

<table class="objects">
<tr><th><a href="{{site.prefix}}/commands/version.html">Version</a></th><td>Display versions of Skupper components</td></tr>
</table>

</div>

## Overview

Skupper uses the `skupper` command as its command-line interface (CLI)
for creating and operating Skupper networks.

#### Capabilities

In its primary role, the Skupper CLI is a thin layer on top of the
standard Skupper resources.  Its job is to configure sites, listeners,
and connectors.  It additionally provides commands for site linking,
system operation, and troubleshooting.

- **Resource configuration:** Create, update, and delete Skupper
  resources.
- **Resource status:** Display the current state of Skupper resources.
- **Resource generation:** Produce Skupper resources in YAML or JSON
  format.
- **Site linking:** Use tokens to set up site-to-site links.
- **System operation:** Install and operate Skupper runtime
  components.
- **Troubleshooting:** Use debugging tools to identify and fix
  problems.

By design, the Skupper CLI does not do everything the Skupper
resources can do.  We encourage you to use the resources directly for
advanced use cases.

#### Usage

~~~
skupper [command] [subcommand] [options]
~~~

- `command`: A resource type or functional area.
- `subcommand`: The specific operation you want to perform.
- `options`: Additional arguments that change the operation's
  behavior.

#### Context

Skupper commands operate with a current platform and namespace (with a
few exceptions).  On Kubernetes, there is additionally a current
kubeconfig and context.  You can use CLI options or environment
variables to change the current selection.

<div class="data-table">

| Context | Default | CLI option | Environment variable |
|-|-|-|-|
| Platform | `kubernetes` | `--platform` | `SKUPPER_PLATFORM` |
| Namespace | _From kubeconfig_ | `--namespace` | _None_ |
| Kubeconfig context | _From kubeconfig_ | `--context` | _None_ |
| Kubeconfig | `~/.kube/config` | `--kubeconfig` | `KUBECONFIG` |

</div>

On Docker, Podman, and Linux, the current namespace defaults to
`default`.

#### Blocking

On Kubernetes, resource operations block until the desired outcome is
achieved, an error occurs, or the timeout is exceeded.  You can change
the wait condition and the timeout duration using the `--wait` and
`--timeout` options.

- Site and link operations block until the resource is ready.
- Listener and connector operations block until the resource is
  configured.
- All resource delete operations block until deletion is complete.

On Docker, Podman, and Linux, resource operations do not block.
Instead, they place the resources in the input location.  Changes are
applied when the user invokes `skupper system reload`.

#### Errors

The Skupper CLI returns a non-zero exit code indicating an error when:

* User input is invalid.
* Referenced resources are not found.
* The operation fails or times out.

#### Resource commands

~~~
skupper <resource-type> create <resource-name> [options]
skupper <resource-type> update <resource-name> [options]
skupper <resource-type> delete <resource-name> [options]
skupper <resource-type> status [resource-name] [options]
skupper <resource-type> generate <resource-name> [options]
~~~

These commands operate on Skupper sites, links, listeners, and
connectors.

Resource properties are set using one or more `--some-key some-value`
command-line options.  YAML resource options in camel case (`someKey`)
are exposed as hyphenated names (`--some-key`) when used as options.

The `create`, `update`, and `delete` commands control the lifecycle of
Skupper resources and configure their properties.

The `status` commands display the current state of resources.  If no
resource name is specified, they list the status of all resources of
the given type.

The `generate` commands produce Skupper resources as YAML or JSON
output.  They are useful for directing the output to files or other
tools.

#### Token commands

~~~
skupper token issue <token-file> [options]
skupper token redeem <token-file> [options]
~~~

These commands use access tokens to create links between sites.

The `token issue` command creates an access token for use in remote
sites.  The `token redeem` command uses an access token to create a
link to the issuing site.

#### System commands

~~~
skupper system install [options]
skupper system uninstall [options]
skupper system start [options]
skupper system stop [options]
skupper system reload [options]
skupper system status [options]
skupper system apply [options]
skupper system delete [options]
skupper system generate-bundle [options]
~~~

These commands configure and operate the Skupper runtime components
for Docker, Podman, and Linux sites.

#### Debug commands

~~~
skupper debug check [options]
skupper debug dump [options]
~~~

These commands help you troubleshoot problems.

#### Version command

~~~
skupper version
~~~

The `version` command displays the versions of Skupper components.

<!-- ## Hello World using the CLI -->

<!-- ~~~ console -->
<!-- # Get the CLI -->

<!-- $ curl https://skupper.io/install.sh | sh -->

<!-- # West -->

<!-- $ export KUBECONFIG=~/.kube/config-west -->
<!-- $ kubectl apply -f https://skupper.io/install.yaml -->
<!-- $ kubectl create deployment frontend --image quay.io/skupper/hello-world-frontend -->

<!-- $ skupper site create --enable-link-access -->
<!-- $ skupper listener create backend 8080 -->
<!-- $ skupper token issue ~/token.yaml -->

<!-- # East -->

<!-- $ export KUBECONFIG=~/.kube/config-east -->
<!-- $ kubectl apply -f https://skupper.io/install.yaml -->
<!-- $ kubectl create deployment backend --image quay.io/skupper/hello-world-backend --replicas 3 -->

<!-- $ skupper site create -->
<!-- $ skupper connector create backend 8080 -->
<!-- $ skupper token redeem ~/token.yaml -->
<!-- ~~~ -->
