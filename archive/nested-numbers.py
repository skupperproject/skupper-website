import os
import re
import argparse

def replace_numbering(file_path):
    with open(file_path, 'r') as file:
        contents = file.readlines()

    # Regular expression for indented numbered list
    pattern = re.compile(r'^(\s+)(\d+)\.\s')
    in_code_block = False
    skip_next = False  # Flag to skip numbering change for the first non-blank line after a code block

    updated_contents = []
    for line in contents:
        if line.strip() == "----":  # Identify the start/end of a code block
            in_code_block = not in_code_block
            skip_next = True  # Activate skip flag after ending a code block
            updated_contents.append(line)
            continue

        if in_code_block:
            updated_contents.append(line)
            continue

        if skip_next and line.strip():  # Check for non-blank line
            skip_next = False  # Reset the skip flag for the first non-blank line
            updated_contents.append(line)
            continue
        elif skip_next:  # If line is blank while skip flag is active
            updated_contents.append(line)
            continue

        match = pattern.match(line)
        if match:
            # Convert number to alphabetic character
            indention, number = match.groups()
            alpha_char = chr(96 + int(number))  # 'a' starts at ASCII 97
            # Inserting a newline character before the alphabetic character
            new_line = f"\n{indention}{alpha_char}. {line[match.end():]}"
            updated_contents.append(new_line)
        else:
            updated_contents.append(line)

    with open(file_path, 'w') as file:
        file.writelines(updated_contents)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                replace_numbering(os.path.join(root, file))

def main(path):
    if os.path.isdir(path):
        process_directory(path)
    elif os.path.isfile(path) and path.endswith('.md'):
        replace_numbering(path)
    else:
        print("The path is not a valid directory or markdown file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace indented numbered lists in markdown files with alphabetic numbering.")
    parser.add_argument("path", help="Directory or markdown file path.")
    args = parser.parse_args()

    main(args.path)
