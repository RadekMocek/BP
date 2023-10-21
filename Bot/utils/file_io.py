import json


def json_read(path):
    with open(path, "r") as file:
        return json.load(file)
