import pymysql


banco_dados = 'index4'
adv_amplificadores = ['bastante', 'demais', 'bem', 'tão'] #'muito', 'mais', 'tanto', 'deveras', 'quanto',
adv_atenuadores = ['pouco'] #'menos',  'quase', , 'apenas'
termos_negacao = ['nada'] #'não', 'nenhum', 'nenhuma', 'nunca', 'jamais', , 'nem'

def gerarTuplaUrlPalavrasBD():
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
        
    cursor.execute('select idurl, idpalavra from palavra_localizacao where idurl = 1423')
    #último idurl = 3.938
    
    cursor.close()
    conexao.close()
        
    return cursor.fetchall()

def gerarTuplaPalavrasPolaridadeBD():
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
        
    cursor.execute('SELECT palavras.idpalavra, palavras.palavra, palavra_polaridade.pol_LIWC_2, pol_OpLexicon_2, pol_ReLiLex_2, pol_Sentilex_2, pol_WordnetBR_2 FROM palavras INNER JOIN palavra_polaridade ON palavras.idpalavra = palavra_polaridade.idpalavra;')
   
    cursor.close()
    conexao.close()
        
    return cursor.fetchall()

def insereScorePolaridadeUrls(idURL, dic):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, autocommit='true')
    cursor = conexao.cursor()
    print(idURL)
    
    cursor.execute('UPDATE noticias_score SET scr_LIWC_2 = %s, scr_OpLexicon_2 = %s, scr_ReLiLex_2 = %s, scr_Sentilex_2 = %s, scr_WordnetBr_2 = %s WHERE id_url = %s;', 
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

#calculando os scores de cada url/notícia
for idUrl, idPalavraUrl in tuplaUrlPalavra:    
    if idAnterior != idUrl:
        tuplaSomadora = [0, 0, 0, 0, 0]
        
    for idPalavraPlvr, palavra, polLIWC, polOpLex, polReliLex, polSenti, polWordNet in tuplaPalavrasPolaridade:
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

for key in dicionario:
    insereScorePolaridadeUrls(key, dicionario)
