#OpLexicon

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


arquivo = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/oplexicon_v3.0/lexico_v3.0.txt'
arquivoWrite = open('arqOpLexicon.csv', 'w')
oplexicon_v3 = open(arquivo, 'r', encoding='utf8')
stemmer = nltk.stem.RSLPStemmer()

print("########## OpLexicion ##########")

dic_palavra_polaridade = {}
for i in oplexicon_v3.readlines():
    posicao_virgula = i.find(',')  
    palavra = (i[:posicao_virgula])
    
    if i.find('0') != -1:
        polaridade_posicao = i.find('0')
    elif i.find('-1') != -1:
        polaridade_posicao = i.find('-1')
    else:
       polaridade_posicao = i.find('1')
   
    polaridade = (i[polaridade_posicao:polaridade_posicao+2]).replace(',','')
    
    if not eNumero(palavra) and len(palavra) > 1 and palavra not in dic_palavra_polaridade:
        radical_palavra = stemmer.stem(palavra).lower()
        dic_palavra_polaridade[radical_palavra] = polaridade

'''
for palavra, polaridade in dic_palavra_polaridade.items():
    arquivoWrite.write(str(palavra))
    arquivoWrite.write(': ')
    arquivoWrite.write(str(polaridade))
    arquivoWrite.write('\n')
'''

frase = "Estou muito feliz, desanimado com algumas coisas..."

print(Score_sentimento(frase))

oplexicon_v3.close()
arquivoWrite.close()