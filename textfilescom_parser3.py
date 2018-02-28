from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from textfiles_parsingbdd import textfiles_management

listaLink = []
bDatos = textfiles_management

def directoryMap():
    html = urlopen("http://www.textfiles.com/directory.html")
    bsObj = BeautifulSoup(html, "html.parser")
    noBuscado = list(bsObj.findAll("a", href=re.compile("(\w+)\.")))
    for link in bsObj.findAll("a", href=re.compile("(\w+)")):
        if link not in noBuscado:
            if 'href' in link.attrs:
                listaLink.append(link.attrs["href"])
    listaLink.remove("virus")
    return(bDatos.bdd_insertardirectorio(listaLink), subdirectoryText(listaLink))
    #return(subdirectoryText(listaLink)) #DEBB

def subdirectoryText(listaLink):
    #print(listaLink) #DEBB
    listaPagina = []
    final = len(listaLink)
    contador = 0
    for pagina in listaLink:
        #while contador < 2: #DEBB
        html = urlopen("http://www.textfiles.com/%s" % pagina)
        bsObj = BeautifulSoup(html, "html.parser")
        for link in bsObj.findAll("a", href=re.compile("(.txt$)")):
            if 'href' in link.attrs:
                tuplaPagina= (pagina, link.attrs["href"])
                listaPagina.append(tuplaPagina)
        contador += 1
        print("Subdirectorio %d de" % contador, "%d por agregar" % final)
    return(bDatos.bdd_insertartexto2(listaPagina))
    #print(listaPagina) #DEBB
        
directoryMap()