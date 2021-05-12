def retiraNumeros(texto):
    apenasCaracteres = []
    
    for caractere in texto:
        if not caractere.isdigit():
            apenasCaracteres.append(caractere)
        
    return ''.join(apenasCaracteres)


p = "12olá23"
print(p)
p = retiraNumeros(p)
print(p)
