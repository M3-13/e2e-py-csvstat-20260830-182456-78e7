"""JSON output for csvstat."""

import json


def render_json(result: list[dict]) -> str:
    obj: dict = {}
    for column in result:
        name = column["name"]
        value: dict = {"type": column["type"]}
        for key, val in column.items():
            if key in ("name", "type"):
                continue
            value[key] = val
        obj[name] = value
    return json.dumps(obj)
