import json
import sys

def gronify(data, parent_key='json', indent=2):
    if isinstance(data, dict):
        for k, v in data.items():
            key = f'{parent_key}.{k}' if parent_key else k
            gronify(v, key, indent)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            key = f'{parent_key}[{i}]' if parent_key else f'[{i}]'
            gronify(v, key, indent)
    else:
        print(f'{parent_key} = {json.dumps(data, indent=indent)}')

if __name__ == '__main__':
    # Example usage reading JSON from a file
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]

    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            gronify(json_data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
