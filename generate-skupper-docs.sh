asciidoctor -a stylesheet=null.css skupper-docs/cli/index.adoc -o input/docs/cli/index.html.in

asciidoctor -a stylesheet=null.css skupper-docs/cli/tokens.adoc -o input/docs/cli/tokens.html.in

asciidoctor -a stylesheet=null.css skupper-docs/cli/podman.adoc -o input/docs/cli/podman.html.in

asciidoctor -a stylesheet=null.css skupper-docs/cli/native-security-options.adoc -o input/docs/cli/native-security-options.html.in

asciidoctor -a stylesheet=null.css skupper-docs/declarative/index.adoc -o input/docs/declarative/index.html.in

asciidoctor -a stylesheet=null.css skupper-docs/operator/index.adoc -o input/docs/operator/index.html.in

asciidoctor -a stylesheet=null.css skupper-docs/console/index.adoc -o input/docs/console/index.html.in

asciidoctor -a stylesheet=null.css skupper-docs/policy/index.adoc -o input/docs/policy/index.html.in

asciidoctor -a stylesheet=null.css skupper-docs/troubleshooting/index.adoc -o input/docs/troubleshooting/index.html.in