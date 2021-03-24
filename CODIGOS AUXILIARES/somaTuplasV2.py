#urls: 1 = "Ações da Petrobrás subindo", 2 = "Vale sofre queda"
#idPalavraPlvr: 1 = casa, 2 = "bom", 3 = "lucrar", 4 = "mal"
urlPalavras = ((1, 1), (1, 2), (1, 3), (2, 3), (2, 4), (2, 1), (3, 1), (3, 2), (3, 4))
palavrasPolaridade = ((1, 0, 0, 1, 0, 0), (2, 1, 1, 0, 1, 1), (3, 1, 0, 0, 0, 1), (4, -1, -1, -1, -1, 0))

tuplasFinais = []
dicionario = {}
tuplaSomadora = [0, 0, 0, 0, 0]
idAnterior = 0

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
    print(dicionario)

print(dicionario)
