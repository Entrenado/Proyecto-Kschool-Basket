#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup
from string import ascii_letters
import sys


lista_url_jugadores = []
for i in range(0,25):
    url = "http://www.bdbasket.com/es/a/j_"+ ascii_letters[i] +".html"
    html = urlopen(url)
    bsObj = BeautifulSoup(html, 'lxml')
    nameList = bsObj.findAll("div", {"class":"pags"})
    if len(nameList) > 0:
        for n in nameList:
            cadena_paginas = n.get_text()
        numero_pag = cadena_paginas[-1]
        for n in range(1,int(numero_pag)+1):
            lista_url_jugadores.append("http://www.bdbasket.com/es/a/j_"+ ascii_letters[i]+ str(n) +".html")
    else:
        lista_url_jugadores.append("http://www.bdbasket.com/es/a/j_"+ ascii_letters[i] +".html")
print 'Leidas las páginas de jugadores'
def leo_jugadores(url):
    try:
        html = urlopen(url)
        print 'pagina leida ', url
        bsObj = BeautifulSoup(html)
    #for sibling in bsObj.find("table",{"id":"taul"}).tr.next_siblings:
    #    print(sibling)
        table = bsObj.find("table", id = "taul")
        rows = table.findAll('tr')
        pais = bsObj.find_all(class_='pais')
        paises = pais[0:len(pais)]
        countries = []
        for n in range(0,len(paises)):
            country = str(paises[n]).split('pais ')[1].split('"')[0]
            countries.append(country)
        data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows]
        contador = 0
        for k in range(1, len(data)):
            if len(data[k][0]) >0: 
                data[k][0] = 'sin pais'
                j = k -1
                if contador == j:
                    contador = j
                else:
                    contador = contador
            else:
                data[k][0] = countries[contador]
                contador = contador + 1
        return data
    except:
        print 'ha ocurrido un error leyendo la página %s revisa si existe'%url
f1 =open('D:\\Master\\ProyectoBasket\\Proyecto-Kschool-Basket\\fichero.csv', 'w') 
        
for j in lista_url_jugadores:
    data = leo_jugadores(j)
 #   print j
 #   print '________________________'

    for n in data:
        #print data
        if len(n) >0:
            listado = n[0].strip() + ','
            for y in range(1,len(n)):
                listado = listado + n[y][0] +','
            #print 'listado =  %s' %listado            
            f1.write(listado[:-1].encode('utf8') + '\n')
f1.close()
