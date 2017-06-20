#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
#import sys
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
    '''
    ci = convertir a integer
    Se utiliza esta función para extaer el entero  de una resulset con formato [u'numero']
    Se pasa una resultset con formato [u'numero']
    '''
    vuelta = int(string.split(str(dato), "'")[1])
    return vuelta   

def numero_temporadas(web2, temp):
    '''
    Esta función se llama desde la función capturo_datos_equipo 
    
    Cuenta el número de temporadas de todos los jugadores de una plantilla 
    que llevan en la liga acb en la temporada solicitada.
    
    web2 son las direcciones web de los jugadores de la plantilla en formato corto
    temp es la temporada que se está analizando. 
    
    el resultado es 
    jug1 : jugadores que es su primera temporada en ACB
    jug3 : jugadores que llevan entre 2 y 3 temporadas en ACB
    jug5 : jugadores que llevan entre 4 y 5 temporadas en ACB
    mas5 : jugadores que llevan más de 5 temporadas en ACB
    '''
    jug1 = 0
    jug3 = 0
    jug5 = 0
    mas5 = 0
    #print web2,temp
    for n in range(1, len(web2)):
        if len(web2[n]) >0:
            urlj = "http://www.bdbasket.com/es" + string.split(web2[n][0],"..")[1]
           # print urlj
            htmlj = urlopen(urlj)
            soup = BeautifulSoup(htmlj, 'lxml')
            table = soup.find("table", {"class" : "taulabdf traject"})
            rows = table.findAll('tr')            
            web = [[w.get('href') for w in a.findChildren(href=True)] for a in rows]
            for n in range(0, len(web)):
                contador = 0
                if string.find(web[n][0], temp) != -1:
                    #print web[n][0]
                    contador = n+1
            if contador == 1: 
                jug1 = jug1 + 1
            elif contador <= 3:
                jug3 = jug3 + 1  
            elif contador <= 5:
                jug5 = jug5 + 1
            else:
                mas5 = mas5 + 1    
    
    return jug1, jug3, jug5, mas5
      
def capturo_datos_equipo(equipo):
    '''
    En esta función capturo los datos por equipo. 
    Esta función se llama desde la función recorro_temporadas donde voy recorriendo 
    en cada tenporada la clasificación y para cada equipo aplico esta función.
    
    Argumentos:
        equipo: se le pasa la web del equipo para esa temporada. Esta web está formada por
        la raíz: "http://www.bdbasket.com/es" + string.split(web[k][0],"..")[1]
        direccion del equipo para esa temporada con el formato ../t/tNumerodetemporadaIdentificadorequipo.html
        por ejemplo: ../t/t2015-161.html donde Numerodetemporada es 2015-16 e Identificadorequipo es 1 (Barcelona)
        
        La función devuelve los valores para ese equipo de:
        total_min: total de minutos jugados por todos los jugadores del equipo,
        total_val: total de puntos de valoración obtenidos por todos los jugadores del equipo, 
        total_puntos: total de puntos anotados por todos los jugadores del equipo, 
        total_min_espana: total de minutos jugados por los jugadores españoles de un equipo, 
        total_puntos_espana: total de puntos anotados  por los jugadores españoles de un equipo, 
        total_val_espana: total de puntos de valoración obtenidos  por los jugadores españoles de un equipo, 
        jugadores: el número de jugadores que ha tenido un equipo esa temporada, 
        espanoles: el número de jugadores españoles que ha tenido un equipo esa temporada
        jug1, jug3, jug5, mas5: resultaod de la función número de temporadas
        
        
    '''
    urle = equipo
    temp = string.split(urle, "es/t/t")[1][0:7]
    htmle = urlopen(urle)
    soup = BeautifulSoup(htmle, 'lxml')
    table = soup.find("table", id = "taulaplantilla")
    rows = table.findAll('tr')
    paises = [[div.attrs for div in tr.findAll("div")] for tr in rows]
    data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
    web = [[w.get('href') for w in a.findChildren(href=True)] for a in rows]
    jug1,jug3,jug5,mas5 = numero_temporadas(web, temp)
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
    return total_min, total_val, total_puntos, total_min_espana, total_puntos_espana, total_val_espana, jugadores, espanoles,jug1, jug3, jug5, mas5
                
        
          
def recorro_temporadas(lista_temporadas):
    '''
    Función que recorre cada una de las temporadas y llama a las subfunciones para obtener 
    los datos por equipo y por temporada. 
    
    Argumentos: 
        lista_temporada: se le pasan las temporadas que hay en la url "http://www.bdbasket.com/es"
        y que tengan en su nombre t/t que es el indicativo de que es una temporada. 
        
    Resultado: devuelve un Dataframe con los datos a explorar. 
    '''
    filas = []
    for n in lista_temporadas:
        url = n
        print url
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find("table", id = "classific")
        rows = table.findAll('tr')
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
        web = [[w.get('href') for w in a.findChildren(href=True)] for a in rows]
        columnas = ["temporada", "equipo", "puesto", "PJ","PG","PP","PF","PC", "total_min", "total_val", "total_puntos", "total_min_espana", "total_puntos_espana", "total_val_espana", "total_jug", "jug_esp", "jug1", "jug3", "jug5", "mas5"]
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
            #print capturo_datos_equipo("http://www.bdbasket.com/es" + string.split(web[k][0],"..")[1])
            total_min, total_val, total_puntos, total_min_espana, total_puntos_espana, total_val_espana, jugadores, espanoles, jug1, jug3, jug5, mas5= capturo_datos_equipo("http://www.bdbasket.com/es" + string.split(web[k][0],"..")[1])
            filas.append([temp,equipo,puesto,PJ,PG,PP,PF,PC,total_min, total_val, total_puntos, total_min_espana, total_puntos_espana, total_val_espana, jugadores, espanoles, jug1,jug3, jug5, mas5])
    temporada = pd.DataFrame(filas,columns= columnas)
    return temporada
        
        
listado =recorro_temporadas(lista_temporadas)
#print listado
listado.to_csv("D:\\Master\\ProyectoBasket\\Proyecto-Kschool-Basket\\temporadas_prueba.csv", index=False)
