'''Créditos: @viniljf
Página código: https://medium.com/@viniljf/utilizando-processamento-de-linguagem-natural-para-criar-um-sumariza%C3%A7%C3%A3o-autom%C3%A1tica-de-textos-775cb428c84e
Página usuário: https://medium.com/@viniljf
'''

def short(texto,q=0.3):

    from urllib.request import Request, urlopen
    from nltk.tokenize import word_tokenize
    from nltk.tokenize import sent_tokenize
    sentencas = sent_tokenize(texto)
    palavras = word_tokenize(texto.lower())
    from nltk.corpus import stopwords
    from string import punctuation
    stopwords = set(stopwords.words('portuguese') + list(punctuation))
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]
    from nltk.probability import FreqDist
    frequencia = FreqDist(palavras_sem_stopwords)
    from collections import defaultdict
    sentencas_importantes = defaultdict(int)
    for i, sentenca in enumerate(sentencas):
        for palavra in word_tokenize(sentenca.lower()):
            if palavra in frequencia:
                sentencas_importantes[i] += frequencia[palavra]
    qtd = int(len(sentencas_importantes) * q)
    from heapq import nlargest
    idx_sentencas_importantes = nlargest(qtd, sentencas_importantes, sentencas_importantes.get)
    materia = ''
    for i in sorted(idx_sentencas_importantes):
        materia = materia + ' ' + sentencas[i]

    return materia
    
