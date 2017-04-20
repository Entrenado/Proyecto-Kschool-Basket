#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup
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
    nameList = soup.findAll("div", {"class":"eq2B"})
    nombre = [a.findChildren(text=True) for a in nameList]
    web = [[w.get('href') for w in a.findChildren(href=True)] for a in nameList]
    for n in range(0,len(nombre)-1):
        equipo_web[str(nombre[n]).split("'")[1]] = web[n][0].split("e")[1][0:2].split(".")[0]
    #print equipo_web
    return equipo_web

equipo_web = capturo_equipos()

def ci(dato):
    vuelta = int(string.split(str(dato), "'")[1])
    return vuelta   

  
def capturo_datos_equipo(equipo):
    urle = equipo
    htmle = urlopen(urle)
    soup = BeautifulSoup(htmle, 'lxml')
    table = soup.find("table", id = "taulaplantilla")
    rows = table.findAll('tr')
    paises = [[div.attrs for div in tr.findAll("div")] for tr in rows]
    data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
    web = [[w.get('href') for w in a.findChildren(href=True)] for a in rows] 
    total_puntos_espana = 0
    total_min_espana = 0
    total_val_espana = 0
    total_puntos = 0
    total_min = 0
    total_val = 0
    espanoles = 0
    jugadores = 0
    for k in range(1,len(data)):
        if len(data[k]) > 10:
            try:
                pais = paises[k][0]["class"][1]
            except:
                pais = "desconocido"
            puntos = ci(data[k][10])
            minutos = ci(data[k][9])
            valoracion = ci(data[k][21])
            total_min = total_min + minutos
            total_val= total_val + valoracion
            total_puntos = total_puntos + puntos
            jugadores = jugadores + 1
            if pais == "espanya":
                total_min_espana = total_min_espana + minutos
                total_val_espana= total_val_espana + valoracion
                total_puntos_espana = total_puntos_espana + puntos
                espanoles = espanoles +1
    return total_min, total_val, total_puntos, total_min_espana, total_puntos_espana, total_val_espana, jugadores, espanoles
                
        
          
def recorro_temporadas(lista_temporadas):
    filas = []
    for n in lista_temporadas:
        url = n
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find("table", id = "classific")
        rows = table.findAll('tr')
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
        web = [[w.get('href') for w in a.findChildren(href=True)] for a in rows]
        columnas = ["temporada", "equipo", "puesto", "PJ","PG","PP","PF","PC", "total_min", "total_val", "total_puntos", "total_min_espana", "total_puntos_espana", "total_val_espana", "total_jug", "jug_esp"]
        for k in range(1,len(data)):
            temp = str(n[-10:-5])
            equipo = string.split(str(data[k][3]), "'")[1]
            puesto = int(string.split(str(data[k][1]), "'")[1])
            PJ = int(string.split(str(data[k][4]), "'")[1])
            PG = int(string.split(str(data[k][5]), "'")[1])
            PP = int(string.split(str(data[k][6]), "'")[1])
            PF = int(string.split(str(data[k][7]), "'")[1])
            PC = int(string.split(str(data[k][8]), "'")[1])
            #print "http://www.bdbasket.com/es" + string.split(web[k][0],"..")[1]
            total_min, total_val, total_puntos, total_min_espana, total_puntos_espana, total_val_espana, jugadores, espanoles= capturo_datos_equipo("http://www.bdbasket.com/es" + string.split(web[k][0],"..")[1])
            filas.append([temp,equipo,puesto,PJ,PG,PP,PF,PC,total_min, total_val, total_puntos, total_min_espana, total_puntos_espana, total_val_espana])
    temporada = pd.DataFrame(filas,columns= columnas)
    return temporada
        
        
listado =recorro_temporadas(lista_temporadas)
print listado
listado.to_csv("D:\\Master\\ProyectoBasket\\Proyecto-Kschool-Basket\\temporadas.csv", index=False)
