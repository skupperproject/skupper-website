# Function to process a single file
process_file() {
    local input_file="$1"
    local base_name=$(basename "$input_file" .adoc)
    local dir_name=$(dirname "$input_file")
    local output_file="input/docs/${dir_name}/${base_name}.md"
    input_dir=`dirname $input_file`

    mkdir -p "output/$input_dir"


    # Reduce file so that all includes are resolved and convert to asciidoc
    # requires https://github.com/opendevise/downdoc and https://github.com/asciidoctor/asciidoctor-reducer
    asciidoctor-reducer "subrepos/skupper-docs/$input_file" | python python/process.py | downdoc -o "$output_file" -

    # Extract the title from the output HTML file
    title=$(head -1 "$output_file" |sed -e 's/# //g')

    # Insert the title at the beginning of the output file
    sed -i "1s;^;---\ntitle: $title\n---\n;" "$output_file"

    # Sometimes found sed* files after above cmd.
    # rm input/docs//${dir_name}/sed*
}

# Check if at least one input file is provided
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <input-file-1> [input-file-2] ..."
    exit 1
fi

# Process each file passed as an argument
for input_file in "$@"; do
    process_file "$input_file"
done