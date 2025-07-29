---
body_class: object command
refdog_links:
- title: Debug dumps
  url: /topics/debug-dumps.html
refdog_object_has_attributes: true
---

# Debug dump command

~~~ shell
skupper debug dump [file] [options]
~~~

Generate a debug dump file.  Debug dumps collect the details of
a site so another party can identify and fix a problem.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# Generate a dump file
$ skupper debug dump
Debug dump file: /home/fritz/skupper-dump-west-2024-12-09.tar.gz

# Generate a dump file to a particular path
$ skupper debug dump /tmp/abc.tar.gz
Debug dump file: /tmp/abc.tar.gz
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-file">[file]</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">optional</div>
</div>
<div class="attribute-body">

The name of the file to generate.

The command exits with an error if the file already exists.

<table class="fields"><tr><th>Default</th><td><p><code>skupper-dump-&lt;site-name&gt;-&lt;date&gt;.tar.gz</code></p>
</td></table>

</div>
</div>

## Global options

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-context">--context</h3>
<div class="attribute-type-info">&lt;name&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the kubeconfig context.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">Kubernetes kubeconfigs</a></td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-kubeconfig">--kubeconfig</h3>
<div class="attribute-type-info">&lt;file&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the path to the kubeconfig file.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes</td><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/">Kubernetes kubeconfigs</a></td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-namespace">--namespace</h3>
<div class="attribute-type-info">(-n) &lt;name&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the current namespace.

<table class="fields"><tr><th>See also</th><td><a href="https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/">Kubernetes namespaces</a>, <a href="{{site.prefix}}/topics/system-namespaces.html">System namespaces</a></td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-platform">--platform</h3>
<div class="attribute-type-info">&lt;platform&gt;</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Set the Skupper platform.

<!-- You can also use the `SKUPPER_PLATFORM` environment variable. -->

<table class="fields"><tr><th>Default</th><td><p><code>kubernetes</code></p>
</td><tr><th>Choices</th><td><table class="choices"><tr><th><code>kubernetes</code></th><td><p>Kubernetes</p>
</td></tr><tr><th><code>docker</code></th><td><p>Docker</p>
</td></tr><tr><th><code>podman</code></th><td><p>Podman</p>
</td></tr><tr><th><code>linux</code></th><td><p>Linux</p>
</td></tr></table></td><tr><th>See also</th><td><a href="{{site.prefix}}/concepts/platform.html">Platform concept</a></td></table>

</div>
</div>

<div class="attribute collapsed">
<div class="attribute-heading">
<h3 id="option-help">--help</h3>
<div class="attribute-type-info">(-h) boolean</div>
<div class="attribute-flags">global</div>
</div>
<div class="attribute-body">

Display help and exit.



</div>
</div>
