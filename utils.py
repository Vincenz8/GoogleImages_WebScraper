# standard libraries
import json
from typing import Any


def load_json(filename: str) -> dict:
    with open(file=filename, mode="r") as json_file:
        json_dict = json.load(json_file)
    return json_dict

def to_json(obj: Any, filename: str) -> None:
    with open(file=filename, mode='w') as json_file:
        json.dump(obj, json_file)