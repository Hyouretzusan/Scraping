from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

listaLink = []
def directoryMap():
    html = urlopen("http://www.textfiles.com/directory.html")
    bsObj = BeautifulSoup(html, "html.parser")
    noBuscado = list(bsObj.findAll("a", href=re.compile("(\w+)\.")))
    for link in bsObj.findAll("a", href=re.compile("(\w+)")):
        if link not in noBuscado:
            if 'href' in link.attrs:
                listaLink.append(link.attrs["href"])
    return(directorySearch(listaLink))


def directorySearch(listaLink): #solo esta pasando '100'
    for pagina in listaLink:
        listaPagina = []
        html = urlopen("http://www.textfiles.com/%s" % pagina)
        bsObj = BeautifulSoup(html, "html.parser")
        for link in bsObj.findAll("a", href=re.compile("(.txt$)")):
            #if link not in noBuscado:
            if 'href' in link.attrs:
                listaPagina.append(link.attrs["href"])
        print(listaPagina)

directoryMap()