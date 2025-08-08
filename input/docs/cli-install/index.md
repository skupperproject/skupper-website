# Installing the Skupper CLI

With Skupper v2, you can install and configure Skupper on Kubernetes without the Skupper CLI.
You don't need the CLI to use Skupper.
You can use custom resources directly.

On Linux or the Mac, you can use the [install script][install-script]
to download and extract the command:

<div class="code-label">Linux or Mac</div>

~~~ shell
curl https://skupper.io/install.sh | sh
~~~

The script installs the command under your home directory.  It prompts
you to add the command to your path if necessary.

[install-script]: https://github.com/skupperproject/skupper-website/blob/main/input/install.sh

## More resources

* [Skupper releases at GitHub](https://github.com/skupperproject/skupper/releases)
* [Skupper images at Quay.io](https://quay.io/organization/skupper)
