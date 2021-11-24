from re import S, search
from flask import Flask , render_template ,redirect,url_for,request ,session
from APIS.ARXIV.ArxivClasses import ArxivHelper , ArxivParser
from APIS.HEP.HepClasses import HepHelper,HepParser
import asyncio , aiohttp , httpx

from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField

import time
app = Flask(__name__)

articleList = []
sessionArticleList = []
sessionArticleListPrev = []
searchController = 0
searched = False

startDate = None
endDate = None

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

class InfoForm(FlaskForm):
    startDate = DateField('Start Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    endDate = DateField('End Date', format='%Y-%m-%d', validators=(validators.DataRequired(),))
    submit = SubmitField('Submit')

def updateArticleList(articles):    
    global articleList
    articleList = articles

def sortByDateAscending(list):
    return sorted(list,key=lambda x:x['Year'] , reverse=False)
def sortByDateDescending(list):
    return sorted(list,key=lambda x:x['Year'] , reverse=True)

def filterArticles(list):
    articleFilter = dict()
    newArticleList = []
    
    for article in list:
        if article.get('Doi'):
            if articleFilter.get(article['Doi']):
                continue
            else:
                articleFilter[article['Doi']] = True
                newArticleList.append(article)
        elif article.get('Eprint'):
            if articleFilter.get(article['Eprint']):
                continue       
            else:
                articleFilter[article['Eprint']] = True
                newArticleList.append(article)
        else:
            if article.get('Title'):
                if article.get('Year'):
                    if articleFilter.get(article['Title']):
                        if articleFilter.get(article['Year']):
                            if articleFilter.get(article['Title']).get('Year') == article['Year']:
                                continue
                            else:
                                articleFilter[article['Title']] = {'Year':article['Year']}
                                newArticleList.append(article)
                        else:
                            articleFilter[article['Title']] = {'Year':article['Year']}
                            newArticleList.append(article)
                    else:
                        articleFilter[article['Title']] = {'Year':article['Year']}
                        newArticleList.append(article)
                else:
                    articleFilter[article['Title']] = {'Year':None}
                    newArticleList.append(article)
            else:
                continue
    return newArticleList
                        
    

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
        
        return redirect(url_for('searchResults',txt=text,hep=HEP,arxiv=ARXIV,filters=0))
    else:
        return render_template('index.html')

@app.route('/search_results/<txt>/hep<hep>/arx<arxiv>/filters<filters>' , methods=['GET' ,'POST'])
async def searchResults(txt,hep,arxiv,filters):

    global searchController
    global articleList
    global sessionArticleList
    global sessionArticleListPrev
    global startDate
    global endDate
    global searched

    arxivArticleList = []
    hepArticleList = []
    dbToSearch = []
    listOfApiCalls = []
    index = 0


    form = InfoForm()
    #handle date range submit
    if form.validate_on_submit():
        sessionArticleListPrev = sessionArticleList.copy()
        sessionArticleList.clear()
        tempStartDate = startDate
        tempEndDate = endDate
        startDate = form.startDate.data.strftime("%m/%d/%Y")
        endDate = form.endDate.data.strftime("%m/%d/%Y")
        startYear = int(form.startDate.data.strftime("%Y"))
        endYear = int(form.endDate.data.strftime("%Y"))
        
        for article in articleList:
            if article['Year'] >= startYear and article['Year'] <= endYear:
                print(article['Year'] , startYear , endYear ,article['Title'])
                sessionArticleList.append(article)
        
        sessionArticleList = sortByDateDescending(sessionArticleList)

        if len(sessionArticleList) == 0:
            startDate= tempStartDate
            endDate= tempEndDate
            return render_template('search_results.html' , hep=hep,txt=txt,arxiv=arxiv, results=sessionArticleList , form=form,startDate=startDate,endDate=endDate,searchURL=session.get('searchURL'))
        else:
            searched = True
            return render_template('search_results.html' , hep=hep,arxiv=arxiv,results=sessionArticleList , txt=txt, form=form,startDate=startDate,endDate=endDate,searchURL=session.get('searchURL'))
    
    if request.method == "POST":
        articleID = request.form.get("info")
        return redirect(url_for('articlePage',id = articleID))

 
    elif searchController == 1:
        articleList = []
        sessionArticleList = []
        sessionArticleListPrev = []
        searchController = 0
        searched = False

        startDate = None
        endDate = None

        if (arxiv == 'on'):
            arxivHelper = ArxivHelper()
            queryURL = arxivHelper.allParamSearch(txt)
            listOfApiCalls.append(httpx.AsyncClient().get(queryURL,timeout=100))

        if (hep == 'on'):
            hepHelper = HepHelper()
            url = hepHelper.hepUrlGenerator(txt)
            listOfApiCalls.append(httpx.AsyncClient().get(url,timeout=100))

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

        updateArticleList(sortByDateDescending(filterArticles(hepArticleList + arxivArticleList)))

        if len(articleList) == 0:
            session['searchURL'] = None
        else:
            session['searchURL'] = f"/search_results/{txt}/hep{hep}/arx{arxiv}/filters{filters}"

        return render_template('search_results.html' ,hep=hep,arxiv=arxiv, results=articleList , txt=txt, form=form,startDate=startDate,endDate=endDate,searchURL=session.get('searchURL'))
        
    else:
        if filters == "1":
            sessionArticleList = []
            sessionArticleListPrev = []
            searchController = 0
            searched = False

            startDate = None
            endDate = None
            
            return render_template('search_results.html' , hep=hep,arxiv=arxiv, results=articleList, txt=txt ,form=form,startDate=startDate,endDate=endDate,searchURL=session.get('searchURL'))
        if len(sessionArticleList) == 0 and not searched:
            startDate = None
            endDate = None
            return render_template('search_results.html' ,hep=hep,arxiv=arxiv,  results=articleList, txt=txt ,form=form,startDate=startDate,endDate=endDate,searchURL=session.get('searchURL'))
        elif len(sessionArticleList) == 0 and searched:
            return render_template('search_results.html' , hep=hep,arxiv=arxiv, results=sessionArticleListPrev, txt=txt,form=form,startDate=startDate,endDate=endDate,searchURL=session.get('searchURL'))
        else:
            return render_template('search_results.html' , hep=hep,arxiv=arxiv,results=sessionArticleList, txt=txt,form=form,startDate=startDate,endDate=endDate,searchURL=session.get('searchURL'))

@app.route('/search_results/<id>')
def articlePage(id):

    global articleList
    global sessionArticleList
    global searched
    if searched:
        if len(sessionArticleList) == 0:
            article = sessionArticleListPrev[int(id)]
            bibtex = sessionArticleListPrev[int(id)]['Bibtex']
        else:
            article = sessionArticleList[int(id)]
            bibtex = sessionArticleList[int(id)]['Bibtex']
    else:
        article = articleList[int(id)]
        bibtex = articleList[int(id)]['Bibtex']

    return render_template('article.html' , bibtex=bibtex, article=article ,searchURL = session['searchURL'])


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
