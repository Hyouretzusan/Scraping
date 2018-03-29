from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import OrderedDict
vow = ("a", "e", "i", "o", "u", "A", "E", "I", "O", "U")

def cleanInput(entrada):
    entrada = re.sub('\n+', " ", entrada) #Elimina endlines
    entrada = re.sub('\[[0-9-]*\]', " ", entrada) #Elimina [2]
    #entrada = re.sub('[0-9-/]', " ", entrada) #DEBB
    entrada = re.sub('\s+', " ", entrada) #Elimina espacios repetidos
    #entrada = entrada.translate(entrada.maketrans('', '', string.punctuation)) #DEBB
    entrada = bytes(entrada, "UTF-8")
    entrada = entrada.decode("ascii", "ignore")
    cleanInput = []
    entrada = entrada.split(' ')
    for item in entrada:
        item = item.strip(string.punctuation)
        #print("Item:", item)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput


def ngrams(entrada, n):
    entrada = cleanInput(entrada)
    output = []
    for i in range(len(entrada)-n+1):
        output.append(entrada[i:i+n])
    return output
    #print(output) #DEBB


html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html, 'html.parser')
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()

bigrams = ngrams(content, 2)
bigrams = OrderedDict(sorted(bigrams, key=lambda t: t[1], reverse=True)) #Buscar maneras de que los bigrams sean keys, y los values sean el conteo
print(bigrams)
#print("2-grams count is: " + str(len(ngrams)))