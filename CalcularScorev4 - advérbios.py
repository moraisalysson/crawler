import pymysql


banco_dados = 'index4'
adv_amplificadores = ['bastante', 'demais', 'bem', 'tão'] #'muito', 'mais', 'tanto', 'deveras', 'quanto',
adv_atenuadores = ['pouco'] #'menos',  'quase', , 'apenas'
termos_negacao = ['nada'] #'não', 'nenhum', 'nenhuma', 'nunca', 'jamais', , 'nem'

def gerarTuplaUrlPalavrasBD():
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
        
    cursor.execute('select idurl, idpalavra from palavra_localizacao where idurl = 4058')
    
    cursor.close()
    conexao.close()
        
    return cursor.fetchall()

def gerarTuplaPalavrasPolaridadeBD():
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
        
    cursor.execute('SELECT palavras.idpalavra, palavras.palavra, palavra_polaridade.polaridade_LIWC, polaridade_OpLexicon, polaridade_ReLiLex, polaridade_Sentilex, polaridade_WordnetBR FROM palavras INNER JOIN palavra_polaridade ON palavras.idpalavra = palavra_polaridade.idpalavra;')
   
    cursor.close()
    conexao.close()
        
    return cursor.fetchall()

def insereScorePolaridadeUrls(idURL, dic):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, autocommit='true')
    cursor = conexao.cursor()
    print(idURL)
    
    cursor.execute('UPDATE noticias_score SET scr_LIWC_adv = %s, scr_OpLexicon_adv = %s, scr_ReLiLex_adv = %s, scr_Sentilex_adv = %s, scr_WordnetBr_adv = %s WHERE id_url = %s;', 
                                                   (dic[idURL][0], 
                                                    dic[idURL][1],
                                                    dic[idURL][2],
                                                    dic[idURL][3],
                                                    dic[idURL][4],
                                                    idURL))
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
multiplicador = 1

#calculando os scores de cada url/notícia
for idUrl, idPalavraUrl in tuplaUrlPalavra:    
    if idAnterior != idUrl:
        tuplaSomadora = [0, 0, 0, 0, 0]
        
    for idPalavraPlvr, palavra, polLIWC, polOpLex, polReliLex, polSenti, polWordNet in tuplaPalavrasPolaridade:
        if idPalavraPlvr == idPalavraUrl:
            tuplaSomadora[0] = tuplaSomadora[0] + (polLIWC * multiplicador)
            tuplaSomadora[1] = tuplaSomadora[1] + (polOpLex * multiplicador)
            tuplaSomadora[2] = tuplaSomadora[2] + (polReliLex * multiplicador)
            tuplaSomadora[3] = tuplaSomadora[3] + (polSenti * multiplicador)
            tuplaSomadora[4] = tuplaSomadora[4] + (polWordNet * multiplicador)
            multiplicador = 1
            break

        if palavra in adv_amplificadores:
            multiplicador = 1.6
        elif palavra in adv_atenuadores:
            multiplicador = -1.6     
        
    dicionario[idUrl] = tuplaSomadora
    
    idAnterior = idUrl

tuplasScores = tuple(dicionario.items())

for key in dicionario:
    insereScorePolaridadeUrls(key, dicionario)
