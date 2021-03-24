#Reli-Lex

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

def palavras_positivas(arquivos):
    dic_palavra_polaridade = {}

    for arquivo in arquivos:
        for i in arquivo.readlines():
            pos_ponto = i.find(']')
            palavra = (i[1:pos_ponto])
            
            if not eNumero(palavra) and len(palavra) > 1 and palavra not in dic_palavra_polaridade:
                radical_palavra = stemmer.stem(palavra).lower()
                dic_palavra_polaridade[radical_palavra] = 1

    return dic_palavra_polaridade

def palavras_negativas(arquivos):
    dic_palavra_polaridade = {}

    for arquivo in arquivos:
        for i in arquivo.readlines():
            pos_ponto = i.find(']')
            palavra = (i[1:pos_ponto])
            
            if not eNumero(palavra) and len(palavra) > 1 and palavra not in dic_palavra_polaridade:
                radical_palavra = stemmer.stem(palavra).lower()
                dic_palavra_polaridade[radical_palavra] = -1

    return dic_palavra_polaridade

print("########## Reli-Lex ##########")

arquivo1 = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/ADJ_Negativos.txt'
arquivo2 = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/ADJ_Positivos.txt'
arquivo3 = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/Subst_Negativos.txt'
arquivo4 = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/Subst_Positivos.txt'
arquivo5 = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/Verbos_Negativos.txt'
arquivo6 = 'C:/Users/alyss/Dropbox/UNIPE/TCC/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/Verbos_Positivos.txt'
stemmer = nltk.stem.RSLPStemmer()

arquivo_adj_negativos = open(arquivo1, 'r', encoding='ANSI')
arquivo_adj_positivos = open(arquivo2, 'r', encoding='ANSI')
arquivo_subs_negativos = open(arquivo3, 'r', encoding='ANSI')
arquivo_subs_positivos = open(arquivo4, 'r', encoding='ANSI')
arquivo_verb_negativos = open(arquivo5, 'r', encoding='ANSI')
arquivo_verb_positivos = open(arquivo6, 'r', encoding='ANSI')

arquivos_positivos = [arquivo_adj_positivos, arquivo_subs_positivos, arquivo_verb_positivos]
arquivos_negativos = [arquivo_adj_negativos, arquivo_subs_negativos, arquivo_verb_negativos]
dic_palavras_positivas = palavras_positivas(arquivos_positivos)
dic_palavras_negativas = palavras_negativas(arquivos_negativos)

dic_palavra_polaridade = {}
dic_palavra_polaridade.update(dic_palavras_positivas)
dic_palavra_polaridade.update(dic_palavras_negativas)

frase = "Estou muito feliz, triste com algumas coisas..."

print(Score_sentimento(frase))

arquivo_adj_negativos.close()
arquivo_adj_positivos.close()
arquivo_subs_negativos.close()
arquivo_subs_positivos.close()
arquivo_verb_negativos.close()
arquivo_verb_positivos.close()