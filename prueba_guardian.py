import sqlite3

conn = sqlite3.connect('tfparsing_bdd.sqlite')
cur = conn.cursor()
cur.execute('SELECT link FROM Directorio')
guardian = [row[0] for row in cur]
print(guardian)

cur.execute('SELECT id FROM Directorio WHERE link = ?', ("adventure", ))
revision = cur.fetchone()[0]
print(revision, type(revision))

lista = [1,2,3,4]
if 4 and 4+1 in lista:
    print(True)
else:
    print(False)

def suma(a, b):
    print(a + b)

def listnumero(suma):
    lista2 = [1,2,3,4]
    for numero in lista2:
        a = numero
        b = numero + 1
        suma(a,b)