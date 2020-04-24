import json
import xml
import sys
from urllib.request import urlopen
from collections import defaultdict

class Hep_Helper:
    def __init__(self):
        # change for more outputs
        self.CONST_QUERY_RESULTS = "3"

    def hep_url_encode(self, string):
        encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
        for el1, el2 in encode_list:
            string = string.replace(el1, el2)
        return string

    def hep_url_generator(self, command_string, format):
        format = "recjson"

        url = "https://old.inspirehep.net/search?p=" + command_string + "&of=" + format + \
            "&ot=creator,title,creation_date,number_of_citations,authors,primary_report_number,doi,&rg=" + self.CONST_QUERY_RESULTS

        # "&ot=creator,creation_date,title,doi,primary_report_number,number_of_citations,reference,recid"

        return url

    def get_source(self, url):
        with urlopen(url) as resp:
            source = resp.read().decode('utf-8')

            self.write_to_json(source, "data/HEP_OUTPUT.json")

            return source

    def write_to_json(self, source, filename):

        data = json.loads(source)

        with open(filename, 'w') as f:
            string = json.dumps(data, indent=2)
            f.write(string)


class Hep_Parser:

    def __init__(self, source):

        self.list_of_dicts = list()
        self.data = json.loads(source)

        for dic in self.data:
            dict_single_result = dict()
            number_of_authors = len(dic['authors'])
            # Handle api error outputing DOI twice

            if dic['doi'] is None:
                dic['doi'] = 'DOI not specified'
            elif isinstance(dic['doi'], list):
                dic['doi'] = dic['doi'][0]

            dict_single_result = {
                'Creation_date': dic['creation_date'],
                'Creator_name': dic['creator']['full_name'],
                'Title': dic['title']['title'],
                'Arxiv_ID': dic['primary_report_number'],
                'DOI': dic['doi'],
                'Citations': dic['number_of_citations'],
                'Num_Of_Authors': number_of_authors}

            self.list_of_dicts.append(dict_single_result)

    def show(self):
        for dic in self.list_of_dicts:
            print("\n")
            for el in dic:
                print(el + ": " + str(dic[el]))

    def sort_by(self, value):
        if value == 'authors':
            self.list_of_dicts = sorted(
                self.list_of_dicts,
                key=lambda x: x['Num_Of_Authors'],
                reverse=True)
        elif value == 'date':
            self.list_of_dicts = sorted(
                self.list_of_dicts,
                key=lambda x: x['Creation_date'])
        elif value == 'citations':
            self.list_of_dicts = sorted(
                self.list_of_dicts,
                key=lambda x: x['Citations'],
                reverse=True)

    def write(self, filename):
        items = []
        with open(filename, 'w') as f:
            for dic in self.list_of_dicts:
                items = dic.items()
                for el in items:
                    f.write(str(el[0]) + ": " + str(el[1]) + '\n')
                f.write('\n')
