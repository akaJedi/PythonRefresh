import random
import time
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import ssl
import urllib.error

# Ignore SSL certificate errors
context = ssl._create_unverified_context()

def getRandomExternalLink(startingSite):
    try:
        req = Request(startingSite, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req, context=context).read()
        soup = BeautifulSoup(html, "html.parser")
        externalLinks = [a.attrs['href'] for a in soup.findAll('a', href=True) if 'http' in a.attrs['href'] and urlparse(a.attrs['href']).netloc != urlparse(startingSite).netloc]
        if len(externalLinks) == 0:
            return None
        return random.choice(externalLinks)
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        if e.code == 429:
            print("Rate limit exceeded. Sleeping for 60 seconds.")
            time.sleep(60)
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def followExternalOnly(startingSite, depth=0, max_depth=3):
    if depth >= max_depth:
        print("Reached maximum depth, stopping recursion.")
        return
    print(f"Random external link is: {startingSite}")
    externalLink = getRandomExternalLink(startingSite)
    if externalLink:
        followExternalOnly(externalLink, depth + 1)
    else:
        print("No external links found, stopping recursion.")

followExternalOnly("http://oreilly.com")
