from urllib.request import urlopen
from random import randint


def wordListSum(wordList): #Calcula probabilidad total, sumando todas las ocurrencias (values) del diccionario
    sum = 0
    for word, value in wordList.items():
        sum += value # -> un : {texto : 1, diccionario : 2} tiene probabilidad total 1 + 2 = 3
    return sum


def retrieveRandomWord(wordList): #Recibe el diccionario asociado a la palabra actual -> un : {texto : 1, diccionario : 2}
    randIndex = randint(1, wordListSum(wordList)) #Pasa el diccionario recibido para obtener la probabilidad total y
    #luego generar un valor entero aleatorio entre 1 y la probabilidad total (3)
    for word, value in wordList.items():
        randIndex -= value #Evalua cada valor del diccionario recibido, y lo resta al numero aleatorio generado anteriormente
        if randIndex <= 0: #Cuando el resultado de la resta sea menor o igual que cero, pasa la palabra asociada al valor 
            return word #restado. De esa manera, entre mayor sea el valor, mayor será la probabilidad de que su palabra asociada
            #sea pasada. En el caso de -> un : {texto : 1, diccionario : 2} la palabra "diccionario" tiene mayor probabilidad
            #de convertirse en la nueva palabra actual 


def buildWordDict(text):
    #Remueve newlines, y comillas
    text = text.replace("\n", " ")
    text = text.replace("\"", "")

    #Los signos de puntuaación deben tomarse como palabras
    #para incluirlos dentro de la cadena
    punctuation = [',','.',';',':']
    for symbol in punctuation:
        text = text.replace(symbol, " "+symbol+" ")
    
    words = text.split(" ")
    #Filtro para palabras vacias
    words = [word for word in words if word != ""]
    
    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
            wordDict[words[i-1]] = {} #Crea un diccionario para esta palabra (i-1)
        if words[i] not in wordDict[words[i-1]]:
            """Si la palabra siguiente (i) no está en el diccionario anterior 
            la agrega como un nuevo valor-diccionario dentro del anterior (i-1)"""
            wordDict[words[i-1]][words[i]] = 0 
        """el valor de este diccionario (i) es la cuenta de las veces que
            aparece la palabra (i) después de la palabra anterior (i-1)"""
        wordDict[words[i-1]][words[i]] = wordDict[words[i-1]][words[i]] + 1 # -> wordDict = {un : {texto : 1, diccionario : 2}}

    return wordDict


text = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
wordDict = buildWordDict(text) #Genera el diccionario doble
#Genera una cadena de Markov de 100 palabras
length = 100
chain = ""
currentWord = "I" #Palabra inicial del texto
for i in range(0, length):
    chain += currentWord+" " #Va concatenando cada palabra actual a la anterior
    currentWord = retrieveRandomWord(wordDict[currentWord]) #Envia el diccionario asociado a la palabra 
    #actual -> un : {texto : 1, diccionario : 2}

print(chain)