#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup
from string import ascii_letters
import pandas as pd
import re
import sys
import string

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
    filas = []
    for n in lista_temporadas:
        url = n
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find("table", id = "classific")
        rows = table.findAll('tr')
        for a in soup.find_all(href=True):
            if a.get('href').find('t/t') != -1 and  re.compile('[0-9]').search( a.get('href')):
                url_equipo = a.get('href')
                print url_equipo
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
        columnas = ["temporada", "equipo", "puesto", "PJ","PG","PP","PF","PC"]
        for k in range(1,len(data)):
            temp = str(n[-10:-5])
            equipo = string.split(str(data[k][3]), "'")[1]
            puesto = int(string.split(str(data[k][1]), "'")[1])
            PJ = int(string.split(str(data[k][4]), "'")[1])
            PG = int(string.split(str(data[k][5]), "'")[1])
            PP = int(string.split(str(data[k][6]), "'")[1])
            PF = int(string.split(str(data[k][7]), "'")[1])
            PC = int(string.split(str(data[k][8]), "'")[1])
            filas.append([temp,equipo,puesto,PJ,PG,PP,PF,PC])
    temporada = pd.DataFrame(filas,columns= columnas)
    return temporada
        #sys.exit()
        
        
listado =recorro_temporadas(lista_temporadas)
listado.to_csv("C:\\Users\\Z22P1P0Z\\Google Drive\\master\\Github\\Proyecto-Kschool-Basket\\temporadas.csv", index=False)
