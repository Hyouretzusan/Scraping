import sqlite3

conn = sqlite3.connect('tfparsing_bdd.sqlite')
cur = conn.cursor()
cur.execute('SELECT id FROM Directorio')
guardian = [row[0] for row in cur]
print(guardian, max(guardian))

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

def listnumero():
    lista2 = [1,2,3,4]
    for numero in lista2:
        a = numero
        b = numero + 1
        suma(a,b)

listnumero()

cur.execute('SELECT link FROM Textos WHERE nivel_id = ?', ("2", ))
revision2 = cur.fetchone()
if revision2 is None:
    print("NONE!")
print("2: ", revision2, type(revision2), cur, "\n")

cur.execute('SELECT id FROM Textos')
lastText = max([row[0] for row in cur])
cur.execute('SELECT * FROM Textos WHERE id = ?', (lastText, ))
lastTextInfo = cur.fetchone()
print("lastText:", lastText, "lastTextInfo:", lastTextInfo)

