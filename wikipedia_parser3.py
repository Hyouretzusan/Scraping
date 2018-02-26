from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

paginas = set()
limite = len(paginas) + 9

def buscarLinks(paginaUrl):
    global paginas    
    global limite
    while len(paginas) <= limite:
    
        html = urlopen("http://en.wikipedia.org" + paginaUrl)
        bsObj = BeautifulSoup(html, "html.parser")
        for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
            if 'href' in link.attrs:
                if link.attrs['href'] not in paginas:
                    nuevaPagina = link.attrs['href']
                    print(len(paginas), nuevaPagina, limite)
                    paginas.add(nuevaPagina)
                    buscarLinks(nuevaPagina)
    else:
        exit()

buscarLinks("")
