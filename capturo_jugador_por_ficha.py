#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import urlopen
from bs4 import BeautifulSoup
import requests
import sys

def extraigo_datos_jugador(req):
    ''' 
    Extrae los datos de los jugadores 
    atributos : req es la url de la página del jugador
                No se permite redirecciones para comprobar que la página existe
    req se construye a través de la url http://www.bdbasket.com/es/j/j + contador + .html
    tiene un límite de 2555 jugadores porque la base de datos es menor
    se ha puesto límite puesto que no se ha encontrado en la web dónde indica 
    el número de jugadores y hay menos de 2555. 
    '''
    html = urlopen(url)
    bsObj = BeautifulSoup(html)
   # table = bsObj.find("table", { "class" : "tabledades" })
    Nombre = bsObj.find("td", text="Nombre:").find_next_sibling("td").text
    FNacimiento = bsObj.find("td", text="Fecha de nacimiento:").find_next_sibling("td").text
    LNacimiento = bsObj.find("td", text="Lugar de nacimiento:").find_next_sibling("td").text
    Pais = bsObj.find("td", text="País:").find_next_sibling("td").text
    Altura = bsObj.find("td", text="Altura:").find_next_sibling("td").text
    Puesto = bsObj.find("td", text="Demarcación:").find_next_sibling("td").text
    datos_jugador=[Nombre,FNacimiento, LNacimiento, Pais, Altura, Puesto]    
    return datos_jugador


contador = 0
while 1:
    contador = contador +1 
    url = "http://www.bdbasket.com/es/j/j%s.html"%str(contador)
    # Realizamos la petición a la web
    req = requests.get(url,allow_redirects=False)
    # No se permite redirecciones puesto que en la página si encontraba números similares 
    # te redirigía ej: 2555 te redirigia a 555
    Status_code= req.status_code
    if Status_code == 200:
        # si la página existe extraigo los datos
        datos_jugador = extraigo_datos_jugador(req)
    print datos_jugador[0]
    if contador > 2555:break
