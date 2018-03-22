import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

#Comunicacion con wikipedia, y parseo de html
html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bsObj = BeautifulSoup(html, "html.parser")
table = bsObj.findAll("table",{"class":"wikitable"})[0] #La tabla buscada es la primera de la pagina
rows = table.findAll("tr") #Parseamos todas las rows de la tabla

#CSV
csvFile = open("comparison.csv", 'wt') #Creacion del archivo
writer = csv.writer(csvFile) #Metodo de modulo CSV para escritura

try:
    for row in rows:
        csvRow = [] #Lista para guardar elementos del row
        for cell in row.findAll(['td', 'th']): #Recorrido de todas las celdas del row
            csvRow.append(cell.get_text())
        writer.writerow(csvRow) #Se escribe el row completo al archivo
finally:
    csvFile.close()