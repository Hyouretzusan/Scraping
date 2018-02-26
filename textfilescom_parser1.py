from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://www.textfiles.com/directory.html")
bsObj = BeautifulSoup(html, "html.parser")
noBuscado = list(bsObj.findAll("a", href=re.compile("(\w+)\.")))
for link in bsObj.findAll("a", href=re.compile("(\w+)")):
    if link not in noBuscado:
        if 'href' in link.attrs:
            print(link.attrs['href'])