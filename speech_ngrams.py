from urllib.request import urlopen
import re
import string
import operator


def cleanInput(entrada):
    entrada = re.sub('\n+', " ", entrada).lower()
    entrada = re.sub('\[[0-9]*\]', "", entrada)
    entrada = re.sub(' +', " ", entrada)
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
    output = {}
    for i in range(len(entrada)-n+1):
        ngramTemp = " ".join(entrada[i:i+n])
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output


def isCommon(sortedNgrams):
    worthy_ngrams = list()
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have", "it",
    "i", "that", "for", "you", "he", "with", "on", "do", "say", "this",
    "they", "is", "an", "at", "but","we", "his", "from", "that", "not",
    "by", "she", "or", "as", "what", "go", "their","can", "who", "get",
    "if", "would", "her", "all", "my", "make", "about", "know", "will",
    "as", "up", "one", "time", "has", "been", "there", "year", "so",
    "think", "when", "which", "them", "some", "me", "people", "take",
    "out", "into", "just", "see", "him", "your", "come", "could", "now",
    "than", "like", "other", "how", "then", "its", "our", "two", "more",
    "these", "want", "way", "look", "first", "also", "new", "because",
    "day", "more", "use", "no", "man", "find", "here", "thing", "give",
    "many", "well"]

    for ngram in sortedNgrams:
        contador_comun = 0
        words = ngram[0].split()
        for word in words:
            if word in commonWords:
                contador_comun += 1
        if contador_comun == 0 and ngram[1] > 2:
            worthy_ngrams.append(ngram)
    print(worthy_ngrams)


content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
ngrams = ngrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1))
isCommon(sortedNGrams)