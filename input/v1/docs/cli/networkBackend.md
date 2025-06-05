---
title: Configuring Podman networkBackend for Skupper
---
# Configuring Podman networkBackend for Skupper

By default, Podman v4 and later use Netavark which works with Skupper.
However, if you upgraded from an earlier version of Podman, you might need to configure Podman to use Netavark.

If you are using CNI, for example, if you upgrade from Podman v3, you must also install the `podman-plugins` package.
For example, `dnf install podman-plugins` for RPM based distributions.

**📌 NOTE**\
CNI will be deprecated in the future in preference of Netavark.

1. To install `netavark` on rpm based Linux, for example, RHEL8:

   ```
   $ sudo dnf install netavark
   ```
2. Configure podman to use `netavark` by making sure the following lines exist in the `/etc/containers/containers.conf` file:

   ```
   [network]
   network_backend = "netavark"
   ```
3. Confirm that `netavark` is configured as the podman network backend:

   ```
   $ podman info --format {{{.Host.NetworkBackend}}}
   ```

See [Using Skupper Podman](../cli/podman.html)[Using Skupper Podman].
