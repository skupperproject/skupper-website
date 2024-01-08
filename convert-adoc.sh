# Function to process a single file
process_file() {
    local input_file="$1"
    local base_name=$(basename "$input_file" .adoc)
    local dir_name=$(dirname "$input_file")
    local output_file="input/docs/${dir_name}/${base_name}.html.in"

    # Run asciidoctor to convert the input file to HTML
    asciidoctor -a stylesheet=null.css "skupper-docs/$input_file" -o "$output_file"

    # Extract the title from the output HTML file
    local title=$(cat "$output_file" | htmlq -t h1)

    # Insert the title at the beginning of the output file
    sed -i "1s;^;---\ntitle: $title\n---\n;" "$output_file"
    rm input/docs//${dir_name}/sed*
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