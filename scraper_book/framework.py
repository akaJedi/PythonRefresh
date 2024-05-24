import random
import time
from urllib.request import urlopen, Request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
context = ssl._create_unverified_context()

def get_random_external_link(starting_site):
    try:
        req = Request(starting_site, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req, context=context).read()
        soup = BeautifulSoup(html, "html.parser")
        external_links = [a.attrs['href'] for a in soup.find_all('a', href=True) 
                          if 'http' in a.attrs['href'] and urlparse(a.attrs['href']).netloc != urlparse(starting_site).netloc]
        return random.choice(external_links) if external_links else None
    except:
        return None

def follow_external_only(starting_site, depth=0, max_depth=3, output_to_screen=False):
    if depth >= max_depth:
        return
    message = f"Random external link is: {starting_site}"
    if output_to_screen:
        print(message)
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")
    external_link = get_random_external_link(starting_site)
    if external_link:
        follow_external_only(external_link, depth + 1, max_depth, output_to_screen)

if __name__ == "__main__":
    protocol = input("Enter the protocol (http or https): ").strip().lower()
    domain = input("Enter the domain (e.g., oreilly.com): ").strip()
    start_url = f"{protocol}://{domain}"
    max_depth = int(input("Enter the maximum depth: "))
    output_option = input("Output to screen as well? (y/n, default is n): ").strip().lower() == 'y'
    follow_external_only(start_url, max_depth=max_depth, output_to_screen=output_option)
