import os
import sys
import json

def json_to_directory(json_data, base_path='.'):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            key_path = os.path.join(base_path, str(key))
            os.makedirs(key_path, exist_ok=True)
            json_to_directory(value, key_path)
    elif isinstance(json_data, list):
        for i, value in enumerate(json_data):
            item_path = os.path.join(base_path, str(i))
            os.makedirs(item_path, exist_ok=True)
            json_to_directory(value, item_path)
    else:
        with open(os.path.join(base_path, 'data.txt'), 'w') as file:
            file.write(str(json_data))

def main():
    json_file_path = sys.argv[1] if len(sys.argv) > 1 else '-'

    try:
        if json_file_path == '-':
            # Read JSON from stdin
            json_data = json.load(sys.stdin)
        else:
            # Read JSON from file
            with open(json_file_path, 'r') as file:
                json_data = json.load(file)

        json_to_directory(json_data)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
