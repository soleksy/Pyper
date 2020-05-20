import json
import xml
import sys
from urllib.request import urlopen
from collections import defaultdict


class Hep_Helper:
    def __init__(self):
        # change for more outputs
        self.CONST_QUERY_RESULTS = "500"

    def hep_url_encode(self, string):
        encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
        for el1, el2 in encode_list:
            string = string.replace(el1, el2)
        return string

    def hep_url_generator(self, command_string, format):
        format = "recjson"

        url = "https://old.inspirehep.net/search?p=" + command_string + "&of=" + format + \
            "&ot=creator,title,creation_date,number_of_citations,authors,primary_report_number,doi,publication_info,&rg=" + \
            self.CONST_QUERY_RESULTS

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

            list_of_authors = list()
            ID = ''
            dict_single_result = dict()
            journal = ""
            number_of_authors = len(dic['authors'])
            # Handle api error outputing DOI twice

            if dic['doi'] is None:
                dic['doi'] =  None
            elif isinstance(dic['doi'], list):
                dic['doi'] = dic['doi'][0]

            if dic['publication_info'] is None:
                journal = None
            else:
                journal = dic['publication_info'].get('reference',None)
                
            for a in dic['authors']:
                list_of_authors.append(a['full_name'])
            
            if dic['primary_report_number'] is None:
                ID = None
            else:
                ID = dic['primary_report_number'].replace('arXiv:','')

            dict_single_result = {
                
                'Authors': list_of_authors,
                'Date_Published': dic['creation_date'],
                'Title': dic['title']['title'],
                'ID': ID,
                'DOI': dic['doi'],
                'Citations': dic['number_of_citations'],
                'Journal': journal,
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
                    if el[0] == 'Authors':
                        f.write(str(el[0] + ": \n "))
                        for x in el[1]:
                            f.write(str(x)+" ,")
                        f.write('\n\n')
                    else:
                        f.write(str(el[0]) + ": \n" + str(el[1]) + '\n\n')
                f.write('\n')
