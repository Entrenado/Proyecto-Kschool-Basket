# -*- coding: utf-8 -*-
from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import string

url = 'http://www.bdbasket.com/es/index.html'
req = requests.get(url)
html = BeautifulSoup(req.text, "html.parser")

#print html
lista_url_temp = []
lista_a = html.findAll('a')

for j in lista_a:
     link= j.get('href')
     if str(link).find("t/t2") != -1 or str(link).find("t/t1") != -1:
         lista_url_temp.append('http://www.bdbasket.com/es/' +link)
#print lista_url_temp

def lectura_jugadores(url, lista_jugadores):
    try:
        tables = pd.read_html(url, header=0)
        print len(tables[1])
#        print (tables[1][1])
        if len(tables[1]) > 0:  
            lista_jugadores.append(tables[1])
            return lista_jugadores
    except:
        return lista_jugadores
        print 'no se ha podido leer la página %s'%url
jugadores = ''
lista_jugadores = []
for j in range(0,26):
    letra = string.ascii_lowercase[j]
    url = 'http://www.bdbasket.com/es/a/j_' + letra + '.html'
    for i in range(1,3):
        if i == 1:
            url = url
        else:
            url = url[:-6] + str(i) + url[-5:]
        print url
        lista_jugadores= lectura_jugadores(url, lista_jugadores)
        #print lista_jugadores
    jugadores = pd.concat(lista_jugadores, ignore_index=True)
    jugadores = jugadores.drop_duplicates()
print len(jugadores)
