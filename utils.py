# standard libraries
import json


def load_config(filename: str) -> dict:
    with open(file=filename, mode="r") as json_file:
        config = json.load(json_file)
    return config
