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


class ArxivParser:

    def __init__(self, filename):
        self.ListOfArticles = list()
        self.filename = filename

    def getComment(self,entry):
        if entry.find('comment') is not None:
            comment = entry.find('comment').text
        else:
            comment = None
        return comment

    def getJournal(self, entry):
        if entry.find('journal_ref') is not None:
            journal = entry.find('journal_ref').text
        else:
            journal = None
        return journal

    def getDoi(self, entry):
        if entry.find('doi') is not None:
            doi = entry.find('doi').text
        else:
            doi = None
        return doi
    
    def getAuthors(self, entry):
        Authors = list()
        authorList = entry.findall('author')
        for el in authorList:
            Authors.append(el.find('name').text)
        return Authors

    def getEprint(self, entry):
        if entry.find('id').text is not None:
            ID = entry.find('id').text
            ID = ID[:-2]
            ID.replace("http://arxiv.org/abs/",'')    
        else:
            ID= None

        return ID

    def getTitle(self, entry):
        if entry.find('title').text is not None:
            title = entry.find('title').text     
        else:
            title= None
        return title

    def getDatePublished(self, entry):
        if entry.find('published').text is not None:
            published = entry.find('published').text     
        else:
            published= None
        return published 

    def getLastUpdate(self, entry):
        if entry.find('updated').text is not None:
            updated = entry.find('updated').text
        else:
            updated = None
        
        return updated

    def parseXML(self):
        singleArticle = dict()
        with open(self.filename, 'r') as file:
            root = ET.fromstring(file.read())

        full_name = os.path.abspath(os.path.join('', self.filename))

        tree = ET.parse(full_name)
        root = tree.getroot()

        entries = root.findall('entry')

        for entry in entries:
            singleArticle['Journal'] = self.getJournal(entry)
            singleArticle['Doi'] = self.getDoi(entry)
            singleArticle['Authors'] = self.getAuthors(entry)
            singleArticle['Eprint'] = self.getEprint(entry)
            singleArticle['NumberOfAuthors'] = len(self.getAuthors(entry))
            singleArticle['Title'] = self.getTitle(entry)
            singleArticle['DatePublished'] = self.getDatePublished(entry)
            singleArticle['LastUpdate']= self.getLastUpdate(entry)
            singleArticle['Comment'] = self.getComment(entry)
            
            self.ListOfArticles.append(singleArticle.copy())
            singleArticle.clear()


    def convertToBibtex(self):

        bibtexList = list()
        singleBibtex = list()
    
        for article in self.ListOfArticles:

            
            header = "@article{" + str(article['Authors'][0]) + ":" + str(article['DatePublished']).split("-", 1)[0] + ","
            author = "author = "

            if len(article['Authors']) == 1:
                author = str("author = " + article['Authors'][0]+  ",")
            else:
                authorListLenght = len(article['Authors'])
                for i in range(0, authorListLenght):
                    if i == 3:
                        author += "and " + str(len(str(article['Authors'])) - 3) +" others,"
                        break
                    else:
                        if(i == authorListLenght-1):
                            author += article['Authors'][i] + ","
                        else:
                            author += article['Authors'][i] + " and "

            singleBibtex.append(header)
            singleBibtex.append(author)

            if article.get("Title") is not None:
                title = article["Title"]
                singleBibtex.append("title = " + title  + ",")
            if article.get("Journal") is not None:
                journal = article["Journal"]
                singleBibtex.append("journal = " + journal +",")
            if article.get("DatePublished") is not None:
                year = str(article['DatePublished']).split("-", 1)[0]
                singleBibtex.append("year = " + year + ",")
            if article.get("Eprint") is not None:
                eprint = article["Eprint"]
                if 'http://arxiv.org/abs/physics/' in eprint:
                    singleBibtex.append("eprint = " + eprint.strip('http://arxiv.org/abs/physics/') + ",")
                else:
                    singleBibtex.append("eprint = " + eprint.strip('http://arxiv.org/abs/') + ",")

            if article.get("Comment") is not None:
                comment = article["Comment"]
                pagesOccurence = comment.find('pages')
                numberOfPages = comment[pagesOccurence-2:pagesOccurence]
                singleBibtex.append("pages = " + numberOfPages + ",")

            size = len(singleBibtex)
            singleBibtex[size-1] = singleBibtex[size-1].replace(",","}",1)
            bibtexList.append(singleBibtex.copy())
            singleBibtex.clear()

        return bibtexList


    def writeData(self, filename):
        with open(filename, 'w') as f:
            for article in self.ListOfArticles:
                f.write(str(article['Authors']) + ": \n " )
                f.write(str(article['DatePublished']) + ": \n ")
                f.write(str(article['LastUpdate']) + ": \n ")
                f.write(str(article['Title']) + ": \n ")
                f.write(str(article['Eprint']) + ": \n ")
                f.write(str(article['Doi']) + ": \n ")
                f.write(str(article['Journal']) + ": \n ")
                f.write(str(article['NumberOfAuthors']) + ": \n ")
                f.write("\n")
            f.write('\n')

    def writeBibtex(self, filename):
        citation_list = self.convertToBibtex()
        with open(filename, 'w') as f:
            for article in citation_list:
                for entry in article:
                    f.write(entry + "\n")
                f.write("\n")

    def show(self):
        for dic in self.ListOfArticles:
            print("\n")
            for el in dic:
                print(el + ": " + str(dic[el]))

    def standardizeXmlFile(self):
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

