from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.request
import re

allImgLinks = set()
"""
def getImageLinks(bsObj, imgUrl):
    imgLinks = []
    for link in bsObj.findAll('img',src=re.compile("^(\/|.*"+imgUrl+")")):
        if link.attrs['src'] is not None:
            if link.attrs['src'] not in imgLinks:
                if(link.attrs['src'].startswith("/")):
                    imgLinks.append(urlparse(imgUrl).scheme+":"+link.attrs['src'])
                else:
                    imgLinks.append(link.attrs['src'])
    return imgLinks
"""

def debuggetImageLinks(linkurl, imgUrl):

    html = urlopen(linkurl)
    bsObj = BeautifulSoup(html)
    imgLinks = []

    for link in bsObj.findAll('img',src=re.compile("^(\/|.*"+imgUrl+")")):
        if link.attrs['src'] is not None:
            if link.attrs['src'] not in imgLinks:
                if(link.attrs['src'].startswith("/")):
                    imgLinks.append(urlparse(imgUrl).scheme+":"+link.attrs['src'])
                else:
                    imgLinks.append(link.attrs['src'])
    return imgLinks


def getInternalLinks(bsObj,includeUrl):
    includeUrl = urlparse(includeUrl).scheme+"://"+urlparse(includeUrl).netloc
    internalLinks = []
    for link in bsObj.findAll('a',href=re.compile("^(\/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if(link.attrs['href'].startswith("/")):
                    internalLinks.append(includeUrl+link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])
    return internalLinks

def AllimgGetter(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html)
    domain = urlparse(siteUrl).scheme+"://"+urlparse(siteUrl).netloc
    internalLinks = getInternalLinks(bsObj,domain)
    i = 0
    for link in internalLinks:
        print(link)
        imgLinks = debuggetImageLinks(link,domain)
        for link in imgLinks:
            print("test")
            if link not in allImgLinks:
                allImgLinks.add(link)
                print(link)
                urllib.request.urlretrieve(link,"{0}.jpg".format(i))
                i += 1
                if i > 10:
                    break
#deb
def pageimgGetter(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html)
    domain = urlparse(siteUrl).scheme+"://"+urlparse(siteUrl).netloc
    imgLinks = getImageLinks(bsObj,domain)
    internalLinks = getInternalLinks(bsObj,domain)
    i = 0
    print("test")
    for link in imgLinks:
        if link not in allImgLinks:
            allImgLinks.add(link)
            print(link)
            urllib.request.urlretrieve(link,"{0}.jpg".format(i))
            i += 1

AllimgGetter("http://giphy.com/search/anime-gif")
