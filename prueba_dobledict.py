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
        wordDict[words[i-1]][words[i]] = wordDict[words[i-1]][words[i]] + 1 


    for result in wordDict:
        print(result, wordDict[result])

text = """Esto es un texto de
prueba. Quiero ver, analizar, estudiar; la
distribucion de un diccionario doble. Le agrego tantas
palabras de prueba como puedo. Quiero ver, como las agrupa.
Esto es repetitivo a proposito. Quiero un diccionario doble con
muchas coincidencias, tantas palabras como puedo para ver como las
agrupa"""

buildWordDict(text)