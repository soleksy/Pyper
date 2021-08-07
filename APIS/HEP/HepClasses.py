import json
from urllib.request import urlopen
from collections import defaultdict


class HepHelper:
    def __init__(self):
        self.CONST_QUERY_RESULTS = "5"

    def hepUrlEncode(self, string):
        encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
        for el1, el2 in encode_list:
            string = string.replace(el1, el2)
        return string

    def hepUrlGenerator(self, command_string):
        
        url = "https://inspirehep.net/api/literature?sort=mostarticled&page=1&q=" + command_string + "&of=recjson" + \
            "&fields=titles,citation_count,first_author,dois,publication_info,collaborations,arxiv_eprints,number_of_pages,volume,author_count&size=" + \
            self.CONST_QUERY_RESULTS

        print(url)
        return url

    def getSource(self, url):
        with urlopen(url) as resp:
            source = resp.read().decode('utf-8')

            self.writeToJson(source, "data/HEP_OUTPUT.json")

            return source

    def writeToJson(self, source, filename):

        data = json.loads(source)

        with open(filename, 'w') as f:
            string = json.dumps(data, indent=2)
            f.write(string)


class HepParser:

    def __init__(self, source):

        self.ListOfArticles = list()
        self.ListOfBibtex = list()

        self.data = json.loads(source)
        self.data = self.data["hits"]["hits"]

    def getAuthor(self,dic):
        if dic['metadata'].get('first_author') is not None:
            author = dic['metadata']['first_author'].get('full_name')
        else:
            author = "Coauthored "
        return author

    def getAuthorCount(self,dic):
        if dic['metadata'].get('author_count') is not None:
            authorCount = dic['metadata']['author_count']
        else:
            authorCount = 0;
        return authorCount

    def getJournal(self,dic):
        if dic['metadata'].get('publication_info') is None:
            journal = None
        elif isinstance(dic['metadata']['publication_info'], list):
            if dic['metadata']['publication_info'][0].get("journal_title") is None:
                journal = None
            else:
                journal = dic['metadata']['publication_info'][0]["journal_title"]

        elif dic['metadata']['publication_info'].get("journal_title") is None:
                journal = None
        else:
                journal = dic['metadata']['publication_info']["journal_title"]

        return journal
        
    def getTitle(self,dic):
        if dic['metadata'].get('titles') is not None:
            title = dic['metadata']['titles'][0]['title']
        else:
            title = "No title"
        return title

    #getDoi
    def getDoi(self,dic):
        if dic['metadata'].get('dois') is not None:
                Doi = dic['metadata']['dois'][0]['value']
        else:
            Doi = "No DOI"
        return Doi
    #getYear
    def getYear(self,dic):
        if dic['metadata'].get('publication_info') is not None:
            if(type(dic["metadata"]['publication_info'])) == list:
                    year = dic["metadata"]['publication_info'][0]["year"]
            else:
                year = dic["metadata"]['publication_info']["year"]
        else:
            year = "No year"
        return year
        
    
    def getCollaboration(self,dic):
        if dic['metadata'].get('collaborations') is None:
            collaboration = "not specified"
        elif isinstance(dic['metadata']['collaborations'], list):
            collaboration = ""
            for el in dic['metadata']['collaborations']:
                collaboration += el['value'] + " "
        else:
            collaboration = dic['metadata']['collaborations']['value']

        return collaboration

        
    def getPages(self,dic):
        if dic['metadata'].get('number_of_pages') is None:
            pages = "not specified"
        else:
            pages = dic['metadata']['number_of_pages']
        return pages

    def getVolume(self,dic):
        if dic['metadata'].get('publication_info') is None:
            volume = "not specified"
        else:
            volume = dic['metadata']['publication_info'][0]["journal_volume"]
        return volume

    def getEprint(self,dic):
        if dic['metadata'].get('arxiv_eprints') is None:
            eprint = "not specified"
        else:
            eprint = dic['metadata']['arxiv_eprints'][0]["value"]
        return eprint

    
    def parseJsonFile(self):
        for dic in self.data:
            
            author = self.getAuthor( dic)
            authorCount = self.getAuthorCount(dic)
            journal = self.getJournal(dic)
            title = self.getTitle(dic)
            year = self.getYear(dic)
            doi = self.getDoi(dic)
            collaboration = self.getCollaboration(dic)
            pages = self.getPages(dic)
            volume = self.getVolume(dic)
            eprint = self.getEprint(dic)
            

            singleArticle = {
                'Author': author,
                'Date_Published': dic['created'],
                'Title': title,
                'DOI': doi,
                'Citations': dic['metadata']['citation_count'],
                'Journal': journal,
                'Year': year,}
            
            bibtexSigleResult = {
                'Author': dic['metadata']['first_author']['full_name'],
                'Title': title,
                'Eprint': eprint,
                'DOI': doi,
                'Collaboration' : collaboration,
                'Journal': journal,
                'Volume': volume,
                'Pages': pages,
                'Year': year,
                'AuthorCount': authorCount
            }

            self.ListOfArticles.append(singleArticle)
            self.ListOfBibtex.append(bibtexSigleResult)

    def convertToBibtex(self):

        bibtexList = list()

        for el in self.ListOfBibtex:

            bibtexList.append(["@article{" + str(el['Author']) + ":" + str(el['Year']) + ",",
                                "author =  " + str(el['Author']) + " and " +str(el['AuthorCount']) + " other authors",
                                "title =  " + str(el['Title']) + ",",
                                "journal =  " + str(el['Journal']) + ",",
                                "year =  " + str(el['Year']) + ",",
                                "volume =  " + str(el['Volume']) + ",",
                                "pages =  " + str(el['Pages']) + ",",
                                "collaboration =  " + str(el['Collaboration']) + ",",
                                "doi =  " + str(el['DOI']) + ",",
                                "eprint =  " + str(el['Eprint']) + ",",
                                "}"]
            )

        return bibtexList
    

    def show(self):
        for dic in self.ListOfArticles:
            print("\n")
            for el in dic:
                print(el + ": " + str(dic[el]))

    def sortBy(self, value):
        if value == 'authors':
            self.ListOfArticles = sorted(
                self.ListOfArticles,
                key=lambda x: x['Num_Of_Authors'],
                reverse=True)
        elif value == 'date':
            self.ListOfArticles = sorted(
                self.ListOfArticles,
                key=lambda x: x['Creation_date'])
        elif value == 'citations':
            self.ListOfArticles = sorted(
                self.ListOfArticles,
                key=lambda x: x['Citations'],
                reverse=True)
                
    def writeBibtex(self, filename):
        bibtexList = self.convertToBibtex()

        with open(filename, 'w') as f:
            for article in bibtexList:
                for el in article:
                    f.write(el+"\n")
                f.write('\n')


    def writeData(self, filename):
        items = []
        with open(filename, 'w') as f:
            for dic in self.ListOfArticles:
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
                
