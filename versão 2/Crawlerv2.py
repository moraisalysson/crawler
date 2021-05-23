from bs4 import BeautifulSoup
import urllib3
from urllib.parse import urljoin #necessário para correção dos links
import re
import nltk
import pymysql
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def inserePalavraLocalizacao(idurl, idpalavra, localizacao):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', autocommit='true')
    cursor = conexao.cursor()
    
    cursor.execute('insert into palavra_localizacao(idurl, idpalavra, localizacao) values(%s, %s, %s)', (idurl, idpalavra, localizacao))
    idpalavra_localizacao = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpalavra_localizacao


def inserePalavra(palavra):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', autocommit = True, use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
    
    cursor.execute('insert into palavras(palavra) values(%s)', palavra)
    idpalavra = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpalavra


def palavraIndexada(palavra): #verifica se palavra já existe no índice
    retorno = -1
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
    
    cursor.execute('select idpalavra from palavras where palavra = %s', palavra)
    
    if cursor.rowcount > 0:
        retorno = cursor.fetchone()[0] #retorna o id da palavra

    cursor.close()
    conexao.close()
    
    return retorno


def inserePagina(url):
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', autocommit='true')
    
    cursor = conexao.cursor()
    cursor.execute('insert into urls(url) values(%s)', url)
    idpagina = cursor.lastrowid

    cursor.close()
    conexao.close()
    
    return idpagina


def paginaIndexada(url):
    retorno = -1 #não existe a página
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice')
    
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
    

def separaPalavras(texto):
    stop = nltk.corpus.stopwords.words('portuguese')

    splitter = re.compile('\W+')
    stemmer = nltk.stem.RSLPStemmer() #extrator radicais das palavras
    
    lista_palavras = []
    lista = [p for p in splitter.split(texto) if p != '']
    
    for p in lista:
        if p.lower() not in stop:
            if len(p) > 1:
                lista_palavras.append(stemmer.stem(p).lower())
    
    return lista_palavras
    

#sopa contém todos os dados da página
    
def getTexto(sopa): #vai retornar apenas o texto, sem as tags
    for tags in sopa(['script', 'style']):
        tags.decompose()
    
    return ' '.join(sopa.stripped_strings)


def indexador(url, sopa):
    indexada = paginaIndexada(url)
    
    if indexada == -2:
        print("url já indexada")
        return
    elif indexada == -1:
        idnova_pagina = inserePagina(url)
    elif indexada > 0:
        idnova_pagina = indexada
        
    print("Indexando " + url)
    
    texto = getTexto(sopa)
    palavras = separaPalavras(texto)
    
    for i in range(len(palavras)):
        palavra = palavras[i]
        idpalavra = palavraIndexada(palavra)

        if idpalavra == -1:
            idpalavra = inserePalavra(palavra)
        
        inserePalavraLocalizacao(url, idpalavra, i)
    
    return

'''
def clicarCarregarMais(pagina):
    driver = webdriver.Chrome()

    driver.get(pagina)

    while True:
        
        time.sleep(10)
        
        html = driver.find_element_by_xpath('//*[@id="infinite-handle"]/span/button')
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)
        html.send_keys(Keys.PAGE_DOWN)
                
        #btn_more = driver.find_element(By.XPATH , '//*[@id="infinite-handle"]/span/button')
        btn_more = driver.find_element_by_xpath('//*[@id="infinite-handle"]/span/button')
        #WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="infinite-handle"]/span/button')))
        #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="infinite-handle"]/span/button'))).click()
        
        driver.execute_script("arguments[0].click();", btn_more)
        #btn_more.click()
'''
def crawl(paginas, profundidade):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #desativando os warnings 
  
    for i in range(profundidade):
        novas_paginas = set() #ñ permite valores repetidos
                
        for pagina in paginas:  
            http = urllib3.PoolManager()
            
            try:
                dados_pagina = http.request('GET', pagina)
            except:
                print('Erro ao abrir a página: ' + pagina)
                continue #passa para a próxima página
            
            sopa = BeautifulSoup(dados_pagina.data, 'lxml') 
#reativar   indexador(pagina, sopa)
#reativar            links = sopa.find_all(href=re.compile("consumo/"))
            links = sopa.select('div.col-12.col-lg-4.img-container a')
            
            contador = 1 #necessário para verificar se todos os <a> têm 'href'    
            for link in links:
                #print('\n')
                #print(str(link.contents) + " - " + str(link.get('href')))
                #print(link.attrs)
                #print('\n')
                
                if('href' in link.attrs):
                    url = urljoin(pagina, str(link.get('href'))) #vai juntar o link base com os links relativos
                    
                    #if url != link.get('href'):
                        #print(url)
                        #print(link.get('href'))
                       
                    
                    if url.find("'") != -1:
                        continue
                    
                    #print(url)
                    url = url.split('#')[0]
                    print(url)
                    print('\n')
                    
                    
                    if url[0:4] == 'http':
                        novas_paginas.add(url)
                    
                    contador = contador + 1
            
            paginas = novas_paginas
            print(contador)

listaPaginas = ['https://www.infomoney.com.br/ultimas-noticias/']
#clicarCarregarMais('https://www.infomoney.com.br/ultimas-noticias/')
crawl(listaPaginas, 1) #a profundidade vai definir um ponto de parada/limite de dados que você quer extrair