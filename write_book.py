from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
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

pdfFile = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf");
outputString = readPDF(pdfFile)