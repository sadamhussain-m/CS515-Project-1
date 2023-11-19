import json
import sys

def flatten_json(json_obj, prefix=""):
    flat_dict = {}
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            flat_key = f"{prefix}.{key}" if prefix else key
            flat_dict.update(flatten_json(value, flat_key))
    elif isinstance(json_obj, list):
        for i, element in enumerate(json_obj):
            flat_key = f"{prefix}[{i}]"
            flat_dict.update(flatten_json(element, flat_key))
    else:
        flat_dict[prefix] = json_obj
    return flat_dict

def gron(json_content):
    json_obj = json.loads(json_content)
    return flatten_json(json_obj)

if __name__ == "__main__":
   
    # if len(sys.argv) > 1:
    #     filename = sys.argv[1]
        filename="/home/sadam/Documents/CS-515/CS515-Project-1/prog/data.json"
        try:
            with open(filename, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)
    # else:
    #     content = sys.stdin.read()

    
        flattened_json = gron(content)
        for key, value in flattened_json.items():
            print(f"json.{key} = {json.dumps(value)};")
