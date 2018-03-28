from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string


def cleanInput(entrada):
    entrada = re.sub('\n+', " ", entrada)
    entrada = re.sub('\[[0-9]*\]', " ", entrada)
    entrada = re.sub('\s+', " ", entrada)
    entrada = bytes(entrada, "UTF-8")
    entrada = entrada.decode("ascii", "ignore")
    cleanInput = []
    entrada = entrada.split(' ')
    for item in entrada:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput


def ngrams(entrada, n):
    entrada = cleanInput(entrada)
    output = []
    for i in range(len(entrada)-n+1):
        output.append(entrada[i:i+n])
    return output


html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html, 'html.parser')
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()
ngrams = ngrams(content, 2)
print(ngrams)
print("2-grams count is: " + str(len(ngrams)))
