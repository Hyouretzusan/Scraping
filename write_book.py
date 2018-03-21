from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf #Funciones para procesamiento
from pdfminer.converter import TextConverter #Convertidor a texto
from pdfminer.layout import LAParams #Parametros para procesar imagen/texto
from io import StringIO #Llamado a modulo String para el convertidor
from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdfFile)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    fout = open("warandpeace1.txt", 'wt')
    size = len(content)
    offset = 0
    chunk = 300
    while True:
        if offset > size:
            break
        retrieve = fout.write(content[offset:offset+chunk])
        print(retrieve)
        offset += chunk
    print("DONE!")

    fout.close()

pdfFile = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")
outputString = readPDF(pdfFile)