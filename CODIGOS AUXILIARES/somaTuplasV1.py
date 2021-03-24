def somarPolaridades(idUrl, polLIWC, polOpLex, polReliLex, polSenti, polWordNet):
    if idUrl not in somadorLIWC:
        somadorLIWC[idUrl] = polLIWC
    else:
        somadorLIWC[idUrl] = polLIWC + somadorLIWC[idUrl]
        
    if idUrl not in somadorOpLexicon:
        somadorOpLexicon[idUrl] = polOpLex
    else:
        somadorOpLexicon[idUrl] = polOpLex + somadorOpLexicon[idUrl]
        
    if idUrl not in somadorReLiLex:
        somadorReLiLex[idUrl] = polReliLex
    else:
        somadorReLiLex[idUrl] = polReliLex + somadorReLiLex[idUrl]

    if idUrl not in somadorSentiLex:
        somadorSentiLex[idUrl] = polSenti
    else:
        somadorSentiLex[idUrl] = polSenti + somadorSentiLex[idUrl]
        
    if idUrl not in somadorWordnet:
        somadorWordnet[idUrl] = polWordNet
    else:
        somadorWordnet[idUrl] = polWordNet + somadorWordnet[idUrl]

#urls: 1 = "Ações da Petrobrás subindo", 2 = "Vale sofre queda"
#idPalavraPlvr: 1 = casa, 2 = "bom", 3 = "lucrar", 4 = "mal"
urlPalavras = ((1, 1), (1, 2), (1, 3), (2, 4))
palavrasPolaridade = ((1, 0, 0, 0, 0, 0), (2, 1, 1, 0, 1, 1), (3, 1, 0, 0, 0, 1), (4, -1, -1, -1, -1, 0))

somadorLIWC = {}
somadorOpLexicon = {}
somadorReLiLex = {}
somadorSentiLex = {}
somadorWordnet = {}

for idUrl, idPalavraUrl in urlPalavras:
    for idPalavraPlvr, polLIWC, polOpLex, polReliLex, polSenti, polWordNet in palavrasPolaridade:
        if idPalavraPlvr == idPalavraUrl:
            somarPolaridades(idUrl, polLIWC, polOpLex, polReliLex, polSenti, polWordNet)
            print(somadorLIWC)

print("LIWC: " + str(somadorLIWC))
print("OpLexicon: " + str(somadorOpLexicon))
print("ReLiLex: " + str(somadorReLiLex))
print("SentiLex: " + str(somadorSentiLex))
print("Wordnet: " + str(somadorWordnet))
