import sys
import json

def ungron(flatContent):
    result = {}
    for line in flatContent.split(';'):
        if line.strip():
            key, value_str = line.split('=', 1)
            value = json.loads(value_str)
            key_parts = key.split('.')
            current_level = result
            for part in key_parts[:-1]:
                if part not in current_level:
                    current_level[part] = {}
                current_level = current_level[part]
            current_level[key_parts[-1]] = value
    return result

if __name__ == "__main__":
    # Read from file or standard input
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
        with open(fileName, 'r') as file:
            content = file.read()
    else:
        content = sys.stdin.read()

    # Ungron and print the reconstructed JSON
    originalJson = ungron(content)
    print(json.dumps(originalJson, indent=2))
