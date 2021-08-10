from flask import Flask , render_template ,redirect,url_for,request
from APIS.ARXIV.ArxivClasses import ArxivHelper , ArxivParser
app = Flask(__name__)


@app.route('/' , methods=['GET' ,'POST'])
def indexPage():


    if request.method == "POST":

        text = request.form["searchText"]
        if text == "":
            text = " "

        return redirect(url_for('searchResults',txt=text))
    else:
        return render_template('index.html')

@app.route('/search_results/<txt>')
def searchResults(txt):

    arxivHelper = ArxivHelper()
    queryURL = ""

    queryURL = arxivHelper.allParamSearch(txt)

    file_to_parse_arxiv = 'data/ARXIV_OUTPUT.xml'

    arxivHelper.apiToFile(queryURL, file_to_parse_arxiv)

    arxivParser = ArxivParser(file_to_parse_arxiv)

    arxivParser.standardizeXmlFile()
    arxivParser.parseXML()

    return render_template('search_results.html' , results=arxivParser.ListOfArticles)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
