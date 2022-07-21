# standard libraries
import json
from typing import Any


def load_config(filename: str) -> dict:
    with open(file=filename, mode="r") as json_file:
        config = json.load(json_file)
    return config

def to_json(obj: Any, filename: str) -> None:
    with open(file=filename, mode='w') as json_file:
        json.dump(obj, json_file)