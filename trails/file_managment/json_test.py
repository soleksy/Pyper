import json

with open("trails/states.json") as f:
    data = json.load(f)

print(json.dumps(data ,indent = 2, sort_keys=True))

