from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from textfiles_parsingbdd import textfiles_management
import sqlite3

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
    
    conn = sqlite3.connect('tfparsing_bdd.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT link FROM Textos')
    guardianText = [row[0] for row in cur]
    cur.execute('SELECT link FROM Subdirectorio')
    guardianSub = [row[0] for row in cur]
    cur.execute('SELECT link FROM Directorio')
    guardianDir = [row[0] for row in cur]

    listaPagina = []
    listaSub = []
    final = len(guardianDir) - len(listaLink)
    contador = 0
    
    for pagina in listaLink:

        cur.execute('SELECT id FROM Directorio WHERE link = ?', (pagina, ))
        revision = cur.fetchone()[0]
        
        if revision and (revision + 1): #Deja pasar el ultimo elemento siempre
            continue

        html = urlopen("http://www.textfiles.com/%s" % pagina)
        bsObj = BeautifulSoup(html, "html.parser")
        
        for link in bsObj.findAll("a", href=re.compile("(.txt$)")):
            if 'href' in link.attrs:
                tuplaPagina= (pagina, link.attrs["href"])
                if tuplaPagina[1] in guardianText: #Podria dejar pasar la lista, y poner el guardian directamente en bdd_insertartexto 
                    continue
                listaPagina.append(tuplaPagina)
        contador += 1
        print("Directorio %d de" % contador, "%d" % final)

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