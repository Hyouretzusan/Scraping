from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now()) #Inicia el numero random con la hora del pc

def buscarLinks(linkUrl): #Genera el objeto BS, y extrae los links
    
    html = urlopen("http://en.wikipedia.org" + linkUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a",\
    href=re.compile("^(/wiki/)((?!:).)*$")) #Genera una lista de links

print("Ingrese la parte final del link de wikipedia que desea evaluar")
linkUsu = input("tal como aparece en su navegador. [Ej: Kevin_Bacon]: ")
linksWiki = buscarLinks("/wiki/" + linkUsu)

while len(linksWiki) > 0: #Recibe la lista de links y escoge uno al azar
    nuevoLink = linksWiki[random.randint(0, len(linksWiki)-1)].attrs["href"]
    print(nuevoLink)
    linksWiki = buscarLinks(nuevoLink)