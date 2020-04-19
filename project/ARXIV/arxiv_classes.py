from urllib.request import urlopen
import xml


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
        return base_url

    def all_param(self, query):
        query = self.url_encode(query)
        return "http://export.arxiv.org/api/query?search_query=all:" + query

    def api_to_file(self, url):
        data = urlopen(url).read()

        with open("sample.xml", 'w') as f_out:
            f_out.write(str(data))

    def get_query_result(self, url):
        data = urlopen(url).read()
        return data
