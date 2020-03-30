import json
import sys
from urllib.request import urlopen
from collections import defaultdict

class Hep_Helper:

    def hep_url_encode(self , string):
        encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
        for el1, el2 in encode_list:
            string = string.replace(el1, el2)
        return string


    def hep_url_generator(self, command_string, format):
        format = "recjson"

        url = "https://old.inspirehep.net/search?p=" + command_string + \
            "&of=" + format + "&ot=creator,title,creation_date,number_of_citations"

            #"&ot=creator,creation_date,title,doi,primary_report_number,number_of_citations,reference,recid"
        
        print(url)
        return url
    
    def get_source(self, url):
        with urlopen(url) as resp:
            source = resp.read()

            return source

    def write_to_json(self, source, filename):

        data = json.loads(source)

        with open(filename, 'w') as f:
            string = json.dumps(data, indent=2)
            f.write(string)
        print("Succesfully saved contents of the query to: " + filename)


    def display_in_cmd(self, url):
        with urlopen(url) as resp:
            source = resp.read()
        data = json.loads(source)
        string = json.dumps(data, indent=2)
        print(string)

class Hep_Parser:


    def __init__(self , source):
        self.data = json.loads(source)

    def get_creator_names(self):
        creator_list = list()
        for dic in self.data:
            creator_list.append(dic['creator']['full_name'])
        return creator_list

    def get_title(self):
        title_list = list()
        for dic in self.data:
            title_list.append(dic['title']['title'])
        return title_list

    def get_creation_date(self):
        date_list = list()
        for dic in self.data:
            date_list.append(dic['creation_date'])
        
        return date_list
  
    def get_citation_count(self):
        citation_count = list()
        for dic in self.data:
            citation_count.append(dic['number_of_citations'])
        return citation_count
