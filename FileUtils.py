import json


def json_to_dict(json_file_path):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    return json_data
