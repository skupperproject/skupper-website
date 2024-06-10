 python external/skupper-docs/scripts/convert-all.py ./convert-adoc.sh external/skupper-docs/.github/workflows/asciidoc-convert-check.yml

# ./convert-adoc.sh \
# cli/index.adoc \
# cli/tokens.adoc \
# cli/podman.adoc \
# cli/native-security-options.adoc \
# yaml/index.adoc \
# operator/index.adoc \
# console/index.adoc \
# policy/index.adoc \
# troubleshooting/index.adoc \
# overview/connectivity.adoc \
# overview/glossary.adoc \
# overview/index.adoc \
# overview/resources.adoc \
# overview/routing.adoc \
# overview/security.adoc \
# kubernetes/deployment-concerns.adoc

cp -r external/skupper-docs/images/ input/docs/

# To process nested numbered lists
python python/nested-numbers.py input/docs/operator/

# To workaround transform interpreting {{.ID}} as a var:

sed -i 's/.ID}} /{.ID}}} /g' input/docs/cli/podman.md
sed -i 's/ {{.Image/ {{{.Image}/g' input/docs/cli/podman.md
sed -i 's/ {{.Labels/ {{{.Labels}/g' input/docs/cli/podman.md

# To workaround https://github.com/skupperproject/skupper-website/issues/81
sed -i 's/   | /| /g' input/docs/kubernetes/deployment-concerns.md
