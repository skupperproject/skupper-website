python external/skupper-docs/scripts/convert-all.py ./convert-adoc.sh external/skupper-docs/published-adoc.txt

cp -r external/skupper-docs/images/ input/docs/

# To process nested numbered lists
python python/nested-numbers.py input/docs/operator/

# To workaround transform interpreting {{.ID}} as a var:

sed -i 's/.ID}} /{.ID}}} /g' input/docs/cli/podman.md
sed -i 's/ {{.Image/ {{{.Image}/g' input/docs/cli/podman.md
sed -i 's/ {{.Labels/ {{{.Labels}/g' input/docs/cli/podman.md
sed -i 's/ {{.Host.NetworkBackend/ {{{.Host.NetworkBackend}/g' input/docs/cli/podman.md
sed -i 's/ {{.Host.NetworkBackend/ {{{.Host.NetworkBackend}/g' input/docs/cli/networkBackend.md


# To workaround https://github.com/skupperproject/skupper-website/issues/81
sed -i 's/   | /| /g' input/docs/kubernetes/deployment-concerns.md
