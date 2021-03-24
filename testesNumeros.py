# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 20:57:52 2021

@author: alyss
"""

import re
import pymysql

def deletePalavrasComNumeros(): 
    retorno = -1
    conexao = pymysql.connect(host='localhost', user='root', passwd='@dmin123', db='indice', use_unicode = True, charset = 'utf8mb4')
    cursor = conexao.cursor()
    
    cursor.execute('select idpalavra, palavra from palavras')
    
    rows = cursor.fetchall()
    
    for row in rows:
        idpalavra = row[0]
        palavra = row[1]
        
        if bool(re.search(r'\d', palavra)):
            print("removendo: ", palavra)
            cursor.execute('delete from palavras where idpalavra = %s', idpalavra)
        
    cursor.close()
    conexao.close()
    
    return retorno


deletePalavrasComNumeros()
