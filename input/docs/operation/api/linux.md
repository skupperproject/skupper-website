# Using the Skupper API on Linux

## Creating a site on local systems using YAML

Using YAML allows you to create and manage sites on Docker, Podman and Linux.

A typical workflow is to create a site, link sites together, and expose services to the application network.

If you require more than one site, specify a unique namespace when using  `skupper`, for example `skupper --namespace second-site ...`.

### Creating a simple site on local systems using YAML

You can use YAML to create and manage Skupper sites.

**Prerequisites**

* The `skupper` CLI is installed.

**Procedure**

1. Create a site CR YAML file named `my-site.yaml` in an empty directory, for example, `local`:

   ```yaml
   apiVersion: skupper.io/v2alpha1
   kind: Site
   metadata:
     name: my-site
   ```
   This YAML creates a site named `my-site` in the `default` namespace.

2. Create the site:
   ```bash
   skupper system setup --path ./local
   ```
   Skupper attempts to process any files in the `local` directory.
   Typically, you create all resources you require for a site before running `skupper system setup`.

3. Check the status of the site:
   ```bash
   skupper site status
   ```
   You might need to issue the command multiple times before the site is ready:
   ```
   NAME    STATUS  MESSAGE
   default Ready   OK
   ```
   You can now link this site to another site to create an application network.

There are many options to consider when creating sites using YAML, see [YAML Reference][yaml-ref], including *frequently used* options.

[yaml-ref]: https://skupperproject.github.io/refdog/resources/index.html

## Linking sites on local systems using YAML

Using a `link` resource YAML file allows you to create links between sites.
The link direction is not significant, and is typically determined by ease of connectivity. For example, if east is behind a firewall, linking from east to west is the easiest option.

Once sites are linked, services can be exposed and consumed across the application network without the need to open ports or manage inter-site connectivity.

The procedures below describe linking an existing site.
Typically, it is easier to configure a site, links and services in a set of files and then create a configured site by placing all the YAML files in a directory, for example `local` and then using the following command to

### Linking sites using a `link` resource

An alternative approach to linking sites using tokens is to create a `link` resource YAML file using the CLI, and to apply that resource to another site.

**Prerequisites**

* A local system site
* A Kubernetes site with `enable-link-access` enabled.

To link sites, you create a `link` resource YAML file on one site and apply that resource on the other site to create the link.

**Procedure**

1. On the site where you want to create a link , make sure link access is enabled:
   ```bash
   skupper site update --enable-link-access
   ```
2. Create a `link` resource YAML file:
   ```bash
   skupper link generate > <filename>
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

3. Apply the `link` resource YAML file on a local system site to create a link:
   ```bash
   mv <filename> ~/.local/share/skupper/namespaces/default/input/resources/
   skupper system setup --force
   ```
   where `<filename>` is the name of a YAML file that is saved on your local filesystem.

   The path shown is specific to the `default` namespace.
   If you are configuring a different namespace, use that name instead.

   The site is recreated and you see some of the internal resources that are not affected, for example:
   ```
   Sources will be consumed from namespace "default"
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-local-ca/tls.crt
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-local-ca/tls.key
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-local-ca/ca.crt
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-site-ca/tls.crt
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-site-ca/tls.key
   2025/03/09 22:43:14 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-site-ca/ca.crt
   2025/03/09 22:43:15 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-service-ca/tls.crt
   2025/03/09 22:43:15 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-service-ca/tls.key
   2025/03/09 22:43:15 WARN certificate will not be overwritten path=~/.local/share/skupper/namespaces/default/runtime/issuers/skupper-service-ca/ca.crt

   ```

4. Check the status of the link:
   ```bash
   skupper link status
   ```
   The output shows the link name:
   ```
   $ skupper link status
   NAME            STATUS
   link-west       Ok
   ```
   You can now expose services on the application network.
