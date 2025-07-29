---
body_class: object command
refdog_links:
- title: Site linking
  url: /topics/site-linking.html
- title: Access token concept
  url: /concepts/access-token.html
- title: AccessGrant resource
  url: /resources/access-grant.html
- title: AccessToken resource
  url: /resources/access-token.html
- title: Token issue command
  url: /commands/token/issue.html
refdog_object_has_attributes: true
---

# Token redeem command

~~~ shell
skupper token redeem <file> [options]
~~~

Redeem a token file in order to create a link to a remote
site.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Examples

~~~ console
# Redeem an access token
$ skupper token redeem ~/token.yaml
Waiting for status...
Link "west-6bfn6" is active.
You can now safely delete /home/fritz/token.yaml.
~~~

## Primary options

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-file">&lt;file&gt;</h3>
<div class="attribute-type-info">string</div>
<div class="attribute-flags">required</div>
</div>
<div class="attribute-body">

The name of the token file to use.



</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-timeout">--timeout</h3>
<div class="attribute-type-info">&lt;duration&gt;</div>
</div>
<div class="attribute-body">

Raise an error if the operation does not complete in the given
period of time.

<table class="fields"><tr><th>Default</th><td><p><code>60s</code></p>
</td></table>

</div>
</div>

<div class="attribute">
<div class="attribute-heading">
<h3 id="option-link-cost">--link-cost</h3>
<div class="attribute-type-info">&lt;integer&gt;</div>
</div>
<div class="attribute-body">

The link cost to use when creating the link.

<table class="fields"><tr><th>Default</th><td>1</td><tr><th>See also</th><td><a href="{{site.prefix}}/topics/load-balancing.html">Load balancing</a></td></table>

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
