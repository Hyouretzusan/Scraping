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
    return(bDatos.bdd_insertardirectorio(listaLink), directoryText(listaLink))
    #return(subdirectoryText(listaLink)) #DEBB


def directoryText(listaLink): #Directorios de primer nivel
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
    return(bDatos.bdd_insertartexto(listaPagina, "Directorio"), bDatos.bdd_insertarsubdirectorio(listaSub), subdirectoryText(listaSub))
    #print(listaPagina) #DEBB 


def subdirectoryText(listaSub): #Directorios de segundo nivel. (tupla[0] es padre, tupla[1] es hijo)
    listaPagina = []
    final = len(listaSub)
    contador = 0
    for tupla in listaSub:
        padre = tupla[0]
        hijo = tupla[1]
        html = urlopen("http://www.textfiles.com/%s/%s" % tupla)
        bsObj = BeautifulSoup(html, "html.parser")
        
        for link in bsObj.findAll("a", href=re.compile("(.txt$)")):
            if 'href' in link.attrs:
                tuplaPagina= (hijo, link.attrs["href"])
                listaPagina.append(tuplaPagina)
        
        contador += 1
        print("Subdirectorio %d de %d" % (contador, final))            
    
    return(bDatos.bdd_insertartexto(listaPagina, "Subdirectorio"))
    #print(listaPagina) #DEBB 

directoryMap()