from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html", context=ctx)
bsObj = BeautifulSoup(html, 'html.parser')
nomLista = bsObj.findAll("span", {"class":"green"})
for nombre in nomLista:
    print(nombre.get_text())