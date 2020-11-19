antora docs-playbook.yml

rm -r _/

shopt -s globstar
for file in skupper/**/*.html; do
  mv "$file" "${file%.abc}.in"
done
