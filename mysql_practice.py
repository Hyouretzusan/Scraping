import pymysql

conn = pymysql.connect(host='127.0.0.1', user='claudio', passwd="sonicboom", db='scraping')
cur = conn.cursor()
cur.execute("SELECT * FROM pages WHERE id=1")
print(cur.fetchone())
cur.close()
conn.close()