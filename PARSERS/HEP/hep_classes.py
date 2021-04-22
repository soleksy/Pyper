import json
import xml
import sys
from urllib.request import urlopen
from collections import defaultdict


class Hep_Helper:
    def __init__(self):
        # change for more outputs
        self.CONST_QUERY_RESULTS = "10"

    def hep_url_encode(self, string):
        encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
        for el1, el2 in encode_list:
            string = string.replace(el1, el2)
        return string

    def hep_url_generator(self, command_string):
        
        url = "https://inspirehep.net/api/literature?q=" + command_string + "&of=recjson" + \
            "&ot=creator,title,creation_date,number_of_citations,authors,primary_report_number,doi,publication_info,&size=" + \
            self.CONST_QUERY_RESULTS

        print(url)
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
        self.data = self.data["hits"]["hits"]
        
        for dic in self.data:
            ID = ''

            list_of_authors = list()
            list_of_titles = list()
            list_of_dois = list()

            dict_single_result = dict()
            journal = ""
            number_of_authors = len(dic['metadata']['authors'])
            # Handle api error outputing DOI twice
            if dic['metadata'].get('dois') is None:
                dic['metadata']['dois'] =  None
            elif isinstance(dic['metadata']['dois'], list):
                dic['metadata']['dois'] = dic['metadata']['dois'][0]

            if dic['metadata'].get('publication_info') is None:
                journal = None

            elif isinstance(dic['metadata']['publication_info'], list):
                for i  in range(0,len(dic['metadata']['publication_info'])):
                    journal = dic['metadata']['publication_info'][i].get('reference',None)
                    if journal != None:
                        break
            else:
                journal = dic['publication_info'].get('retitlesference',None)
                
            for el in dic['metadata']['authors']:
                list_of_authors.append(el['full_name'])

            for el in dic['metadata']['titles']:
                list_of_titles.append(el['title'])
            
            if dic['metadata']['dois'] is not None:
                for el in dic['metadata']['dois']:
                    list_of_dois.append(dic['metadata']['dois']["value"])

            dict_single_result = {
                
                'Authors': list_of_authors,
                'Date_Published': dic['created'],
                'Title': list_of_titles,
                'ID': ID,
                'DOI': list_of_dois,
                'Citations': dic['metadata']['citation_count'],
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
                    if type(el[1]) == list:
                        f.write(str(el[0] + ":\n"))
                        for x in el[1]:
                            f.write(str(x)+" ,")
                        f.write('\n\n')
                    else:
                        f.write(str(el[0]) + ": \n" + str(el[1]))
                        f.write('\n\n')
                f.write('\n\n')
