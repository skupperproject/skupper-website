---
body_class: object command
refdog_links:
- title: Platform concept
  url: /concepts/platform.html
- title: System uninstall command
  url: /commands/system/uninstall.html
refdog_object_has_attributes: true
---

# System install command

~~~ shell
skupper system install [options]
~~~

Install local system infrastructure and configure the environment.

It does the following:

- Checks the local environment for required resources and
  configuration.
- In some instances, configures the local environment.  On
  Podman, it starts the Podman API service if it is not already
  available.

**Note:** With a long-lived controller, this operation would
also start the controller as a user-scoped systemd service.

<table class="fields"><tr><th>Platforms</th><td>Kubernetes, Docker, Podman, Linux</td></table>

## Primary options

## Global options

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
