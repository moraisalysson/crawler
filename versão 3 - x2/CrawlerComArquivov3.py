from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin #necessário para correção dos links
import re
import nltk
import pymysql

banco_dados = 'index4'

def inserePalavraLocalizacao(idurl, idpalavra, frase, palavra_posicao):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, autocommit='true')
    cursor = conexao.cursor()
    
    cursor.execute('insert into palavra_localizacao(idurl, idpalavra, localizacao_na_frase, frase) values(%s, %s, %s, %s)', (idurl, idpalavra, palavra_posicao, frase))
    idpalavra_localizacao = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpalavra_localizacao


def inserePalavra(palavra):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, autocommit = True, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
    
    cursor.execute('insert into palavras(palavra) values(%s)', palavra)
    idpalavra = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpalavra


def palavraIndexada(palavra): #verifica se palavra já existe no índice
    retorno = -1
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
    
    cursor.execute('select idpalavra from palavras where palavra = %s', palavra)
    
    if cursor.rowcount > 0:
        retorno = cursor.fetchone()[0] #retorna o id da palavra

    cursor.close()
    conexao.close()
    
    return retorno


def inserePagina(url, autor, data):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados, autocommit='true')
    
    dia, mes, ano =  data.split()
    dia = int(dia)
    ano = int(ano)
        
    cursor = conexao.cursor()
    cursor.execute('insert into urls(url, autor, dia, mes, ano) values(%s, %s, %s, %s, %s)', (url, autor, dia, mes, ano))
    idpagina = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpagina


def paginaIndexada(url):
    retorno = -1 #não existe a página
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db=banco_dados)
    
    cursorUrl = conexao.cursor()
    cursorUrl.execute('select idurl from urls where url = %s', url)
    
    if cursorUrl.rowcount > 0:
        #print('Url cadastrada')
        idurl = cursorUrl.fetchone()[0]
        cursorPalavra = conexao.cursor()
        cursorPalavra.execute('select idurl from palavra_localizacao where idurl = %s', idurl)
        
        if cursorPalavra.rowcount > 0:
            #print('Url com palavras')
            retorno = -2 #a página existe e contém palavras
        else:
            #print('Url sem palavras cadastradas')
            retorno = idurl #a página existe, mas sem palavras
            
        cursorPalavra.close()
    #else:
       # print('Url não cadastrada')
    
    cursorUrl.close()
    conexao.close()
    
    return retorno
   
    
def eNumero(valor):
    try:
        float(valor)
    except ValueError:
        return False
    
    return True

def retiraNumeros(texto):
    apenasCaracteres = []
    
    for caractere in texto:
        if not caractere.isdigit():
            apenasCaracteres.append(caractere)
           
    return ''.join(apenasCaracteres)


def separaFrases(texto):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
    
    frases = sent_tokenizer.tokenize(texto)
    
    return frases

def separaPalavras(texto):
    stop = nltk.corpus.stopwords.words('portuguese')

    splitter = re.compile('\W+')
    
    lista_palavras = []
    lista = [p for p in splitter.split(texto) if p != '']
    
    for p in lista:
        p = retiraNumeros(p) 

        if p.lower() not in stop and not eNumero(p):
            if len(p) > 1:                
                
                #lista_palavras.append(p.lower())
                lista_palavras.append(p.lower()) 
    
    return lista_palavras
    

def getTexto(sopa): #vai retornar apenas o texto, sem as tags
     #removendo caracteres de controle
    
    sopa = sopa.replace('\n', ' ').replace('\t', '').replace(
        '$', ' ').replace('%', ' ').replace('#', ' ').replace(
        ';PUBLICIDADE});', '. ').replace('.', '. ')
    
    cleantext = sopa
    cleanr = re.compile("googletag.*?;")
    
    while ("googletag" in cleantext):
        cleantext = re.sub(cleanr, ' ', cleantext)
        
    return cleantext

    
def indexador(url, sopaAutor, sopaData, sopaConteudo):
    indexada = paginaIndexada(url)
    
    textoAutor = getTexto(sopaAutor)[4:103] #retornará apenas o nome
    textoData = getTexto(sopaData)[0:11] #retornará apenas dd/mês/aaaa
    textoConteudo = getTexto(sopaConteudo)
    
    if indexada == -2:
        print("url já indexada")
        return
    elif indexada == -1:
        idnova_pagina = inserePagina(url, textoAutor, textoData)
        print("página gravada com sucesso!")
    elif indexada > 0:
        idnova_pagina = indexada
     
    frases = separaFrases(textoConteudo)
    
    for i in range(len(frases)):
        frase = frases[i]
        
        palavras = separaPalavras(frase)
    
        for j in range(len(palavras)):
            palavra = palavras[j]
            idpalavra = palavraIndexada(palavra)
            
            if idpalavra == -1:
                idpalavra = inserePalavra(palavra)
            
            inserePalavraLocalizacao(idnova_pagina, idpalavra, i, j)
         
    return

def crawl(arquivoHtml):
  
    arquivo = open(arquivoHtml, 'r', encoding='utf8')
    string_arquivo = arquivo.read() 
    arquivo.close()
    
    sopa = BeautifulSoup(string_arquivo, 'lxml') 
    
    #links = sopa.find_all(href=re.compile("consumo/"))
    links = sopa.select('div > span.hl-title.hl-title-2 > a')
    
    for link in links:
        
        if('href' in link.attrs):
            url = urljoin('www.infomoney.com.br/-/-/-/', str(link.get('href'))) #vai juntar o link base com os links relativos               
            
            if url.find("'") != -1:
                print("página fora do padrão #1")
                continue

            url = url.split('#')[0]
            url = url.replace('index.html', '')
            http = urllib3.PoolManager()
            
            try:
                dados_pagina = http.request('GET', url)
            except:
                print('Erro ao abrir a página: ' + url)
                continue #passa para a próxima página
            
            sopaUrl = BeautifulSoup(dados_pagina.data, 'lxml')
            
            try:
                #pegando o texto apenas do Cabeçalho e do Conteúdo de cada artigo
                sopaUrlAutor = sopaUrl.select('div.col.post-header.border-b.my-5.px-0.pb-5 > div > div > div.d-lg-flex.m-0.justify-content-between > div.article-author.d-flex > div.author-info-container > span.author-name')[0].text
                sopaUrlData = sopaUrl.select('div.col.post-header.border-b.my-5.px-0.pb-5 > div > div > div.d-lg-flex.m-0.justify-content-between > div.article-author.d-flex > div.author-info-container > span.article-date > span')[0].text
                sopaUrlConteudo = sopaUrl.select('div.col-md-9.col-lg-8.col-xl-6.m-sm-auto.m-lg-0.article-content')[0].text
            except:
                print("página fora do padrão #2")
                continue #passa para a próxima página
            
            indexador(url, sopaUrlAutor, sopaUrlData, sopaUrlConteudo)
'''
cont = 2
while cont < 400:
    print(cont)
    listaPaginas = 'D:/ALYSSON/WORKSPACE/HTTrack/infomoney/www.infomoney.com.br/economia/page/' + str(cont) + '/index.html'    
    crawl(listaPaginas) #a profundidade vai definir um ponto de parada/limite de dados que você quer extrair
    cont += 1
    
cont = 2
while cont < 400:
    print(cont)
    listaPaginas = 'D:/ALYSSON/WORKSPACE/HTTrack/infomoney/www.infomoney.com.br/mercados/page/' + str(cont) + '/index.html'    
    crawl(listaPaginas) #a profundidade vai definir um ponto de parada/limite de dados que você quer extrair
    cont += 1
'''
cont = 2
while cont < 399:
    print(cont)
    listaPaginas = 'D:/ALYSSON/WORKSPACE/HTTrack/infomoney/www.infomoney.com.br/politica/page/' + str(cont) + '/index.html'    
    crawl(listaPaginas) #a profundidade vai definir um ponto de parada/limite de dados que você quer extrair
    cont += 1

cont = 2
while cont < 400:
    print(cont)
    listaPaginas = 'D:/ALYSSON/WORKSPACE/HTTrack/infomoney/www.infomoney.com.br/ultimas-noticias/page/' + str(cont) + '/index.html'    
    crawl(listaPaginas) #a profundidade vai definir um ponto de parada/limite de dados que você quer extrair
    cont += 1

#26/01/21: erro de index out of range na página 10 / 79 urls salvas    