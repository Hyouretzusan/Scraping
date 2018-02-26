from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def directoryMap():
    html = urlopen("http://www.textfiles.com/directory.html")
    bsObj = BeautifulSoup(html, "html.parser")
    noBuscado = list(bsObj.findAll("a", href=re.compile("(\w+)\.")))
    for link in bsObj.findAll("a", href=re.compile("(\w+)")):
        if link not in noBuscado:
            if 'href' in link.attrs:
                #linkStr = str(link.attrs['href'])
                #directoryList = directoryList.append(linkStr)
                linkSearch = link.attrs["href"] #directorySearch(link.attrs["href"])
                return(directorySearch(linkSearch))


def directorySearch(linkSearch): #solo esta pasando '100'
    print("http://www.textfiles.com/%s" % linkSearch)
    """html = urlopen("http://www.textfiles.com/%s" % linkSearch)
    bsObj = BeautifulSoup(html, "html.parser")
    for link in bsObj.findAll("a"):
        print(link)"""

directoryMap()