#!/usr/bin/env python
# -*- coding: utf-8 -*-


# cojo el fichero y empiezo a hacer transformaciones y algo de ML
import pandas as pd
import os

def leo_ini(ruta):
    if ruta != "":
        ruta = ruta
    else: 
        ruta = "D:\Master\ProyectoBasket\Proyecto-Kschool-Basket"
    f1 = open(os.path.join(ruta, "ini.txt"))
    lineas=f1.readlines()
    for k in lineas:
        if k.find("ruta") != -1:
            ruta_final = k.split("=")[1]
    return ruta_final
    
ruta = leo_ini("D:\Master\ProyectoBasket\Proyecto-Kschool-Basket")   

df = pd.read_csv(os.path.join(ruta, "temporadas.csv"), sep = ',')
print df.head()
df["porcentaje_jug_esp"] = df["jug_esp"]/df["total_jug"]
df["porcentaje_jug_1"] = df["jug_1"]/df["total_jug"]
df["porcentaje_jug_3"] = df["jug_3"]/df["total_jug"]
df["porcentaje_jug_5"] = df["jug_5"]/df["total_jug"]
df["porcentaje_jug_mas5"] = df["mas5"]/df["total_jug"]
df["total_min_no_esp"] = df["total_min"]-df["total_min_espana"]
df["porcentaje_min_esp"]= df["total_min_espana"]/df["total_min"]
df["porcentaje_min__no_esp"]= df["total_min_no_esp"]/df["total_min"]
df["total_puntos_no_esp"] = df["total_puntos"]-df["total_puntos_espana"]
df["porcentaje_puntos_esp"]= df["total_puntos_espana"]/df["total_puntos"]
df["porcentaje_puntos__no_esp"]= df["total_puntos_no_esp"]/df["total_puntos"]
df["total_val_no_esp"] = df["total_val"]-df["total_val_espana"]
df["porcentaje_val_esp"]= df["total_val_espana"]/df["total_val"]
df["porcentaje_val__no_esp"]= df["total_val_no_esp"]/df["total_val"]
