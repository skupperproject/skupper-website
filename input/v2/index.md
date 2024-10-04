# Skupper v2

<!-- A major improvement to Skupper is coming soon. -->

<!-- ## What's in v2? -->

<!-- <\!-- We've had 1.x for over two years. -\-> -->

<!-- ## Why the big change? -->

<!-- - CRDs! -->
<!-- - Uniform model.  Declarative API.  Everything goes through the CRDs. -->
<!--   - New CLI that follows the new model.  The CLI isn't doing anything clever.  It's just a convenient tool for producing CRs. -->
<!--   - Same model and CRDs across site types (Kubernetes, Docker, Podman, and Systemd sites) -->
<!--   - GitOps -->
<!--   - Integrations -->
<!-- - A uniform model and API across platforms and interfaces. -->

<!-- - Service exposure model! -->
<!-- - (?) Attached connectors - Tracking pods in namespaces other than that of the site -->
<!-- - No more service sync -->

<!-- - A new controller impl. -->
<!-- - Combine site and service controllers. -->
<!-- - Avoiding site recreation! -->

<!-- - HA routers! -->
<!-- - Faster routers! -->

<!-- - Gordon's preso -->
<!-- - My planning docs -->

<!-- - Observability decoupled -->

<!-- ## Important to know -->

<!-- 1.x is _not_ backward compatible with 2. -->
<!-- We are developing tooling to migrate 1.x config to 2.x config. -->

<!-- | 1.x | 2.x | -->
<!-- |-|-| -->
<!-- | Gateways | Docker, Podman, and Systemd sites | -->

<!-- ## When will it be available? -->

<!-- ## Try it now -->

<!-- Feedback requested! -->

~~~
kubectl apply -f https://skupper.io/v2/install.yaml
~~~

~~~
curl https://skupper.io/install.sh | sh -s -- --version 2.0.0-preview-1
~~~

<!-- Things are still changing! -->
<!-- This is preview 1.  Another preview is planned for the end of October. -->
<!-- We are aiming for a 2.0 release in November! -->

<!-- <https://skupperproject.github.io/refdog/> -->
