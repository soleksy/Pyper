from re import search
from flask import Flask , render_template ,redirect,url_for,request ,session
from APIS.ARXIV.ArxivClasses import ArxivHelper , ArxivParser
from APIS.HEP.HepClasses import HepHelper,HepParser
import asyncio , aiohttp , httpx
import time
app = Flask(__name__)

articleList = []
searchController = 0

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def updateList(articles):
    global articleList
    articleList = articles



@app.route('/' , methods=['GET' ,'POST'])
def indexPage():
    global searchController
    if request.method == "POST":
        searchController = 1
        text = request.form["searchText"]
        if text == "":
            text = " "
        ARXIV = request.form.get('arxiv')
        if ARXIV == None:
            ARXIV = 'off'

        HEP = request.form.get('hep')
        if HEP == None:
            HEP = 'off'
        
        return redirect(url_for('searchResults',txt=text,hep=HEP,arxiv=ARXIV))
    else:
        return render_template('index.html')

@app.route('/search_results/<txt>/hep<hep>/arx<arxiv>' , methods=['GET' ,'POST'])
async def searchResults(txt,hep,arxiv ):

    global searchController
    global articleList

    arxivArticleList = []
    hepArticleList = []

    dbToSearch = []
    listOfApiCalls = []

    index = 0

    session['searchURL'] = f"/search_results/{txt}/hep{hep}/arx{arxiv}"

    if request.method == "POST":
        articleID = request.form.get("info")
        return redirect(url_for('articlePage',id = articleID))

    elif searchController == 1:
        
        if (arxiv == 'on'):
            arxivHelper = ArxivHelper()
            queryURL = arxivHelper.allParamSearch(txt)
            listOfApiCalls.append(httpx.AsyncClient().get(queryURL))

        if (hep == 'on'):
            hepHelper = HepHelper()
            url = hepHelper.hepUrlGenerator(txt)
            listOfApiCalls.append(httpx.AsyncClient().get(url))

        async with httpx.AsyncClient():
            dbToSearch = await asyncio.gather(
                *listOfApiCalls
            )
        
        if (arxiv=='on'):
            arxivParser = ArxivParser(dbToSearch[index].content)
            arxivParser.standardizeXml()
            arxivParser.parseXML()
            arxivArticleList = arxivParser.ListOfArticles
            index += 1
        if (hep == 'on'):
            hepParser = HepParser(dbToSearch[index].content)
            hepParser.parseJsonFile()
            hepArticleList = hepParser.ListOfArticles
            index += 1

        searchController = 0
        updateList(hepArticleList + arxivArticleList)

        return render_template('search_results.html' , results=arxivArticleList+hepArticleList)

    else:
        return render_template('search_results.html' , results=articleList)

@app.route('/search_results/<id>')
def articlePage(id):

    global articleList
    article = articleList[int(id)]
    bibtex = articleList[int(id)]['Bibtex']

    return render_template('article.html' , bibtex=bibtex, article=article ,searchURL = session['searchURL'])


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
