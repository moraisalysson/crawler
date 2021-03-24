import pymysql


def gerarTuplaUrlPalavrasBD():
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
        
    cursor.execute('select idurl, idpalavra from palavra_localizacao where idurl <= 2')
    #último idurl = 21.530
    
    cursor.close()
    conexao.close()
        
    return cursor.fetchall()

def gerarTuplaPalavrasPolaridadeBD():
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
        
    cursor.execute('select idpalavra, polaridade_LIWC, polaridade_OpLexicon, polaridade_ReLiLex, polaridade_Sentilex, polaridade_WordnetBR from palavra_polaridade')
   
    cursor.close()
    conexao.close()
        
    return cursor.fetchall()

def insereScorePolaridadeUrls(idurl, dicionario):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', autocommit='true')
    cursor = conexao.cursor()
    
    cursor.execute('insert into noticias_score(id_url, score_LIWC, score_OpLexicon, score_ReLiLex, score_Sentilex, score_WordnetBr, polaridade_LIWC, polaridade_OpLexicon, polaridade_ReLiLex, polaridade_Sentilex, polaridade_WordnetBr) values(%d, %d, %d, %d, %d, %d, %s, %s, %s, %s, %s)', 
                                                   (idurl, 
                                                    dicionario[idurl][0], 
                                                    dicionario[idurl][1],
                                                    dicionario[idurl][2],
                                                    dicionario[idurl][3],
                                                    dicionario[idurl][4],
                                                    dicionario[idurl][5],
                                                    dicionario[idurl][6],
                                                    dicionario[idurl][7],
                                                    dicionario[idurl][8],
                                                    dicionario[idurl][9]
                                                    ))
    idpalavra_polaridade = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpalavra_polaridade

tuplasScores = ()
dicionario = {}
tuplaSomadora = [0, 0, 0, 0, 0]
idAnterior = 0
tuplaUrlPalavra = gerarTuplaUrlPalavrasBD()
tuplaPalavrasPolaridade = gerarTuplaPalavrasPolaridadeBD()

#calculando os scores de cada url/notícia
for idUrl, idPalavraUrl in tuplaUrlPalavra:
    print(idUrl)
    
    if idAnterior != idUrl:
        tuplaSomadora = [0, 0, 0, 0, 0]
        
    for idPalavraPlvr, polLIWC, polOpLex, polReliLex, polSenti, polWordNet in tuplaPalavrasPolaridade:
        if idPalavraPlvr == idPalavraUrl:
            tuplaSomadora[0] = tuplaSomadora[0] + polLIWC
            tuplaSomadora[1] = tuplaSomadora[1] + polOpLex
            tuplaSomadora[2] = tuplaSomadora[2] + polReliLex
            tuplaSomadora[3] = tuplaSomadora[3] + polSenti
            tuplaSomadora[4] = tuplaSomadora[4] + polWordNet
            break

    dicionario[idUrl] = tuplaSomadora
    
    idAnterior = idUrl

tuplasScores = tuple(dicionario.items())

#Adicionar a Polaridade à tupla
for tupla in tuplasScores:
    i = 0
    while i < 5:
        if tupla[1][i] > 0:
            tupla[1].append("Positivo")
        elif tupla[1][i] == 0:
            tupla[1].append("Neutro")
        else:
            tupla[1].append("Negativo")
        i += 1

#print(tuplasScores)

for key in dicionario:
    insereScorePolaridadeUrls(key, dicionario)
