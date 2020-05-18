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
        return base_url

    def all_param(self, query):
        query = self.url_encode(query)
        return "http://export.arxiv.org/api/query?search_query=all:" + query

    def api_to_file(self, url, file_name):
        r = requests.get(url)
        with open(file_name, 'w') as f_in:
            f_in.write(r.content.decode('utf-8'))


class Arxiv_Parser:

    def __init__(self, filename):
        self.list_of_dicts = list()
        self.filename = filename

    def parse_xml(self):
        single_result_dict = {}
        journal = ""
        doi = ""

        with open(self.filename, 'r') as file:
            root = ET.fromstring(file.read())

        full_name = os.path.abspath(os.path.join('', self.filename))

        tree = ET.parse(full_name)
        root = tree.getroot()

        entries = root.findall('entry')

        for entry in entries:
            if entry.find('journal_ref') is not None:
                journal = entry.find('journal_ref').text
            else:
                journal = "NONE"
            if entry.find('doi') is not None:
                doi = entry.find('doi').text
            else:
                doi = "NONE"
            list_of_authors = list()

            authors = entry.findall('author')
            for el in authors:
                list_of_authors.append(el.find('name').text)
            number_of_authors = len(authors)

            single_result_dict = {
                "Authors": list_of_authors,
                "Date_Published": entry.find('published').text,
                "Last_Update": entry.find('updated').text,
                "Title": entry.find('title').text,
                "ID": entry.find('id').text.replace("http://arxiv.org/abs/",''),
                "DOI": doi,
                "Journal": journal,
                "Num_Of_Authors": number_of_authors}

            self.list_of_dicts.append(single_result_dict)

    def show(self):
        for dic in self.list_of_dicts:
            print("\n")
            for el in dic:
                print(el + ": " + str(dic[el]))

    def standarize_xml_file(self):
        with open(self.filename, 'r') as file_r:
            data = file_r.readlines()
            with open(self.filename, 'w') as file_w:
                for d in data:

                    d = d.replace(' xmlns="http://www.w3.org/2005/Atom"', '')
                    d = d.replace(
                        ' xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"', '')
                    d = d.replace('opensearch:', '')
                    d = d.replace('arxiv:', '')
                    d = d.replace(
                        ' xmlns:arxiv="http://arxiv.org/schemas/atom"', '')

                    file_w.write(d)

    def filter_range(self, range):
        temp_list = list()
        year = 0
        status = ''
        try:
            if range[0] == '-':
                status = 'till'
                year = int(range[1:])
            elif range[0] == '+':
                status = 'after'
                year = int(range[1:])
            else:
                status = 'between'
                year1 = int(range[0:4])
                year2 = int(range[5:9])

            for dic in self.list_of_dicts:
                full_date = dic['Date_Published']
                date = int(full_date[:4])
                if status == 'till':
                    if date <= year:
                        temp_list.append(dic)
                elif status == 'after':
                    if date >= year:
                        temp_list.append(dic)
                else:
                    if date >= year1 and date <= year2:
                        temp_list.append(dic)
            self.list_of_dicts = temp_list
        except BaseException:
            print("Error while parsing range expression try ./pyper.py ARXIV -h for more information on available range formats")
            return -1

    def sort_by(self, value):
        if value == 'authors':
            self.list_of_dicts = sorted(
                self.list_of_dicts,
                key=lambda x: x['Num_Of_Authors'],
                reverse=True)
        elif value == 'published':
            self.list_of_dicts = sorted(
                self.list_of_dicts,
                key=lambda x: x['Date_Published'])
        elif value == 'updated':
            self.list_of_dicts = sorted(
                self.list_of_dicts,
                key=lambda x: x['Last_Update'],
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
                            f.write(str(x))
                        f.write('\n\n')
                    else:
                        f.write(str(el[0]) + ": \n" + str(el[1]) + '\n\n')
                f.write('\n')
