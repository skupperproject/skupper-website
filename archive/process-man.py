import os
import re
import sys

def process_markdown_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            parent_dir = os.path.basename(os.path.dirname(filepath))
            process_file(filepath, parent_dir)

def process_file(filepath, parent_dir):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    title = extract_title(lines)
    full_title = f"{title}"
    processed_lines = add_yaml_header(full_title, lower_headings(comment_out_lines(convert_links_in_see_also(lines))))

    with open(filepath, 'w') as file:
        file.writelines(processed_lines)

def extract_title(lines):
    for line in lines:
        if line.startswith("## "):
            return line.strip("# ").strip()
    return "Untitled"

def add_yaml_header(title, lines):
    yaml_header = f"---\ntitle: {title}\n---\n"
    return [yaml_header] + lines

def lower_headings(lines):
    return [re.sub(r'^(#+)', r'\1#', line) for line in lines]

def comment_out_lines(lines):
    return [f'<!-- {line} -->' if line.startswith('######') else line for line in lines]

def convert_links_in_see_also(lines):
    see_also_section = False
    updated_lines = []
    for line in lines:
        if line.strip() == "### SEE ALSO":
            see_also_section = True
        if line.startswith('### ') and line.strip() != "### SEE ALSO":
            see_also_section = False
        if see_also_section:
            line = re.sub(r'\.md', '.html', line)
            line = line.replace('(skupper.html)	 -','(index.html)')
        updated_lines.append(line)
    return updated_lines

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    process_markdown_files(directory)
