urlPalavras = ((1, 1), (1, 2), (1, 3), (2, 3), (2, 4), (2, 1), (3, 1), (3, 2), (3, 4))
palavrasPolaridade = ((1, 0, 0, 1, 0, 0), (2, 1, 1, 0, 1, 1), (3, 1, 0, 0, 0, 1), (4, -1, -1, -1, -1, 0))

tuplasScores = ()
dicionario = {}
tuplaSomadora = [0, 0, 0, 0, 0]
idAnterior = 0

#calculando os scores de cada url/notícia
for idUrl, idPalavraUrl in urlPalavras:
    if idAnterior != idUrl:
        tuplaSomadora = [0, 0, 0, 0, 0]
        
    for idPalavraPlvr, polLIWC, polOpLex, polReliLex, polSenti, polWordNet in palavrasPolaridade:
       if idPalavraPlvr == idPalavraUrl:
            print(tuplaSomadora)
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
        
print(tuplasScores)
