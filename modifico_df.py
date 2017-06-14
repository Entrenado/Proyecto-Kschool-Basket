#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Read the web scrapped file, transform same values and start to apply Machine Learning
import pandas as pd
import os
import statsmodels.formula.api as sm
import seaborn as sns 
from sklearn.ensemble import RandomForestClassifier  
from sklearn.cross_validation import cross_val_score

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, svm
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.decomposition import PCA
from sklearn import grid_search

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
print 'RESULTADOS  REGRESION LINEAL' 

print ' -------------------------------------------------------------------------------------------------------------------------------------------'
result = sm.ols(formula="puesto ~ jug_esp + jug1 +jug3 + jug5 + mas5 + total_min_espana + total_min_no_esp + total_puntos + total_puntos_espana + total_puntos_no_esp", data=df).fit()
print result.params
print result.summary()
result2 = sm.ols(formula="puesto ~ jug_esp + jug1 +jug3 + jug5 + mas5 + total_min_espana + total_min_no_esp + total_puntos + total_puntos_espana + total_puntos_no_esp", data=df).fit()
df.to_csv("D:\\Master\\ProyectoBasket\\Proyecto-Kschool-Basket\\temporadas_totalizado.csv", index=False)
result3 = sm.ols(formula="puesto ~ jug1 +jug3 + jug5 + porcentaje_jug_esp + porcentaje_min_esp", data=df).fit()
print result3.summary()
##  

print ' -------------------------------------------------------------------------------------------------------------------------------------------'

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
print 'RESULTADOS  Accuracy SVM' 

print ' -------------------------------------------------------------------------------------------------------------------------------------------'

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
print ' -------------------------------------------------------------------------------------------------------------------------------------------'


# Better accuracy but still far from acceptables values 

# I will try, as suggested, with PCA. Let's see what are the results.

def plot_corr(df,size=10):
    '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
    df: pandas DataFrame
    size: vertical and horizontal size of the plot'''

    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)), corr.columns);
    plt.yticks(range(len(corr.columns)), corr.columns);
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)
        
columnas_sin_pct = ["PJ", "PG", "PP", "PF", "PC", "total_min", "total_val", "total_puntos", "total_min_espana","total_puntos_espana", "total_val_espana", "total_jug", "jug_esp",\
       "jug1", "jug3", "jug5", "mas5", \
       "total_min_no_esp", "total_puntos_no_esp",\
       "total_val_no_esp"]
otro_df = df[columnas_sin_pct]

plot_corr(df)
plot_corr(otro_df) 

#deleting percentages because it is usual that have high correlation in fact this is a calculation from the original number


# we'll try to use PCA to obtain better results.

valores2 = ["PF", "PC", "total_val","porcentaje_jug_esp",\
       "porcentaje_jug_1", "porcentaje_jug_3", "porcentaje_jug_5",\
       "porcentaje_jug_mas5", "porcentaje_min_esp", "porcentaje_val_esp"\
       ]

# A first View
import numpy as np
from sklearn.decomposition import PCA  
DATA = df_numerico[valores2].values
my_model = PCA(n_components=4)
my_model.fit_transform(DATA)

print df[valores2].columns
print my_model.explained_variance_
print my_model.explained_variance_ratio_
print my_model.explained_variance_ratio_.cumsum()

# Let's try to identify the best approach n_components
lista_valores_PCA = []
def genero_PCA(componentes):
    my_model = PCA(n_components=componentes)
    my_model.fit_transform(DATA)
    valores = np.insert(my_model.explained_variance_ratio_.cumsum(),0,0)
    return valores
lista_comp =[0]
plt.figure()
pos_H = 0
pos_V = 0
for x in range(1,10):
    componentes = x
    lista_comp.append(x)
    y = genero_PCA(componentes)
    plt.subplot2grid((3, 3), (pos_H, pos_V))
    plt.plot(lista_comp,y)
    if x%3 ==0 :
        pos_V = 0
        pos_H = pos_H + 1
    else:
        pos_V = x%3
plt.show()  

print "VALORES REGRESION LINEAL tras PCA"
print ' -------------------------------------------------------------------------------------------------------------------------------------------'
      
valores_PCA = my_model.fit_transform(DATA)
result_PCA = sm.OLS(df_numerico["puesto"], valores_PCA).fit()
print result_PCA.summary()

print ' -------------------------------------------------------------------------------------------------------------------------------------------'

# We remove the multicollinearity but the R squared is still very low. 

# Next step Random Forest.

clf = RandomForestClassifier(n_jobs=700)
clf.fit(X_train, y_train)
clf.feature_importances_
importance_sum = sum(clf.feature_importances_)
feat_imp_perct =  [100*(x/importance_sum) for x in clf.feature_importances_]
param_grid = {
                 'n_estimators': [50, 100, 150, 200],
                 'max_depth': [3, 4, 6, 7]
             }
grid_clf = grid_search.GridSearchCV(clf, param_grid, cv=10)
grid_clf.fit(X_train, y_train)
grid_clf. best_estimator_
grid_clf. best_params_
grid_clf. grid_scores_
print grid_clf. best_estimator_
best_clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini', \
            max_depth=4, max_features='auto', max_leaf_nodes=None,\
            min_impurity_split=1e-07, min_samples_leaf=1,\
            min_samples_split=2, min_weight_fraction_leaf=0.0,\
            n_estimators=50, n_jobs=700, oob_score=False,\
            random_state=None, verbose=0, warm_start=False)
best_clf.fit(X_train, y_train)
pred = best_clf.predict(X_test)
from sklearn import metrics
# testing score
pred = best_clf.predict(X_test)
PredOutputs = best_clf.predict(X_train)
# testing score
score = metrics.f1_score(y_test, pred,average='micro', pos_label=list(set(y_test)))
# training score
score_train = metrics.f1_score(y_train, PredOutputs ,average='micro', pos_label=list(set(y_train)))

print 'RESULTADOS RANDOM FOREST'
print ' -------------------------------------------------------------------------------------------------------------------------------------------'

print "f1 score with test data:", score
print "f1 score with train data:", score_train

print ' -------------------------------------------------------------------------------------------------------------------------------------------'

# lo que vamos a hacer es bajar la sensibilidad del ajuste. Es decir no queremos saber el puesto exacto si no si jugará playoff, descenderá o quedará en medio

def puesto(x):
    if x <= 8: x= "playoff"
    elif x >8 and x <=16: x="sin_playoff"
    else: x = "descenso"
    return x
    
df_numerico["sub_puesto"] = df_numerico["puesto"].apply(lambda x: puesto(x))

X_train, X_test, y_train, y_test = train_test_split(df_numerico[valores2],df_numerico["sub_puesto"],test_size=0.2,random_state=0)
best_clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini', \
            max_depth=4, max_features='auto', max_leaf_nodes=None,\
            min_impurity_split=1e-07, min_samples_leaf=1,\
            min_samples_split=2, min_weight_fraction_leaf=0.0,\
            n_estimators=50, n_jobs=700, oob_score=False,\
            random_state=None, verbose=0, warm_start=False)
best_clf.fit(X_train, y_train)
pred = best_clf.predict(X_test)
from sklearn import metrics
# testing score
pred = best_clf.predict(X_test)
PredOutputs = best_clf.predict(X_train)
# testing score
score = metrics.f1_score(y_test, pred,average='micro', pos_label=list(set(y_test)))
# training score
score_train = metrics.f1_score(y_train, PredOutputs ,average='micro', pos_label=list(set(y_train)))

print 'RESULTADOS RANDOM FOREST con baja sensibilidad'
print ' -------------------------------------------------------------------------------------------------------------------------------------------'

print "f1 score with test data:", score
print "f1 score with train data:", score_train

print ' -------------------------------------------------------------------------------------------------------------------------------------------'

