import json

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return super().default(obj)

class SessionSerializer:
    def serialize(self, data):
        return json.dumps(data, cls=CustomJSONEncoder)

    def deserialize(self, raw_str):
        return json.loads(raw_str)
