import json
import sys
import cmd_module
from urllib.request import urlopen
from collections import defaultdict

List_Of_Commands = sys.argv[1:]

url = cmd_module.url_generator(List_Of_Commands)

print(url)

with urlopen(url) as resp:
    source = resp.read()

data = json.loads(source)

with open("sample_api.json", 'w') as f:
    string = json.dumps(data, indent=2)
    f.write(string)