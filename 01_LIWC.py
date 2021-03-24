#LIWC
import nltk
import re
import pymysql

def palavraIndexada(idpalavra): #verifica se palavra já existe no índice
    retorno = -1
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
    
    cursor.execute('select idpalavra_polaridade from palavra_polaridade where idpalavra = %s', idpalavra)
    
    if cursor.rowcount > 0:
        retorno = cursor.fetchone()[0] #retorna o id da palavra

    cursor.close()
    conexao.close()
    
    return retorno

def atualizarPolaridade(idPalavra_polaridade, polaridade):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', autocommit='true')
    cursor = conexao.cursor()
    
    cursor.execute('update palavra_polaridade SET polaridade_LIWC = %s WHERE idpalavra_polaridade = %s', (polaridade, idPalavra_polaridade))
    idpalavra_polaridade = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpalavra_polaridade
    
def inserePalavraPolaridade(idpalavra, polaridade):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', autocommit='true')
    cursor = conexao.cursor()
    
    cursor.execute('insert into palavra_polaridade(idpalavra, polaridade_LIWC) values(%s, %s)', (idpalavra, polaridade))
    idpalavra_polaridade = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpalavra_polaridade

def eNumero(valor):
    try:
        float(valor)
    except ValueError:
        return False
    
    return True
    
def gerarTuplaPalavrasBD():
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
        
    cursor.execute('select * from palavras')
   
    cursor.close()
    conexao.close()
        
    return cursor.fetchall()

def gerarTuplaPalavrasPolaridadeBD():
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
        
    cursor.execute('select * from palavra_polaridade')
   
    cursor.close()
    conexao.close()
        
    return cursor.fetchall()

def Score_sentimento(frase):
    frase = frase.lower()
    l_sentimento = []
    stemmer = nltk.stem.RSLPStemmer()
    
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

def gerarArquivoDoLexico(dicionario):
    arquivoWrite = open('arqLIWC.csv', 'w')
    
    for palavra, polaridade in dicionario.items():
        arquivoWrite.write(str(palavra))
        arquivoWrite.write(': ')
        arquivoWrite.write(str(polaridade))
        arquivoWrite.write('\n')
        
    arquivoWrite.close()

def gerarDicionarioLexico():
    arquivo = 'C:/Users/alyss/Dropbox/UNIPE/2021_1/TCC 2/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/LIWC-PT.txt'
    liwc_pt = open(arquivo, 'r', encoding='utf8')
    dic_palavra_polaridade = {}
    stemmer = nltk.stem.RSLPStemmer()
    
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

    liwc_pt.close()
    
    return dic_palavra_polaridade


#-------------------- MAIN --------------------#
tuplaTabelaPalavras = gerarTuplaPalavrasBD()
dic_palavra_polaridade = gerarDicionarioLexico()
frase = "Estou muito feliz, animado com algumas coisas..."

print("########## LIWC ##########")
    
for idPalavra, palavra in tuplaTabelaPalavras:
    id_indexada = palavraIndexada(idPalavra)
    isPalavraNoDicionario =  palavra in dic_palavra_polaridade
    
    if id_indexada == -1 and isPalavraNoDicionario:
        inserePalavraPolaridade(idPalavra, dic_palavra_polaridade[palavra])        
    
    elif id_indexada >= 0 and isPalavraNoDicionario:   
        atualizarPolaridade(id_indexada, dic_palavra_polaridade[palavra])

#print(Score_sentimento(frase))
print("LIWC: análise concluída.")

