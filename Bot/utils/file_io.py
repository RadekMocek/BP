import json


def json_read(path: str) -> dict:
    with open(path, "r") as file:
        return json.load(file)
