#Sentilex
#Não foram extraídos os radicais das palavras

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
    
print("########## Sentilex ##########")

arquivo = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/SentiLex-PT02/SentiLex-lem-PT02.txt'
sentilexpt = open(arquivo, 'r', encoding='utf8')
dic_palavra_polaridade = {}
stemmer = nltk.stem.RSLPStemmer()

for i in sentilexpt.readlines():
    pos_ponto = i.find('.')
    palavra = (i[:pos_ponto])
    pol_pos = i.find('POL')
    polaridade = (i[pol_pos+7:pol_pos+9]).replace(';','')
    
    if not eNumero(palavra) and len(palavra) > 1 and palavra not in dic_palavra_polaridade:
        radical_palavra = stemmer.stem(palavra).lower()
        dic_palavra_polaridade[radical_palavra] = polaridade

frase = "Estou muito feliz, desanimado com algumas coisas..."


print(Score_sentimento(frase))
