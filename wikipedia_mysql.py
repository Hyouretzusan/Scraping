from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import pymysql
import re

conn = pymysql.connect(host='127.0.0.1', user='claudio', passwd="sonicboom", db='scraping', charset='utf8')
cur = conn.cursor()
random.seed(datetime.datetime.now())

def store(title, content):
    print("Storing:", title, content)
    cur.execute("INSERT INTO pages (title, content) VALUES (\"%s\",\"%s\")", (title, content))
    cur.connection.commit()

def getLinks(articleUrl):
    print("Getting links")
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    title = bsObj.find("h1", {"id":"firstHeading"}).get_text()
    content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
    print(title, type(title), content, type(content)) #DEBB
    store(title, content)
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")
linkst = type(links)
linksl = len(links)
print("links tipo %s, len %d" % (linkst, linksl))
try:
    while len(links) > 0:
        print("New article")
        newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
        print(newArticle)
        links = getLinks(newArticle)
finally:
    cur.close()
    conn.close()