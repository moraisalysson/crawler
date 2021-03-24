#WordnetAffectBr
import nltk

def eNumero(valor):
    try:
        float(valor)
    except ValueError:
        return False
    
    return True

def Score_sentimento(frase):
    frase = frase.lower()
    l_sentimento = []

    stop = nltk.corpus.stopwords.words('portuguese')

    for p in frase.split():
       if len(p) > 1 and p not in stop: 
            p = p.replace(',','').replace('.', '')
            p = stemmer.stem(p).lower()
            l_sentimento.append(int(dic_palavra_polaridade.get(p, 0)))
            print("%s: %d" %(p, int(dic_palavra_polaridade.get(p, 0))))

    score = sum(l_sentimento)

    if score > 0:
        return "Positivo, Score:{}".format(score)
    elif score == 0:
        return "Neutro, Score:{}".format(score) 
    else:
        return "Negativo, Score:{}".format(score)
    

arquivo = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/wordnetaffectbr_valencia.csv'
sentilexpt = open(arquivo, 'r')
dic_palavra_polaridade = {}
stemmer = nltk.stem.RSLPStemmer()

print("########## WordnetAffectBr ##########")

for i in sentilexpt.readlines():
    pos_ponto = i.find(';')
    palavra = (i[:pos_ponto])
    polaridade = (i[pos_ponto+1:]).replace('\n','')
    if polaridade == '-':
        polaridade = -1
    elif polaridade == '+':
        polaridade = 1
    else:
        polaridade = 0
        
    if not eNumero(palavra) and len(palavra) > 1 and palavra not in dic_palavra_polaridade:
        radical_palavra = stemmer.stem(palavra).lower()
        dic_palavra_polaridade[radical_palavra] = polaridade


frase = "Estou muito feliz, desanimado com algumas coisas..."

print(Score_sentimento(frase))
