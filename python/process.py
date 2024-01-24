import sys

def process_adoc_content(content):
    lines = content.splitlines()
    level_offset = 0
    processed_lines = []

    for line in lines:
        if line.startswith(':leveloffset:'):
            offset_value = line.strip().split()[-1]
            if offset_value.startswith('+'):
                level_offset += int(offset_value[1:])
            elif offset_value.startswith('-'):
                level_offset -= int(offset_value[1:])
            elif offset_value.endswith('!'):
                level_offset = 0
        elif line.startswith('='):
            heading_level = line.count('=') + level_offset
            processed_lines.append('=' * heading_level + line.lstrip('='))
        else:
            processed_lines.append(line)

    return '\n'.join(processed_lines)

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        with open(file_path, 'r') as file:
            content = file.read()
    else:
        content = sys.stdin.read()

    processed_content = process_adoc_content(content)
    print(processed_content)

if __name__ == "__main__":
    main()
