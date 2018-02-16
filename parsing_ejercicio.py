from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import ssl

def getTitle(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        html = urlopen(url, context=ctx)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'html.parser')
        titulo = bsObj.body.h1
    except AttributeError as e:
        return None
    return titulo

linkUsu = input("Ingrese una url: ")    
tituloUsu = getTitle(linkUsu)
if tituloUsu == None:
    print("El título de la página no fue encontrado")
else:
    print(tituloUsu)