from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from textfiles_parsingbdd import textfiles_management
import sqlite3

bDatos = textfiles_management
conn = sqlite3.connect('tfparsing_bdd.sqlite')
cur = conn.cursor()

def startScraping():
    cur.execute('SELECT id FROM Textos')
    lastText = max([row[0] for row in cur])

    if len(lastText) == 0:
        directoryMap(0) #Empieza una corrida con la base de datos vacía
    else:
        cur.execute('SELECT * FROM Textos WHERE id = ?', (lastText, ))
        lastTextInfo = cur.fetchone()
        lastTextNivel = lastTextInfo[2]
        lastTextPadreId = lastTextInfo[3]

        if lastTextNivel == 1:
            directoryMap(lastTextPadreId - 1) #Comienza parseo desde último directorio registrado en tabla Textos

        elif lastTextNivel == 2:
            cur.execute('SELECT link, directorio_id FROM Subdirectorio WHERE id = ?', (lastTextPadreId, ))
            subdirectorioPadre = cur.fetchone()[0] #link de subdirectorio
            directorioPadreId = cur.fetchone()[1] #id de directorio
            cur.execute('SELECT link FROM Directorio WHERE id = ?', (directorioPadreId, ))
            directorioPadre = cur.fetchone()[0] #link de directorio
            tuplaSub = (directorioPadre, subdirectorioPadre) #(link directorio, link subdirectorio)
            subdirectoryText(tuplaSub)
            directoryMap(directorioPadreId - 1)


def directoryMap(corrida): #El parámetro 'corrida' sirve para indicar desde donde se empieza
    listaPreliminar = []
    html = urlopen("http://www.textfiles.com/directory.html")
    bsObj = BeautifulSoup(html, "html.parser")
    noBuscado = list(bsObj.findAll("a", href=re.compile("(\w+)\.")))
    for link in bsObj.findAll("a", href=re.compile("(\w+)")):
        if link not in noBuscado and if 'href' in link.attrs:
            if link.attrs["href"] == "virus":
                continue
            listaPreliminar.append(link.attrs['href'])
    listaLink = listaPreliminar[corrida:] 
    print("Directorios por parsear:", len(listaLink))
    directoryText(listaLink)
    #subdirectoryText(listaLink) #DEBB


def directoryText(listaLink): #Directorios de primer nivel
    
    cur.execute('SELECT link, padre_id FROM Textos')
    guardianText = [row[0] for row in cur]
    guardianTextId = [row[1] for row in cur]
    cur.execute('SELECT link FROM Directorio')
    guardianDir = [row[0] for row in cur]

    contador = 0
    
    for Dir in listaLink:

        if Dir in guardianDir:
            continue

        html = urlopen("http://www.textfiles.com/%s" % Dir)
        bsObj = BeautifulSoup(html, "html.parser")
            
        for link in bsObj.findAll("a", href=re.compile("(.txt$)")):
            if 'href' in link.attrs:
                tuplaDir= (Dir, link.attrs["href"])
                if tuplaDir[1] in guardianText:
                    print("El archivo %s ya se encuentra registrado en la base de datos." % tuplaDir[1])
                    continue
                bDatos.bdd_insertartexto(tuplaDir, "Directorio")
        
        for link in bsObj.findAll("a", href=re.compile("^[^/]([A-Z]+[0-9]*[^a-z.//]+)")):
            if 'href' in link.attrs:
                tuplaSub = (Dir, link.attrs["href"]) #(link directorio, link subdirectorio)
                subdirectoryText(tuplaSub)

        bDatos.bdd_insertardirectorio(Dir)
        contador += 1
        print("Directorio %d de %d" % (contador, len(listaLink)))


def subdirectoryText(tuplaSub): #Directorios de segundo nivel. (tupla[0] es padre, tupla[1] es hijo)
    
    cur.execute('SELECT link FROM Subdirectorio')
    guardianSub = [row[0] for row in cur]
    cur.execute('SELECT link FROM Textos')
    guardianText = [row[0] for row in cur]
    contador = 0
    padre = tuplaSub[0]
    hijo = tuplaSub[1]

    if hijo in guardianSub: 
        print("El subdirectorio %s ya se encuentra registrado en la base de datos." % tuplaSub[1])
    
    else: 
        html = urlopen("http://www.textfiles.com/%s/%s" % tuplaSub)
        bsObj = BeautifulSoup(html, "html.parser")
            
        for link in bsObj.findAll("a", href=re.compile("(.txt$)")):
            if 'href' in link.attrs:
                tuplaPagina= (hijo, link.attrs["href"])
                
                if tuplaPagina[1] in guardianText:
                    print("El archivo %s ya se encuentra registrado en la base de datos." % tuplaPagina[1])
                    continue
                bDatos.bdd_insertartexto(tuplaPagina, "Subdirectorio")
            
        contador += 1
        print("Subdirectorio %d" % contador)
        bDatos.bdd_insertarsubdirectorio(tuplaSub)

conn.close()  

startScraping()