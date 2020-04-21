from urllib.request import urlopen
import requests
import os
from xml.etree import ElementTree as ET



class Arxiv_Helper:

    def url_encode(self, string):
        encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
        for el1, el2 in encode_list:
            string = string.replace(el1, el2)
        return string

    def parse_param_list(self, params):
        base_url = "http://export.arxiv.org/api/query?search_query="

        for i, (el1, el2) in enumerate(params):
            base_url += el1 + "%3A" + el2
            if i != len(params) - 1:
                base_url += "%20AND%20"
            base_url += "&max_results=10" # change for more outputs
            print(base_url)
            
        return base_url

    def all_param(self, query):
        query = self.url_encode(query)
        return "http://export.arxiv.org/api/query?search_query=all:" + query

    def api_to_file(self , url , file_name):
        r = requests.get(url)
        with open(file_name , 'w') as f_in:
            f_in.write(r.content.decode('utf-8'))
        
        return file_name

    
        

class Arxiv_Parser:

    def parse_xml(self, file_name):
        with open(file_name,'r') as file:
            root = ET.fromstring(file.read())

        full_name = os.path.abspath(os.path.join('',file_name))

        tree = ET.parse(full_name)
        root = tree.getroot()

        #parsing code here

        return file_name


    def standarize_xml_file(self , file_name):
        with open(file_name,'r') as file_r:
            data = file_r.readlines()
            with open(file_name,'w') as file_w:
                for d in data:

                    d = d.replace(' xmlns="http://www.w3.org/2005/Atom"' , '')
                    d = d.replace(' xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"','')
                    d = d.replace('opensearch:' , '')
                    d = d.replace('arxiv:' , '')
                    d = d.replace(' xmlns:arxiv="http://arxiv.org/schemas/atom"' , '')

                    file_w.write(d)


        return file_name


