# Using Skupper with OpenShift

## Prerequisites

* You must have [access to an OpenShift cluster][start].
* You must [install the OpenShift command-line tool (`oc`)](https://docs.openshift.com/container-platform/4.7/cli_reference/openshift_cli/getting-started-cli.html#installing-openshift-cli).

**Note:** The `oc` command is a `kubectl` equivalent with extensions
for OpenShift.  The Skupper getting started guide uses `kubectl` for
the core Kubernetes operations, but you can safely use `oc` instead.
For example, `kubectl create namespace west` and `oc create namespace
west` have the same effect.

[start]: https://www.openshift.com/try
[installation]: https://docs.openshift.com/container-platform/4.7/cli_reference/openshift_cli/getting-started-cli.html#installing-openshift-cli

## Cluster access

### Using the command line

Use the `oc login` command with the URL of your OpenShift cluster and
your username.

    oc login openshift.example.net:6443 -u alice

The command will prompt you for any needed credentials or login
details.

See the [instructions for logging in][logging-in] for more
information.

[logging-in]: https://docs.openshift.com/container-platform/4.7/cli_reference/openshift_cli/getting-started-cli.html#cli-logging-in_cli-developer-commands

### Using the console

You can also use the OpenShift console to generate an `oc login`
command that you can paste into your console session.

1. Navigate to the OpenShift console and log in.
1. Select the menu for your account in the top right of the page.
1. Select **Copy Login Command**.  Follow the prompts until you have an
   `oc login` command to copy.
1. Paste the `oc login` command into your console session.

## More information

* [OpenShift website](https://www.openshift.com/)
* [OpenShift documentation](https://docs.openshift.com/)
* [OpenShift CLI getting started guide](https://docs.openshift.com/container-platform/4.7/cli_reference/openshift_cli/getting-started-cli.html)
* [OKD website](https://www.okd.io/)
* [OKD documentation](https://docs.okd.io/)
