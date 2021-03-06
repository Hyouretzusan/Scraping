from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from textfiles_parsingbdd2 import textfiles_management
import sqlite3

bDatos = textfiles_management

def startScraping():
    conn = sqlite3.connect('tfparsing_bdd.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT id FROM Textos')
    lastText = [row[0] for row in cur]

    if len(lastText) == 0:
        directoryMap(0) #Empieza una corrida con la base de datos vacía
        #print("HOLA!") #DEBB
    else:
        maxLastText = max(lastText)
        cur.execute('SELECT * FROM Textos WHERE id = ?', (maxLastText, ))
        lastTextInfo = cur.fetchone()
        lastTextNivel = lastTextInfo[2]
        lastTextPadreId = lastTextInfo[3]

        if lastTextNivel == 1:
            #print("Id padre:",lastTextPadreId) #DEBB
            directoryMap(lastTextPadreId - 1) #Comienza parseo desde último directorio registrado en tabla Textos

        elif lastTextNivel == 2:
            print("HOLA!", lastTextInfo) #DEBB
            cur.execute('SELECT link, directorio_id FROM Subdirectorio WHERE id = ?', (lastTextPadreId, ))
            miSub = cur.fetchone()
            subdirectorioPadre = miSub[0] #link de subdirectorio
            directorioPadreId = miSub[1] #id de directorio
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
        if link not in noBuscado and 'href' in link.attrs:
            if link.attrs["href"] == "virus":
                continue
            listaPreliminar.append(link.attrs['href'])
    listaLink = listaPreliminar[corrida:] 
    print("Directorios por parsear:", len(listaLink))
    #bDatos.bdd_insertardirectorio(listaLink)
    directoryText(listaLink)
    #subdirectoryText(listaLink) #DEBB


def directoryText(listaLink): #Directorios de primer nivel
    #print(listaLink) #DEBB
    
    conn = sqlite3.connect('tfparsing_bdd.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT link, padre_id FROM Textos')
    guardianText = [row[0] for row in cur]
    guardianTextId = [row[1] for row in cur]
    cur.execute('SELECT link FROM Directorio')
    guardianDir = [row[0] for row in cur]
    cur.execute('SELECT link FROM Subdirectorio')
    guardianSub = [row[0] for row in cur]

    contador = 0
    
    for Dir in listaLink: #Por cada directorio en la lista recibida, se ejecuta el siguiente codigo

        if Dir not in guardianDir: #En caso de reinicio, evito volver a registrar un directorio en bdd
            bDatos.bdd_insertardirectorio(Dir)
        else:
            print("El directorio %s ya estaba registrado. Revisando contenido." % Dir)

        #El siguiente codigo, consulta el contenido del directorio, y separa textos de subdirectorios
        html = urlopen("http://www.textfiles.com/%s" % Dir)
        bsObj = BeautifulSoup(html, "html.parser")
            
        for link in bsObj.findAll("a", href=re.compile("(.txt$)")): #Recorre todos los textos en el directorio
            if 'href' in link.attrs:
                tuplaDir= (Dir, link.attrs["href"])
                if tuplaDir[1] in guardianText: #Evita duplicidad de textos en caso de reinicio
                    print("El archivo %s ya se encuentra registrado en la base de datos." % tuplaDir[1])
                    continue
                bDatos.bdd_insertartexto(tuplaDir, "Directorio") #Va guardando los textos a medida que los lee"""
                #print("Tupla directorios:", tuplaDir) #DEBB
        
        for link in bsObj.findAll("a", href=re.compile("^[^/]([A-Z]+[0-9]*[^a-z.//]+)")): #Recorre todos los subs en el directorio
            if 'href' in link.attrs:
                tuplaSub = (Dir, link.attrs["href"]) #(link directorio, link subdirectorio)
                if tuplaSub[1] not in guardianSub: #Evita duplicidad de textos en caso de reinicio
                    bDatos.bdd_insertarsubdirectorio(tuplaSub)
                else:
                    print("El subdirectorio %s ya estaba registrado. Revisando contenido" % tuplaSub[1])
                subdirectoryText(tuplaSub) #Genera los links para subdirectorios uno por uno, y los pasa
                print("Tupla subdirectorios:", tuplaSub) #DEBB

        #bDatos.bdd_insertardirectorio(Dir) #Solo guardará un directorio en bdd cuando ambos for anteriores se cumplan
        contador += 1
        print("Directorio %d de %d" % (contador, len(listaLink))) 
        

def subdirectoryText(tuplaSub): #Subdirectorios. (tupla[0] es directorio, tupla[1] es subdirectorio)
    conn = sqlite3.connect('tfparsing_bdd.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT link FROM Subdirectorio')
    guardianSub = [row[0] for row in cur] 
    cur.execute('SELECT link FROM Textos')
    guardianText = [row[0] for row in cur]
    contador = 0
    padre = tuplaSub[0]
    hijo = tuplaSub[1]

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
        #bDatos.bdd_insertarsubdirectorio(tuplaSub) #Solo guarda en bdd cuando haya recorrido todos los txt dentro del sub
    conn.close()  

startScraping()