import random
import time
import logging
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import ssl
import urllib.error

# Configure logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        logging.error(f"HTTPError: {e.code} {e.reason}")
        if e.code == 429:
            logging.warning("Rate limit exceeded. Sleeping for 60 seconds.")
            time.sleep(60)
        return None
    except Exception as e:
        logging.error(f"Exception: {e}")
        return None

def followExternalOnly(startingSite, depth=0, max_depth=3):
    if depth >= max_depth:
        logging.info("Reached maximum depth, stopping recursion.")
        return
    logging.info(f"Random external link is: {startingSite}")
    externalLink = getRandomExternalLink(startingSite)
    if externalLink:
        followExternalOnly(externalLink, depth + 1, max_depth)
    else:
        logging.info("No external links found, stopping recursion.")

if __name__ == "__main__":
    start_url = "http://oreilly.com"
    max_depth = int(input("Enter the maximum depth: "))
    followExternalOnly(start_url, max_depth=max_depth)
