from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import datetime
import random
from urllib.parse import urljoin

pages = set()
random.seed(datetime.datetime.now().timestamp())

# Extract list of internal links found on the page
def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    # Will find all links starting with "/"
    for link in bsObj.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

# Extracting list of all external links found on the page
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # Will find all links starting with http or www and not containing the current address
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").replace("https://", "").split("/")
    return addressParts

def getRandomExternalLink(startingPage):
    req = Request(startingPage, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    bsObj = BeautifulSoup(html, 'html.parser')
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(bsObj, splitAddress(startingPage)[0])
        return getRandomExternalLink(urljoin(startingPage, internalLinks[random.randint(0, len(internalLinks)-1)]))
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print("Random external link is: " + externalLink)
    followExternalOnly(externalLink)

followExternalOnly("http://oreilly.com")
