from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1', user='claudio', passwd='sonicboom', db='wikipedia', charset='utf8')
cur = conn.cursor()


def insertPageIfNotExists(url):
    print(url)
    cur.execute("SELECT * FROM pages WHERE url = %s", (url))
    if cur.rowcount == 0:
        print("Inserting page")
        cur.execute("INSERT INTO pages (url) VALUES (%s)", (url))
        conn.commit()
        return cur.lastrowid
    else:
        print("Page exists. Returning id")
        return cur.fetchone()[0]


def insertLink(fromPageId, toPageId):
    cur.execute("SELECT * FROM links WHERE fromPageId = %s AND toPageId = %s", (int(fromPageId), int(toPageId)))
    if cur.rowcount == 0:
        print("Inserting link")
        cur.execute("INSERT INTO links (fromPageId, toPageId) VALUES (%s, %s)", (int(fromPageId), int(toPageId)))
        conn.commit()


pages = set()
def getLinks(pageUrl, recursionLevel): #recibe un link, y el nivel de recursion
    global pages
    print("Recursion:", recursionLevel)
    if recursionLevel > 4:
        exit()
    pageId = insertPageIfNotExists(pageUrl)
    html = urlopen("http://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html, 'html.parser')
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        print(link)
        insertLink(pageId, insertPageIfNotExists(link.attrs['href']))
        if link.attrs['href'] not in pages:
            print("We have encountered a new page, add it and search it for links")
            newPage = link.attrs['href']
            pages.add(newPage)
            getLinks(newPage, recursionLevel+1)


getLinks("/wiki/Kevin_Bacon", 0)
cur.close()
conn.close()
