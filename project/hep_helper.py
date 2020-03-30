import json
import sys
from urllib.request import urlopen
from collections import defaultdict


def url_encode(string):
    encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
    for el1, el2 in encode_list:
        string = string.replace(el1, el2)
    return string


def hep_url_generator(command_string, format):
    format = "recjson"

    url = "https://old.inspirehep.net/search?p=" + command_string + \
        "&of=" + format + "&ot=creator,creation_date,title,doi,primary_report_number,number_of_citations,reference,recid"
        
    print(url)
    return url


def save_to_json(url, filename):

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
