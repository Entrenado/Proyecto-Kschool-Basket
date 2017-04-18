#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup
from string import ascii_letters
import re
import sys

pagina = "http://www.bdbasket.com/es"
html = urlopen(pagina)
soup = BeautifulSoup(html, 'lxml')
#soup = BeautifulSoup(bsObj)
lista_temporadas = []
lista_equipos = []

for a in soup.find_all(href=True):
    #print re.compile('[0-9]').search( a.get('href'))
    if a.get('href').find('t/t') != -1 and  re.compile('[0-9]').search( a.get('href')):
        lista_temporadas.append("http://www.bdbasket.com/es/" + a.get('href'))
    if a.get('href').find('e/e') != -1 and  re.compile('[0-9]').search( a.get('href')):
        lista_equipos.append("http://www.bdbasket.com/es/" +a.get('href'))
#print lista_temporadas
#print lista_equipos

def recorro_temporadas(lista_temporadas):
    temporada = {}
    lista = []
    for n in lista_temporadas:
        url = n
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find("table", id = "classific")
        rows = table.findAll('a')
        contador = 1
        for k in rows:
            equipo = k.getText()
            posicion = lista.append[(contador, n[-10:-5])]
            temporada[equipo]= posicion
            contador = contador +1
        print temporada
    return temporada
        #sys.exit()
        
        
listado =recorro_temporadas(lista_temporadas)
