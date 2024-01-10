import os
import argparse
import re

def add_yaml_header_and_replace_md(file_path, title):
    """
    Add YAML header to the file and replace '.md' with '.html'.
    """
    with open(file_path, 'r+') as file:
        content = file.read()
        content = content.replace('.md', '.html')
        file.seek(0, 0)
        file.write('---\n')
        file.write(f'title: {title}\n')
        file.write('---\n')
        file.write(content)

def process_directory(path):
    """
    Process each markdown file in the given directory.
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                parent_dir = os.path.basename(os.path.dirname(file_path))
                title = f"{parent_dir}: {file}"
                title = title.replace('.md', '')
                title = title.replace('_', ' ')
                
                add_yaml_header_and_replace_md(file_path, title)

def main():
    parser = argparse.ArgumentParser(description="Process markdown files in a specified directory.")
    parser.add_argument("path", type=str, help="Path to the directory containing markdown files")
    args = parser.parse_args()

    process_directory(args.path)

if __name__ == "__main__":
    main()
