import json
import sys
from urllib.request import urlopen
from collections import defaultdict

def hep_url_generator(command_string,format,BAI):
    if format in ['json' , 'out' , None]:
        format = "recjson"
    if BAI == True:
        url = "http://inspirehep.net/search?ln=en&cc=HepNames&p=" + command_string + \
        "&of=" +format
    else:
        url = "https://inspirehep.net/search?p=" + command_string + \
            "&of=" +format+ "&ot=creator,creation_date,title"
    
    return url

def save_to_json(url , filename):
    
    with urlopen(url) as resp:
        source = resp.read()

    data = json.loads(source)

    with open(filename, 'w') as f:
        string = json.dumps(data, indent=2)
        f.write(string)
    print("Succesfully saved contents of the query to: " + filename)

def display_in_cmd(url):
    with urlopen(url) as resp:
        source = resp.read()
    data = json.loads(source)
    string = json.dumps(data, indent=2)
    print(string)