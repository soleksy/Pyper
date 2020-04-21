import json
import xml
import sys
from urllib.request import urlopen
from collections import defaultdict


class Hep_Helper:

    def hep_url_encode(self, string):
        encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
        for el1, el2 in encode_list:
            string = string.replace(el1, el2)
        return string

    def hep_url_generator(self, command_string, format):
        format = "recjson"

        url = "https://old.inspirehep.net/search?p=" + command_string + "&of=" + format + \
            "&ot=creator,title,creation_date,number_of_citations,primary_report_number,doi&rg=250"

        # "&ot=creator,creation_date,title,doi,primary_report_number,number_of_citations,reference,recid"

        print(url)
        return url

    def get_source(self, url):
        with urlopen(url) as resp:
            source = resp.read().decode('utf-8')

            self.write_to_json(source, "data/API_OUTPUT_JSON.json")

            return source

    def write_to_json(self, source, filename):

        data = json.loads(source)

        with open(filename, 'w') as f:
            string = json.dumps(data, indent=2)
            f.write(string)


class Hep_Parser:

    def __init__(self, source):

        self.List_Of_Results = list()
        self.data = json.loads(source)

        for dic in self.data:
            # Handle api error outputing DOI twice
            if dic['doi'] is None:
                dic['doi'] = 'DOI not specified'
            elif isinstance(dic['doi'], list):
                dic['doi'] = dic['doi'][0]

            self.List_Of_Results.append([
                dic['creation_date'],  # 0 DATE
                dic['creator']['full_name'],  # 1 NAME
                dic['title']['title'],  # 2 TITLE
                dic['primary_report_number'],  # 3 ARXIV_ID
                dic['doi'],  # 4 DIGITAL_OBJECT_ID
                dic['number_of_citations']])  # 5 CITATIONS

    def show(self):
        for List in self.List_Of_Results:
            print("\n")
            for el in List:
                print(el)

    def write(self, filename):
        with open(filename, 'w') as f:
            for List in self.List_Of_Results:
                f.write("\n")
                for el in List:
                    f.write(str(el) + "\n")

    def sort_by(self, value):
        if value == 'name':
            self.List_Of_Results.sort(key=lambda x: x[1])
        elif value == 'date':
            self.List_Of_Results.sort(key=lambda x: x[0])
        elif value == 'citations':
            self.List_Of_Results.sort(key=lambda x: x[5], reverse=True)
