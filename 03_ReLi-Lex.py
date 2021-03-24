#Reli-Lex
import nltk
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
    
    cursor.execute('update palavra_polaridade SET polaridade_ReLiLex = %s WHERE idpalavra_polaridade = %s', (polaridade, idPalavra_polaridade))
    idpalavra_polaridade = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpalavra_polaridade
    
def inserePalavraPolaridade(idpalavra, polaridade):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', autocommit='true')
    cursor = conexao.cursor()
    
    cursor.execute('insert into palavra_polaridade(idpalavra, polaridade_ReLiLex) values(%s, %s)', (idpalavra, polaridade))
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
    arquivoWrite = open('arqReliLex.csv', 'w')
    
    for palavra, polaridade in dicionario.items():
        arquivoWrite.write(str(palavra))
        arquivoWrite.write(': ')
        arquivoWrite.write(str(polaridade))
        arquivoWrite.write('\n')
        
    arquivoWrite.close()

def palavras_positivas(arquivos):
    dic_palavra_polaridade = {}
    stemmer = nltk.stem.RSLPStemmer()

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
    stemmer = nltk.stem.RSLPStemmer()

    for arquivo in arquivos:
        for i in arquivo.readlines():
            pos_ponto = i.find(']')
            palavra = (i[1:pos_ponto])
            
            if not eNumero(palavra) and len(palavra) > 1 and palavra not in dic_palavra_polaridade:
                radical_palavra = stemmer.stem(palavra).lower()
                dic_palavra_polaridade[radical_palavra] = -1

    return dic_palavra_polaridade

def gerarDicionarioLexico():
    arquivo1 = 'C:/Users/alyss/Dropbox/UNIPE/2021_1/TCC 2/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/ADJ_Negativos.txt'
    arquivo2 = 'C:/Users/alyss/Dropbox/UNIPE/2021_1/TCC 2/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/ADJ_Positivos.txt'
    arquivo3 = 'C:/Users/alyss/Dropbox/UNIPE/2021_1/TCC 2/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/Subst_Negativos.txt'
    arquivo4 = 'C:/Users/alyss/Dropbox/UNIPE/2021_1/TCC 2/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/Subst_Positivos.txt'
    arquivo5 = 'C:/Users/alyss/Dropbox/UNIPE/2021_1/TCC 2/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/Verbos_Negativos.txt'
    arquivo6 = 'C:/Users/alyss/Dropbox/UNIPE/2021_1/TCC 2/CRAWLER/FERRAMENTAS ANAL SENTIMENTOS/ReLi-Lex/Verbos_Positivos.txt'
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
    
    arquivo_adj_negativos.close()
    arquivo_adj_positivos.close()
    arquivo_subs_negativos.close()
    arquivo_subs_positivos.close()
    arquivo_verb_negativos.close()
    arquivo_verb_positivos.close()

    return dic_palavra_polaridade


#-------------------- MAIN --------------------#
tuplaTabelaPalavras = gerarTuplaPalavrasBD()
dic_palavra_polaridade = gerarDicionarioLexico()
frase = "Estou muito feliz, triste com algumas coisas..."

print("########## Reli-Lex ##########")

for idPalavra, palavra in tuplaTabelaPalavras:
    id_indexada = palavraIndexada(idPalavra)
    isPalavraNoDicionario =  palavra in dic_palavra_polaridade
    
    if id_indexada == -1 and isPalavraNoDicionario:
        inserePalavraPolaridade(idPalavra, dic_palavra_polaridade[palavra])        
    
    elif id_indexada >= 0 and isPalavraNoDicionario:   
        atualizarPolaridade(id_indexada, dic_palavra_polaridade[palavra])

#print(Score_sentimento(frase))
print("RELI-LEX: análise concluída.")
