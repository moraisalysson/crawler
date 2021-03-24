#LIWC
import nltk
import re
   
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


arquivo = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/LIWC-PT.txt'
liwc_pt = open(arquivo, 'r', encoding='utf8')
arquivoWrite = open('arqLIWC.csv', 'w')
dic_palavra_polaridade = {}
stemmer = nltk.stem.RSLPStemmer()

print("Léxico: LIWC")

for i in liwc_pt.readlines():
    if i.find('126') != -1: #positivas
        posicao = i.find('1')
        palavra = (i[0:posicao]).replace('\n', '').replace('\t', '').replace('*', '')
        palavra = re.sub('[0-9]', '', palavra) #retira os números
        
        if not eNumero(palavra) and len(palavra) > 1 and palavra not in dic_palavra_polaridade:
            radical_palavra = stemmer.stem(palavra).lower()
            dic_palavra_polaridade[radical_palavra] = 1        
        
    elif i.find('127') != -1: #negativas
        posicao = i.find('1')
        palavra = (i[0:posicao]).replace('\n', '').replace('\t', '').replace('*', '')
        palavra = re.sub('[0-9]', '', palavra) #retira os números
        
        if not eNumero(palavra) and len(palavra) > 1 and palavra not in dic_palavra_polaridade:
            radical_palavra = stemmer.stem(palavra).lower()
            dic_palavra_polaridade[radical_palavra] = -1


for palavra, polaridade in dic_palavra_polaridade.items():
    arquivoWrite.write(str(palavra))
    arquivoWrite.write(': ')
    arquivoWrite.write(str(polaridade))
    arquivoWrite.write('\n')

    
frase = "Estou muito feliz, animado com algumas coisas..."

print(Score_sentimento(frase))

liwc_pt.close()
arquivoWrite.close()