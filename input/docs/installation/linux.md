# Installing Skupper on Linux

Before you can create a site on Linux (including Docker and Podman
sites), you must install the Skupper system resources into your user
account.

#### Prerequisites

- A user account on a Linux system
- The Skupper CLI (see [Installing the Skupper CLI](../installation/cli.html))

#### Procedure

Use the `skupper system install` command:

~~~ shell
skupper system install
~~~

The command uses your configured platform (set by the
`SKUPPER_PLATFORM` environment variable or the [`--platform`
option][option-platform]) to check the local environment and set up
the required resources.

[option-platform]: {{skupper_site_url}}/commands/system/install.html#option-platform

After installation, you can create sites using the Skupper API or CLI:

- [Creating a site using the API](../operation/api/site-configuration.html)
- [Creating a site using the CLI](../operation/cli/site-configuration.html)
