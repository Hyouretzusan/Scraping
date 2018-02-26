from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())
def buscarLinks(linkUrl):
    html = urlopen("http://en.wikipedia.org" + linkUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",\
    href=re.compile("^(/wiki/)((?!:).)*$"))

print("Ingrese la parte final del link de wikipedia que desea evaluar")
linkUsu = input("tal como aparece en su navegador. [Ej: Kevin_Bacon]: ")
linksWiki = buscarLinks("/wiki/" + linkUsu)

while len(linksWiki) > 0:
    nuevoLink = linksWiki[random.randint(0, len(linksWiki)-1)].attrs["href"]
    print(nuevoLink)
    linksWiki = buscarLinks(nuevoLink)