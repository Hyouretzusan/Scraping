import pymysql

class kevinbacon_management:
    def __init__(self):
        print("")


    def bdd_consultartabla():
        conn = pymysql.connect(host='127.0.0.1', user='claudio', passwd="sonicboom", db='scraping', charset='utf8')
        cur = conn.cursor()
        
        cur.execute('SELECT * FROM pages')
        
        existencia = cur.fetchall()

        if len(existencia) == 0:
            print("\nNo hay registros")
        
        else:
            print("La base de datos contiene los siguientes registros:\n")
            for row in existencia:
                print(row)
        conn.close()

    def bdd_borrartabla():
        conn = pymysql.connect(host='127.0.0.1', user='claudio', passwd="sonicboom", db='scraping', charset='utf8')
        cur = conn.cursor()
        
        cur.execute('TRUNCATE TABLE pages')
        
        existencia = cur.fetchall()
        print("Borrada!")
        conn.close()