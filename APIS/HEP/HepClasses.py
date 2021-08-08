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
            author = None
        return author

    def getAuthorCount(self,dic):
        if dic['metadata'].get('author_count') is not None:
            authorCount = dic['metadata']['author_count']
        else:
            authorCount = None;
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
            title = None
        return title

    def getDoi(self,dic):
        if dic['metadata'].get('dois') is not None:
                Doi = dic['metadata']['dois'][0]['value']
        else:
            Doi = None
        return Doi
    def getYear(self,dic):
        if dic['metadata'].get('publication_info') is not None:
            if(type(dic["metadata"]['publication_info'])) == list:
                    year = dic["metadata"]['publication_info'][0]["year"]
            else:
                year = dic["metadata"]['publication_info']["year"]
        else:
            year = None
        return year
        
    
    def getCollaboration(self,dic):
        if dic['metadata'].get('collaborations') is None:
            collaboration = None
        elif isinstance(dic['metadata']['collaborations'], list):
            collaboration = ""
            for el in dic['metadata']['collaborations']:
                collaboration += el['value'] + " "
        else:
            collaboration = dic['metadata']['collaborations']['value']

        return collaboration


    def getPages(self,dic):
        if dic['metadata'].get('number_of_pages') is None:
            pages = None
        else:
            pages = dic['metadata']['number_of_pages']
        return pages

    def getVolume(self,dic):
        if dic['metadata'].get('publication_info') is None:
            volume = None
        else:
            volume = dic['metadata']['publication_info'][0]["journal_volume"]
        return volume

    def getEprint(self,dic):
        if dic['metadata'].get('arxiv_eprints') is None:
            eprint = None
        else:
            eprint = dic['metadata']['arxiv_eprints'][0]["value"]
        return eprint

    
    def parseJsonFile(self):
        singleArticle = dict()
         
        for dic in self.data:
        
            author = self.getAuthor(dic)
            authorCount = self.getAuthorCount(dic)
            journal = self.getJournal(dic)
            title = self.getTitle(dic)
            year = self.getYear(dic)
            doi = self.getDoi(dic)
            collaboration = self.getCollaboration(dic)
            pages = self.getPages(dic)
            volume = self.getVolume(dic)
            eprint = self.getEprint(dic)
            

            if author is not None:
                singleArticle['Author'] = author
            if authorCount is not None:
                singleArticle['AuthorCount'] = authorCount
            if journal is not None:
                singleArticle['Journal'] = journal
            if title is not None:
                singleArticle['Title'] = title
            if year is not None:
                singleArticle['Year'] = year
            if doi is not None:
                singleArticle['Doi'] = doi
            if collaboration is not None:
                singleArticle['Collaboration'] = collaboration
            if pages is not None:
                singleArticle['Pages'] = pages
            if volume is not None:
                singleArticle['Volume'] = volume
            if eprint is not None:
                singleArticle['Eprint'] = eprint
  
            self.ListOfArticles.append(singleArticle.copy())

            singleArticle.clear()

    def convertToBibtex(self):


        bibtexList = list()
        singleBibtex = list()

        for bibtex in self.ListOfArticles:
            if bibtex.get('Author') is None:
                if bibtex.get("AuthorCount") is not None:
                    if bibtex.get("Year") is not None:  
                        header =  "@article{" + "Coauthored by " +  str(bibtex.get("AuthorCount")) + " authors" + ":" + str(bibtex['Year']) + ","
                    else:
                        header = "@article{" + "Coauthored by " +  str(bibtex.get("AuthorCount")) + " authors"
                else:
                        if bibtex.get("Year") is not None:  
                            header = "@article{"+ "Anonymous" + ":" + str(bibtex['Year']) + ","
                        else:
                            header = "@article{"+ "Anonymous"
            else:
                if bibtex.get("Year") is not None: 
                    header = "@article{"+ bibtex.get("Author") + ":" + str(bibtex['Year']) + ","
                else:
                    header = "@article{"+ bibtex.get("Author")

            singleBibtex.append(header)

            if bibtex.get('Author') is not  None:
                if bibtex.get("AuthorCount") is not None:
                    author = "author =  " + str(bibtex['Author']) + " and " +str(bibtex['AuthorCount']) + " others"
            else:
                if bibtex.get("AuthorCount") is not None:
                    author = "Coauthored by " +  str(bibtex.get("AuthorCount")) + " authors"
                else:
                    author = "Anonymous"

            singleBibtex.append(author)
    
            if bibtex.get('Title') is not None:
                title = "title =  " + str(bibtex['Title']) + ","
                singleBibtex.append(title)
            
            if bibtex.get('Year') is not None:
                year = "year =  " + str(bibtex['Year']) + ","
                singleBibtex.append(year)

            if bibtex.get('Journal') is not None:
                journal = "journal =  " + str(bibtex['Journal']) + ","
                singleBibtex.append(journal)
        
            
            if bibtex.get('Volume') is not None:
                volume = "volume =  " + str(bibtex['Volume']) + ","
                singleBibtex.append(volume)
            
            if bibtex.get('Pages') is not None:
                pages = "pages =  " + str(bibtex['Pages']) + ","
                singleBibtex.append(pages)
            
            if bibtex.get('Collaboration') is not None:
                collaboration = "collaboration =  " + str(bibtex['Collaboration']) + ","
                singleBibtex.append(collaboration)
            
            if bibtex.get('Doi') is not None:
                doi = "doi =  " + str(bibtex['Doi']) + ","
                singleBibtex.append(doi)
            
            if bibtex.get('Eprint') is not None:
                eprint = "eprint =  " + str(bibtex['Eprint']) + ","
                singleBibtex.append(eprint)

            size = len(singleBibtex)
            singleBibtex[size-1] = singleBibtex[size-1].replace(","," }")
            bibtexList.append(singleBibtex.copy())
            singleBibtex.clear()


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
                
