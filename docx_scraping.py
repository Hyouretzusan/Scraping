#Para extraer el XML dentro del documento
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO

wordFile = urlopen("http://pythonscraping.com/pages/AWordDocument.docx").read()
wordFile = BytesIO(wordFile)
document = ZipFile(wordFile)
xml_content = document.read('word/document.xml')
print(xml_content.decode('utf-8'))

#Para extraer el texto
from bs4 import BeautifulSoup

wordObj = BeautifulSoup(xml_content.decode('utf-8'), 'html.parser')
#textStrings = wordObj.findAll("w:t")
#for textElem in textStrings:
#    print(textElem.text)

textStrings = wordObj.findAll("w:t")
for textElem in textStrings:
    closeTag = ""
    try:
        style = textElem.parent.previousSibling.find("w:pstyle")
        if style is not None and style["w:val"] == "Title":
            print("<h1>")
            closeTag = "</h1>"
    except AttributeError:
        #No hay tags
        pass
    print(textElem.text)
    print(closeTag)