import json

def to_json(obj, pretty=True):
    if pretty:
        return json.dumps(obj, indent=4, ensure_ascii=False, default=str)
    return json.dumps(obj, ensure_ascii=False, default=str)

def from_json(json_str):
    return json.loads(json_str)
