# -*- coding: utf-8 -*-
from urllib2 import urlopen
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

url = 'http://www.bdbasket.com/es/index.html'
req = requests.get(url)
html = BeautifulSoup(req.text, "html.parser")

#print html
lista_url_temp = []
lista_a = html.findAll('a')

for j in lista_a:
     link= j.get('href')
     if str(link).find("t/t2") != -1 or str(link).find("t/t1") != -1:
         lista_url_temp.append('http://www.bdbasket.com/es/' +link)
print lista_url_temp