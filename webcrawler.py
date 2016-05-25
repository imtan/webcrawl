from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.error import URLError
import re
from datetime import datetime
import random
import time
def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(),"html.parser")
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title


def getURL(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html,"html.parser")
    except AttributeError as e:
        return None
    return bsObj

"""
#1章
title = getTitle("http://www.pythonscraping.com/pages/page1.html")
if title == None:
    print("Title could not be found")
else:
    print(title)
#2-1
bsObj = getURL("http://www.pythonscraping.com/pages/warandpeace.html")
if bsObj == None:
    print("URL could not be found")
nameList = bsObj.findAll("span",{"class":"green"})
for name in nameList:
    print(name.get_text())

#2-2
bsObj = getURL("http://www.pythonscraping.com/pages/page3.html")
for child in bsObj.find("table",{"id":"giftList"}).children:
    print(child)

for sibling in bsObj.find("table",{"id":"giftList"}).tr.next_siblings:
    print(sibling)

print(bsObj.find("img",{"src":"../img/gifts/img1.jpg"
                        }).parent.previous_sibling.get_text())

#2-4
images = bsObj.findAll("img",{"src":re.compile("\.\.\/img\/gifts/img.*\.jpg")})
for image in images:
    print(image["src"])

"""
#bsObj = getURL("http://en.wikipedia.org/wiki/Kevin_Bacon")
"""
for link in bsObj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])

for link in bsObj.find("div",{"id":"bodyContent"}).findAll("a",
                                                           href=re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])
"""
"""
random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find("div",{"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0,len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)
"""
"""
pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id="mw-context-text").findAll("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("This page is missing something! No worries though!")
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print("---------------\n"+newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")
"""

pages = set()
random.seed(datetime.now())

def getInternalLinks(bsObj, includeUrl):
    includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
    internalLinks = []
    for link in bsObj.findAll("a",href=re.compile("^(\/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks


def getExternalLinks(bsObj,  excludeUrl):
    externalLinks = []
    for link in bsObj.findAll("a", href=re.compile(
            "^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print("No external links, looking around the site for one")
        domain = (urlparse(startingPage).scheme+"://"+urlparse(startingPage).netloc)
        internalLinks = getInternalLinks(bsObj,startingPage)
        return getRandomExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("Random external link is: " +externalLink)
    followExternalOnly(externalLink)



#get all link
#followExternalOnly("http://en.wikipedia.org")

allExtLinks = set()
allIntLinks = set()

def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    domain = urlparse(siteUrl).scheme+"://"+urlparse(siteUrl).netloc
    bsObj = BeautifulSoup(html)
    internalLinks = getInternalLinks(bsObj,domain)
    externalLinks = getExternalLinks(bsObj,domain)

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            allIntLinks.add(link)
            getAllExternalLinks(link)

#allIntLinks.add("http://oreilly.com")
#allIntLinks.add("http://giphy.com/search/yuru-yuri")
getAllExternalLinks("http://oreilly.com")
#getAllExternalLinks("http://giphy.com/search/yuru-yuri")

#followExternalOnly("http://oreilly.com")
