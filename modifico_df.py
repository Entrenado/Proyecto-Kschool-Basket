#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Read the web scrapped file, transform same values and start to apply Machine Learning
import pandas as pd
import os
import statsmodels.formula.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, svm
from sklearn.metrics import accuracy_score
#%matplotlib inline


def leo_ini():
    import os
    script_dir = os.path.dirname(__file__)
    f1 = open(os.path.join(script_dir,"ini.txt"), 'r')
    lineas=f1.readlines()
    for k in lineas:
        if k.find("ruta") != -1:
            ruta_final = k.split("=")[1]
    return ruta_final
    
ruta = leo_ini()   

df = pd.read_csv(os.path.join(ruta, "temporadas.csv"), sep = ',')
print df.head()
df["porcentaje_jug_esp"] = df["jug_esp"]/df["total_jug"]
df["porcentaje_jug_1"] = df["jug1"]/df["total_jug"]
df["porcentaje_jug_3"] = df["jug3"]/df["total_jug"]
df["porcentaje_jug_5"] = df["jug5"]/df["total_jug"]
df["porcentaje_jug_mas5"] = df["mas5"]/df["total_jug"]
df["total_min_no_esp"] = df["total_min"]-df["total_min_espana"]
df["porcentaje_min_esp"]= df["total_min_espana"]/df["total_min"]
df["porcentaje_min_no_esp"]= df["total_min_no_esp"]/df["total_min"]
df["total_puntos_no_esp"] = df["total_puntos"]-df["total_puntos_espana"]
df["porcentaje_puntos_esp"]= df["total_puntos_espana"]/df["total_puntos"]
df["porcentaje_puntos_no_esp"]= df["total_puntos_no_esp"]/df["total_puntos"]
df["total_val_no_esp"] = df["total_val"]-df["total_val_espana"]
df["porcentaje_val_esp"]= df["total_val_espana"]/df["total_val"]
df["porcentaje_val__no_esp"]= df["total_val_no_esp"]/df["total_val"]

# Reviewing the data

df.describe()

correlaciones = df.corr()
jugadores = ["jug1", "jug3", "jug5", "mas5"]
correlaciones[jugadores]
sns.boxplot(data=df[jugadores])
correlaciones[(correlaciones <= -0.5) & (correlaciones >= 0.5) & (correlaciones != 1)] #comprobamos si las correlaciones son mayores que 0,5
sns.boxplot(data = df)

result = sm.ols(formula="puesto ~ jug_esp + jug1 +jug3 + jug5 + mas5 + total_min_espana + total_min_no_esp + total_puntos + total_puntos_espana + total_puntos_no_esp", data=df).fit()
print result.params
result.summary()
result2 = sm.ols(formula="puesto ~ jug_esp + jug1 +jug3 + jug5 + mas5 + total_min_espana + total_min_no_esp + total_puntos + total_puntos_espana + total_puntos_no_esp", data=df).fit()
df.to_csv("D:\\Master\\ProyectoBasket\\Proyecto-Kschool-Basket\\temporadas_totalizado.csv", index=False)
result3 = sm.ols(formula="puesto ~ jug1 +jug3 + jug5 + porcentaje_jug_esp + porcentaje_min_esp", data=df).fit()
result3.summary()
#
# It seems that ther regression doesn't work we'll try to build a classification method. Though the position are numbers we can understand it like categories with values from 1 to 26. 
#

# Scaling the values , I'm going to select the numeric columns in the dataframe
columnas_numericas = ["PJ", "PG", "PP", "PF", "PC", "total_min", "total_val", "total_puntos", \
        "total_min_espana","total_puntos_espana", "total_val_espana", "total_jug", "jug_esp",\
       "jug1", "jug3", "jug5", "mas5", "porcentaje_jug_esp",\
       "porcentaje_jug_1", "porcentaje_jug_3", "porcentaje_jug_5",\
       "porcentaje_jug_mas5", "total_min_no_esp", "porcentaje_min_esp",\
       "porcentaje_min_no_esp", "total_puntos_no_esp",\
       "porcentaje_puntos_esp", "porcentaje_puntos_no_esp",\
       "total_val_no_esp", "porcentaje_val_esp", "porcentaje_val__no_esp"]

df_numerico = df[columnas_numericas]
clf = svm.SVC()
df_numerico = df_numerico.apply(lambda x: preprocessing.scale(x))
# adding target column 
df_numerico["puesto"] =df["puesto"]
# deleting PG and PP because we can't modify this values with people selection or behaviour. 
df_numerico = df_numerico.drop(labels="PG", axis=1)
df_numerico = df_numerico.drop(labels="PP", axis=1)

# Generating train and test subsets. If the accuracy is enough we'll use for control season that are not in the data (later 2016)
X_train, X_test, y_train, y_test = train_test_split(df_numerico[jugadores],df_numerico["puesto"],test_size=0.2,random_state=0)
C = 1.0  # SVM regularization parameter
# Model creation with only players by years in the league. Must be interesting for the result
svc = svm.SVC(kernel='linear', C=C).fit(X_train, y_train)
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X_train, y_train)
poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(X_train, y_train)
lin_svc = svm.LinearSVC(C=C).fit(X_train, y_train)
lista = [svc, rbf_svc,poly_svc,lin_svc]
listado = ["svc", "rbf_svc","poly_svc","lin_svc"]
contador = 0
for k in lista:
    clf_svm = k
    clf_svm.fit(X_train, y_train)
    y_pred_svm = clf_svm.predict(X_test)
    acc_svm = accuracy_score(y_test, y_pred_svm)
    print "accuracy %s: "%listado[contador],acc_svm
    contador = contador +1

#accuraccy is completely inefficient 

# Model building adding other variables

valores = ["PF", "PC", "total_min", "total_val","jug1", "jug3", "jug5", "mas5","total_jug","total_val_no_esp", "porcentaje_val_esp", "total_min_no_esp", "porcentaje_min_esp"]
X_train, X_test, y_train, y_test = train_test_split(df_numerico[valores],df_numerico["puesto"],test_size=0.2,random_state=0)
C = 1.0  # SVM regularization parameter
svc = svm.SVC(kernel='linear', C=C).fit(X_train, y_train)
rbf_svc = svm.SVC(kernel='rbf', gamma=0.7, C=C).fit(X_train, y_train)
poly_svc = svm.SVC(kernel='poly', degree=3, C=C).fit(X_train, y_train)
lin_svc = svm.LinearSVC(C=C).fit(X_train, y_train)
lista = [svc, rbf_svc,poly_svc,lin_svc]
listado = ["svc", "rbf_svc","poly_svc","lin_svc"]
contador = 0
for k in lista:
    clf_svm = k
    clf_svm.fit(X_train, y_train)
    y_pred_svm = clf_svm.predict(X_test)
    acc_svm = accuracy_score(y_test, y_pred_svm)
    print "accuracy %s: "%listado[contador],acc_svm
    contador = contador +1

# Better accuracy but still far from acceptables values 

