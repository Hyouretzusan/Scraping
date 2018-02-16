from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

preciosLista = list()
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, 'html.parser')
tdTags = bsObj.findAll("td")

for tag in tdTags:
    tagStr = str(tag)
    if "$" in tagStr:
        precios = re.findall('\$([0-9.,]*)\s', tagStr)
        preciosLista.append(precios[0])

print(preciosLista)
