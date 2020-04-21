from urllib.request import urlopen
import requests
import os
from xml.etree import ElementTree as ET


class Arxiv_Helper:
    def __init__(self):
        self.CONST_QUERY_RESULTS = "3"

    def url_encode(self, string):
        encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
        for el1, el2 in encode_list:
            string = string.replace(el1, el2)
        return string

    def params_to_url(self, params):
        base_url = "http://export.arxiv.org/api/query?search_query="

        for i, (el1, el2) in enumerate(params):
            base_url += el1 + "%3A" + el2
            if i != len(params) - 1:
                base_url += "%20AND%20"

        base_url += "&max_results=" + self.CONST_QUERY_RESULTS
        print(base_url)
        return base_url

    def all_param(self, query):
        query = self.url_encode(query)
        print("http://export.arxiv.org/api/query?search_query=all:" + query)
        return "http://export.arxiv.org/api/query?search_query=all:" + query

    def api_to_file(self, url, file_name):
        r = requests.get(url)
        with open(file_name, 'w') as f_in:
            f_in.write(r.content.decode('utf-8'))


class Arxiv_Parser:

    def __init__(self, param_dict):
        self.parameters = param_dict
        print(param_dict)

    def parse_xml(self, file_name):
        data = ''
        with open(file_name, 'r') as file:
            root = ET.fromstring(file.read())

        full_name = os.path.abspath(os.path.join('', file_name))

        tree = ET.parse(full_name)
        root = tree.getroot()

        titles = root.findall('entry/title')
        ids = root.findall('entry/id')
        published = root.findall('entry/published')
        updated = root.findall('entry/updated')

        entries = root.findall('entry')

        for entry in entries:

            authors = entry.findall('author')
            number_of_authors = len(authors)

            if self.parameters['ALL'] is not None:
                data += "One of " + str(number_of_authors) + "authors\n"

            elif number_of_authors == 1:
                data += authors[0].text + " is the only author.\n"
            else:
                data += self.parameters['au'] + " is one of " + \
                    str(number_of_authors) + " authors\n"

            data += "Title: " + entry.find('title').text + '\n'
            data += "ID: " + entry.find('id').text + '\n'
            data += "Date Published: " + entry.find('published').text + '\n'
            data += "Last Update: " + entry.find('updated').text + '\n'

            if entry.find('journal_ref') is not None:
                data += "Journal: " + entry.find('journal_ref').text + '\n'

            if entry.find('doi') is not None:
                data += "DOI: " + entry.find('doi').text + '\n'

            data += '\n'

        return data

    def standarize_xml_file(self, file_name):
        with open(file_name, 'r') as file_r:
            data = file_r.readlines()
            with open(file_name, 'w') as file_w:
                for d in data:

                    d = d.replace(' xmlns="http://www.w3.org/2005/Atom"', '')
                    d = d.replace(
                        ' xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"', '')
                    d = d.replace('opensearch:', '')
                    d = d.replace('arxiv:', '')
                    d = d.replace(
                        ' xmlns:arxiv="http://arxiv.org/schemas/atom"', '')

                    file_w.write(d)
