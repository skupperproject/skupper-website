rm -r docs2/*
antora --fetch docs-playbook.yml

cp -r antora_build/skupper/* docs2

shopt -s globstar
for file in docs2/**/*.html; do
  mv "$file" "${file%.abc}.in"
done
