cd scripts

# which directory should docs land in?
docs_dir=docs2

# clear temporary directory 
rm -r antora_build/*

# clear input directory

rm -r ../input/$docs_dir/*

# generate html in temporary directory (antora_build)
antora --fetch docs-playbook.yml

# copy html to input (removing skupper level)
cp -r antora_build/skupper/latest/* ../input/$docs_dir

# rename all html files to *.in
shopt -s globstar
for file in ../input/$docs_dir/**/*.html; do
  mv "$file" "${file%.abc}.in"
done
