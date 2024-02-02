import sys

def process_adoc_content(content):
    lines = content.splitlines()
    level_offset = 0
    processed_lines = []
    in_block = False  # Flag to indicate if we are inside a block

    for line in lines:
        if line.startswith('===='):
            in_block = not in_block
            processed_lines.append(line)
        elif line.startswith(':leveloffset:'):
            if not in_block:  # Process leveloffset only outside of blocks
                offset_value = line.strip().split()[-1]
                if offset_value.startswith('+'):
                    level_offset += int(offset_value[1:])
                elif offset_value.startswith('-'):
                    level_offset -= int(offset_value[1:])
                elif offset_value.endswith('!'):
                    level_offset = 0
        elif line.startswith('=') and not in_block:
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
