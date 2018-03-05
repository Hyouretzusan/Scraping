import sqlite3

class textfiles_management:
    def __init__(self):
        print("")


    def bdd_creartabla():
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS Directorio')
        cur.execute('CREATE TABLE Directorio (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, link TEXT, nivel INTEGER)')
        cur.execute('DROP TABLE IF EXISTS Subdirectorio')
        cur.execute('CREATE TABLE Subdirectorio (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, link TEXT, nivel INTEGER, directorio_id INTEGER, UNIQUE(id, directorio_id))')
        cur.execute('DROP TABLE IF EXISTS Textos')
        cur.execute('CREATE TABLE Textos (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, link TEXT, nivel_id INTEGER, padre_id INTEGER, UNIQUE(id, nivel_id))')
        print("LA BASE DE DATOS HA SIDO INICIADA")
        conn.commit()
        conn.close()


    def bdd_insertardirectorio(listaLink):

        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        cur.execute('SELECT link FROM Directorio')
        guardian = [row[0] for row in cur]
        
        for linkDir in listaLink:
            if linkDir == "virus":
                continue
            elif linkDir in guardian:
                print("El directorio %s ya se encuentra registrado" % linkDir)
                continue
            else:
                cur.execute('INSERT INTO Directorio (link, nivel) VALUES (?, ?)', (linkDir, 1))
                conn.commit()
                print("Registrado directorio: %s" % linkDir)
        conn.close()


    def bdd_insertarsubdirectorio(tuplaSub):
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        directorioPadre = tuplaSub[0]
        directorioHijo = tuplaSub[1]
            
        cur.execute('SELECT * FROM Directorio WHERE link = ?', (directorioPadre, ))
        direct_id = cur.fetchone()[0]
        cur.execute('INSERT INTO Subdirectorio (link, directorio_id, nivel) VALUES (?, ?, ?)', (directorioHijo, direct_id, 2))
        conn.commit()
            
        print("Registrado subdirectorio: %s" % directorioHijo)
        conn.close()


    def bdd_insertartexto(tuplaPagina, nivelPagina):
        if len(tuplaPagina) == 0:
            continue
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
            
        if nivelPagina == "Directorio":
            cur.execute('SELECT * FROM Directorio WHERE link = ?', (tuplaPagina[0], ))
        elif nivelPagina == "Subdirectorio":
            cur.execute('SELECT * FROM Subdirectorio WHERE link = ?', (tuplaPagina[0], ))
            
        directPadre = cur.fetchone()
        direct_id = directPadre[0]
        nivl_id = directPadre[2]
            
        cur.execute('INSERT INTO Textos (link, nivel_id, padre_id) VALUES (?, ?, ?)', (tuplaPagina[1], nivl_id, direct_id))
        conn.commit()

        if nivelPagina == "Directorio":
            print("Directorio %s. Texto registrado: %s" % (tuplaPagina[0],tuplaPagina[1]))
        elif nivelPagina == "Subdirectorio":
            print("Subirectorio %s. Texto registrado: %s" % (tuplaPagina[0],tuplaPagina[1]))
        conn.close()


    def bdd_consultartabla(tabla):
        conn = sqlite3.connect('tfparsing_bdd.sqlite')
        cur = conn.cursor()
        
        if tabla == "Directorio":
            cur.execute('SELECT link FROM Directorio')
        elif tabla == "Subdirectorio":
            cur.execute('SELECT link FROM Subdirectorio')
        elif tabla == "Textos":
            cur.execute('SELECT link FROM Textos')
        
        existencia = cur.fetchall()

        if len(existencia) == 0:
            print("\nNo hay registros para la tabla %s" % tabla)
        
        else:
            print("La base de datos contiene los siguientes registros:\n")
            for row in existencia:
                print(row[0])
        conn.close()
