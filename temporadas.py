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
def  capturo_equipos():
    equipo_web={}
    urle = "http://www.bdbasket.com/e/e.html"
    htmle = urlopen(urle)
    soup = BeautifulSoup(htmle, 'lxml')
    nameList = soup.findAll("div", {"class":"eq2b"})
    nombre = [a.findChildren(text=True) for a in nameList]
    web = [[w.get('href') for w in a.findChildren(href=True)] for a in nameList]
    for n in range(0,len(nombre)-1):
        equipo_web[str(nombre[n]).split("'")[1]] = web[n][0].split("e")[1][0:2].split(".")[0]
    return equipo_web

equipo_web = capturo_equipos()
    
def recorro_temporadas(lista_temporadas, equipo_web):
    filas = []
    for n in lista_temporadas:
        url = n
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find("table", id = "classific")
        rows = table.findAll('tr')
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
        
        
listado =recorro_temporadas(lista_temporadas,equipo_web)
listado.to_csv("C:\\Users\\Z22P1P0Z\\Google Drive\\master\\Github\\Proyecto-Kschool-Basket\\temporadas.csv", index=False)
