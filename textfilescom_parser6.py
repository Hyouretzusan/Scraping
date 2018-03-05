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
    cur.execute('SELECT link, padre_id FROM Textos')
    guardianText = [row[0] for row in cur]
    guardianTextId = [row[1] for row in cur]
    cur.execute('SELECT link FROM Subdirectorio')
    guardianSub = [row[0] for row in cur]
    cur.execute('SELECT link FROM Directorio')
    guardianDir = [row[0] for row in cur]

    final = len(guardianDir) - len(listaLink)
    contador = 0
    
    for pagina in listaLink:

        cur.execute('SELECT id FROM Directorio WHERE link = ?', (pagina, ))
        revision = cur.fetchone()[0]
        
        if revision and (revision + 1) in guardianTextId: #Deja pasar el ultimo elemento siempre
            print("La base de datos ya contiene todos los registros del directorio: %s" % pagina)
            continue

        html = urlopen("http://www.textfiles.com/%s" % pagina)
        bsObj = BeautifulSoup(html, "html.parser")
        
        for link in bsObj.findAll("a", href=re.compile("(.txt$)")):
            if 'href' in link.attrs:
                tuplaPagina= (pagina, link.attrs["href"])
                if tuplaPagina[1] in guardianText: #Podria dejar pasar la lista, y poner el guardian directamente en bdd_insertartexto 
                    print("El archivo %s ya se encuentra registrado en la base de datos." % tuplaPagina[1])
                    continue
                bDatos.bdd_insertartexto(tuplaPagina, "Directorio")
        contador += 1
        print("Directorio %d de %d" % (contador,final))

        for link in bsObj.findAll("a", href=re.compile("^[^/]([A-Z]+[0-9]*[^a-z.//]+)")):
            if 'href' in link.attrs:
                tuplaSub = (pagina, link.attrs["href"])
                subdirectoryText(tuplaSub)
                if tuplaSub[1] in guardianSub: #Podria dejar pasar la lista, y poner el guardian directamente en bdd 
                    print("El subdirectorio %s ya se encuentra registrado en la base de datos." % tuplaSub[1])
                    continue
                bDatos.bdd_insertarsubdirectorio(tuplaSub)
    conn.close()
    #return(bDatos.bdd_insertartexto(listaPagina, "Directorio"), bDatos.bdd_insertarsubdirectorio(listaSub), subdirectoryText(listaSub))
    #print(listaPagina) #DEBB 


def subdirectoryText(tuplaSub): #Directorios de segundo nivel. (tupla[0] es padre, tupla[1] es hijo)

    conn = sqlite3.connect('tfparsing_bdd.sqlite')
    cur = conn.cursor()
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
            if tuplaPagina[1] in guardianText: #Podria dejar pasar la lista, y poner el guardian directamente en bdd_insertartexto 
                print("El archivo %s ya se encuentra registrado en la base de datos." % tuplaPagina[1])
                continue
            bDatos.bdd_insertartexto(tuplaPagina, "Subdirectorio")
        
        contador += 1
        print("Subdirectorio %d" % contador)       
    conn.close()     
    
    #return(bDatos.bdd_insertartexto(listaPagina, "Subdirectorio"))
    #print(listaPagina) #DEBB 

directoryMap()

"""Debo realizar el algoritmo de manera que empiece en un directorio, vaya guardando los textos de ese directorio por un lado
y los subdirectorios del texto por otro. Teniendo los subdirectorios, vaya recorriendo uno por uno para ir guardando sus respectivos
textos. Los registros se irán guardando en la base de datos a medida que se generan y, cuando quiera reiniciar el parser, deberá
consultar en la base de datos para determinar en cuál fue el último directorio en que se quedó, y empezar desde cero en ese directorio, 
incluso si ya lo había recorrido casi todo anteriormente. Eso evitará que se me escapen registros en caso de un paro inesperado. Para evitar
duplicidad, en este algoritmo, los guardianes estarán implementados justo en el momento antes de insertar el registro en la base de datos

REHACER EL PARSER PARA QUE SOLO PASE AL SIGUIENTE DIRECTORIO SI YA RECORRIÓ TODO EL DIRECTORIO ANTERIOR, INCLUÍDOS LOS SUBDIRECTORIOS"""