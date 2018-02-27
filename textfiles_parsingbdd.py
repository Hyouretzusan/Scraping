import sqlite3

class textfiles_management:
    def __init__(self):
        print("")


    def bdd_creartabla():
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS Directorio')
        cur.execute('CREATE TABLE Directorio (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, link TEXT, nivel)')
        cur.execute('DROP TABLE IF EXISTS Subdirectorio')
        cur.execute('CREATE TABLE Subdirectorio (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, link TEXT, nivel, directorio_id INTEGER, UNIQUE(id, directorio_id))')
        cur.execute('DROP TABLE IF EXISTS Textos')
        cur.execute('CREATE TABLE Textos (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, link TEXT, nivel_id INTEGER, padre_id INTEGER, UNIQUE(id, nivel_id))')
        print("LA BASE DE DATOS HA SIDO INICIADA")
        conn.commit()
        conn.close()


    def bdd_insertardirectorio(listaLink):
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        for linkDir in listaLink:
            cur.execute('INSERT INTO Directorio (link, nivel) VALUES (?, ?)', (linkDir, 1))
            conn.commit()
            print("%s registrado" % linkDir)
        conn.close()


    def bdd_insertarsubdirectorio(linkDir, linkSub):
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Directorio WHERE link = ?', (linkDir, ))
        direct_id = cur.fetchone()[0]
        cur.execute('INSERT INTO Subdirectorio (link, directorio_id, nivel) VALUES (?, ?, ?)', (linkSub, direct_id, 2))
        conn.commit()
        print("Directorio %s registrado" % linkDir)
        conn.close()


    def bdd_insertartexto2(listaPagina): #txt segundo nivel: directorio, archivo
        for tupla in listaPagina:
            if len(tupla) == 0:
                continue
            conn = sqlite3.connect('tfparsing_bdd.sqlite')
            cur = conn.cursor()
            cur.execute('SELECT * FROM Directorio WHERE link = ?', (tupla[0], ))
            directPadre = cur.fetchone()
            direct_id = directPadre[0]
            nivl_id = directPadre[2]
            cur.execute('INSERT INTO Textos (link, nivel_id, padre_id) VALUES (?, ?, ?)', (tupla[1], nivl_id, direct_id))
            conn.commit()
            print("Texto %s registrado " % tupla[1], "Hijo de %s" % tupla[0])
        conn.close()


    def bdd_consultartabla(tabla):
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        
        if tabla == "Directorio":
            cur.execute('SELECT * FROM Directorio')
        elif tabla == "Subdirectorio":
            cur.execute('SELECT * FROM Subdirectorio')
        elif tabla == "Textos":
            cur.execute('SELECT * FROM Textos')
        
        print("La base de datos contiene los siguientes registros:\n")
        for row in cur:
            if row is None:
                print("No hay registros")
            else:
                print(row)
        conn.close()


    def bdd_borrartrabajador(cedTrab):
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Trabajador WHERE cedula = ?', (cedTrab,))
        trab_id = cur.fetchone()[0]
        cur.execute('DELETE FROM Familiar WHERE trabajador_id = ?', (trab_id,))
        cur.execute('DELETE FROM Trabajador WHERE cedula = ?', (cedTrab,))
        conn.commit()
        conn.close()
        print("\nTrabajador eliminado")


    def bdd_borrarfamiliar(cedFam):
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        cur.execute('DELETE FROM Familiar WHERE cedula = ?', (cedFam,))
        conn.commit()
        conn.close()
        print("\nFamiliar eliminado")


    def bdd_cargafamiliar(cedTrab):
        contador = 0
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT * FROM Trabajador WHERE cedula = ?', (cedTrab,))
        trab_id = cur.fetchone()[0]
        cur.execute('SELECT * FROM Trabajador JOIN Familiar ON Trabajador.id = Familiar.trabajador_id WHERE Trabajador.id = ?', (trab_id,))
        #carga = cur.fetchone()
        #print("El trabajador: ", carga[1:4])
        #print("Tiene los siguientes familiares: ")
        for row in cur:
            if contador == 0:
                print("El trabajador:", row[1:5])
                print("\nTiene los siguientes familiares:")
                contador = contador + 1
            print(row[6:10])
        conn.close()