from urllib.request import urlopen
import requests
import os
from xml.etree import ElementTree as ET



class ArxivHelper:
    def __init__(self):
        self.CONST_QUERY_RESULTS = "20"

    def url_encode(self, string):
        encode_list = [(" ", "%20"), (":", "%3A"), ("/", "%2" + "F")]
        for el1, el2 in encode_list:
            string = string.replace(el1, el2)
        return string

    def paramsToUrl(self, params):
        base_url = "http://export.arxiv.org/api/query?search_query="

        for i, (el1, el2) in enumerate(params):
            base_url += el1 + "%3A" + el2
            if i != len(params) - 1:
                base_url += "%20AND%20"

        base_url += "&max_results=" + self.CONST_QUERY_RESULTS
        base_url += "&sortBy=relevance&sortOrder=ascending"
        return base_url

    def allParamSearch(self, query):
        query = self.url_encode(query)
        return "http://export.arxiv.org/api/query?search_query=all:" + query + "&max_results=" + self.CONST_QUERY_RESULTS + "&sortBy=relevance"

    def apiToFile(self, url, file_name):
        r = requests.get(url)
        with open(file_name, 'w') as f_in:
            f_in.write(r.content.decode('utf-8'))




class ArxivArticle:
        def __init__(self, Authors,DatePublished,LastUpdate,Title,ID,DOI,Journal,NumOfAuthors,bibtex):
            self.Authors = Authors
            self.DatePublished = DatePublished
            self.LastUpdate = LastUpdate
            self.Title = Title
            self.ID = ID
            self.DOI = DOI
            self.Journal = Journal
            self.NumOfAuthors = NumOfAuthors
            self.bibtex = bibtex


class ArxivParser:

    def __init__(self, filename):
        self.ListOfArticles = list()
        self.ListOfBibtex = list()
        self.filename = filename

    def getJournal(self, entry):
        if entry.find('journal_ref') is not None:
            journal = entry.find('journal_ref').text
        else:
            journal = "Journal not specified"
        return journal

    def getDoi(self, entry):
        if entry.find('doi') is not None:
            doi = entry.find('doi').text
        else:
            doi = "DOI not specified"
        return doi
    
    def getAuthors(self, entry):
        Authors = list()
        authorList = entry.findall('author')
        for el in authorList:
            Authors.append(el.find('name').text)
        return Authors

    def getID(self, entry):
        if entry.find('id').text is not None:
            ID = entry.find('id').text
            ID = ID[:-2]
            ID.replace("http://arxiv.org/abs/",'')    
        else:
            ID= "ID not specified"

        return ID

    def getTitle(self, entry):
        if entry.find('title').text is not None:
            title = entry.find('title').text     
        else:
            title= "Title not specified"
        return title

    def getDatePublished(self, entry):
        if entry.find('published').text is not None:
            published = entry.find('published').text     
        else:
            published= "Publishing date not specified"
        return published 

    def getLastUpdate(self, entry):
        if entry.find('updated').text is not None:
            updated = entry.find('updated').text
        else:
            updated = "Update date not specified"
        
        return updated

    def parseXML(self):
        with open(self.filename, 'r') as file:
            root = ET.fromstring(file.read())

        full_name = os.path.abspath(os.path.join('', self.filename))

        tree = ET.parse(full_name)
        root = tree.getroot()

        entries = root.findall('entry')

        for entry in entries:
            Journal = self.getJournal(entry)
            Doi = self.getDoi(entry)
            Authors = self.getAuthors(entry)
            ID = self.getID(entry)
            NumberOfAuthors = len(Authors)
            Title = self.getTitle(entry)
            DatePublished = self.getDatePublished(entry)
            LastUpdate= self.getLastUpdate(entry)
            
            SingleBibtexArticle = {
                "Authors": Authors,
                "Title": Title,
                "Journal": Journal,
                "Date_Published": entry.find('published').text
                }

            article = ArxivArticle(Authors,DatePublished, 
            LastUpdate,Title,ID,Doi,Journal,NumberOfAuthors,SingleBibtexArticle)
            self.ListOfArticles.append(article)
            self.ListOfBibtex.append(SingleBibtexArticle)

    def show(self):
        for dic in self.ListOfArticles:
            print("\n")
            for el in dic:
                print(el + ": " + str(dic[el]))

    def standarizeXmlFile(self):
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

    def filterRange(self, range):
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

            for dic in self.ListOfArticles:
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
            self.ListOfArticles = temp_list
        except BaseException:
            print("Error while parsing range expression try ./pyper.py ARXIV -h for more information on available range formats")
            return -1

    def sortBy(self, value):
        if value == 'authors':
            self.ListOfArticles = sorted(
                self.ListOfArticles,
                key=lambda x: x['Num_Of_Authors'],
                reverse=True)
        elif value == 'published':
            self.ListOfArticles = sorted(
                self.ListOfArticles,
                key=lambda x: x['Date_Published'])
        elif value == 'updated':
            self.ListOfArticles = sorted(
                self.ListOfArticles,
                key=lambda x: x['Last_Update'],
                reverse=True)

    def convertToBibtex(self):

        citation_list = list()
        
        


        for article in self.ListOfBibtex:
            if len(article['Authors'][0]) == 1:
                authors = str(article['Authors'][0])
            else:
                authors = str(article['Authors'][0]) + ' and ' + str(len(article['Authors'][0])-1) + ' others'

            citation_list.append(["@article{" + str(article['Authors'][0]) + ":" + str(article['Date_Published']).split("-", 1)[0] + ",",
                                "author =  " + authors,
                                "title =  " + article['Title'] + " },",
                                "journal = " + article['Journal'] + " },",
                                "year =  " + str(article['Date_Published']).split("-", 1)[0] + " ,",
                                "}"]
            )


        return citation_list


    def writeData(self, filename):
        with open(filename, 'w') as f:
            for article in self.ListOfArticles:
                f.write(str(article.Authors[0]) + ": \n " )
                f.write(str(str(article.DatePublished) + ": \n "))
                f.write(str(str(article.LastUpdate) + ": \n "))
                f.write(str(article.Title) + ": \n ")
                f.write(str(str(article.ID) + ": \n "))
                f.write(str(str(article.DOI) + ": \n "))
                f.write(str(str(article.Journal) + ": \n "))
                f.write(str(str(article.NumOfAuthors) + ": \n "))
                f.write(str(str(article.bibtex) + ": \n "))
                f.write("\n")
            f.write('\n')

    def writeBibtex(self, filename):
        citation_list = self.convertToBibtex()
        with open(filename, 'w') as f:
            for article in citation_list:
                for entry in article:
                    f.write(entry + "\n")
                f.write("\n")
