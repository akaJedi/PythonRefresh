from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html)

for sibling in bsObj.find("table",{"id":"giftList"}).tr.next_siblings:
    print(sibling)


### I did work with chat gpt to enchance the script:
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Context to ignore SSL certificate errors
context = ssl._create_unverified_context()

try:
    html = urlopen("http://www.pythonscraping.com/pages/page3.html", context=context)
    bsObj = BeautifulSoup(html, 'html.parser')
    
    table = bsObj.find("table", {"id": "giftList"})
    if table is not None:
        rows = table.find_all("tr")
        for row in rows:
            print(row)
    else:
        print("Table with id 'giftList' not found.")
except Exception as e:
    print(f"An error occurred: {e}")
