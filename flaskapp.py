from re import search
from flask import Flask , render_template ,redirect,url_for,request ,session
from APIS.ARXIV.ArxivClasses import ArxivHelper , ArxivParser
app = Flask(__name__)

articlesInstance = ArxivParser('')
searchController = 0

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def updateList(articles):
    global articlesInstance
    articlesInstance = articles

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
def searchResults(txt,hep,arxiv ):
    global searchController
    global articlesInstance
    session['searchURL'] = f"/search_results/{txt}/hep{hep}/arx{arxiv}"
    if request.method == "POST":
        articleID = request.form.get("info")
        return redirect(url_for('articlePage',id = articleID))

    elif searchController == 1:
        arxivHelper = ArxivHelper()
        queryURL = ""

        queryURL = arxivHelper.allParamSearch(txt)

        file_to_parse_arxiv = 'data/ARXIV_OUTPUT.xml'

        arxivHelper.apiToFile(queryURL, file_to_parse_arxiv)

        arxivParser = ArxivParser(file_to_parse_arxiv)

        arxivParser.standardizeXmlFile()
        arxivParser.parseXML()
        searchController = 0
        updateList(arxivParser)
        return render_template('search_results.html' , results=articlesInstance)
    else:
        return render_template('search_results.html' , results=articlesInstance)

@app.route('/search_results/<id>')
def articlePage(id):

    global articlesInstance
    bibtexList = articlesInstance.convertToBibtex()
    article = articlesInstance.ListOfArticles[int(id)]
    bibtex = bibtexList[int(id)]
    return render_template('article.html' , bibtex=bibtex, article=article ,searchURL = session['searchURL'])


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
