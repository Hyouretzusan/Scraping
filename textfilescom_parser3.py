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


def subdirectoryText(listaLink): #Directorios de primer nivel
    #print(listaLink) #DEBB
    listaPagina = []
    listaSub = []
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
        print("Subdirectorio %d de" % contador, "%d" % final)

        for link in bsObj.findAll("a", href=re.compile("^[^/]([A-Z]+[0-9]*[^a-z.//]+)")):
            if 'href' in link.attrs:
                tuplaSub = (pagina, link.attrs["href"])
                listaSub.append(tuplaSub)
    return(bDatos.bdd_insertartexto(listaPagina), bDatos.bdd_insertarsubdirectorio(listaSub)) #Falta bDatos.bdd_insertartexto(listaSub)
    #print(listaPagina) #DEBB 
    #return(subdirectoryMap(listaLink)) #DEBB subdirectoryMap
        
directoryMap()