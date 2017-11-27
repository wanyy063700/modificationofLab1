#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:19:36 2017

@author: wanyy063700

"""
import requests
import re
from bs4 import BeautifulSoup

alp=['https://www.noslang.com/dictionary/a/',
     'https://www.noslang.com/dictionary/b/',
     'https://www.noslang.com/dictionary/c/',
     'https://www.noslang.com/dictionary/d/',
     'https://www.noslang.com/dictionary/e/',
     'https://www.noslang.com/dictionary/f/',
     'https://www.noslang.com/dictionary/g/',
     'https://www.noslang.com/dictionary/h/',
     'https://www.noslang.com/dictionary/i/',
     'https://www.noslang.com/dictionary/j/',
     'https://www.noslang.com/dictionary/k/',
     'https://www.noslang.com/dictionary/l/',
     'https://www.noslang.com/dictionary/m/',
     'https://www.noslang.com/dictionary/n/',
     'https://www.noslang.com/dictionary/o/',
     'https://www.noslang.com/dictionary/p/',
     'https://www.noslang.com/dictionary/q/',
     'https://www.noslang.com/dictionary/r/',
     'https://www.noslang.com/dictionary/s/',
     'https://www.noslang.com/dictionary/t/',
     'https://www.noslang.com/dictionary/u/',
     'https://www.noslang.com/dictionary/v/',
     'https://www.noslang.com/dictionary/w/',
     'https://www.noslang.com/dictionary/x/',
     'https://www.noslang.com/dictionary/y/',
     'https://www.noslang.com/dictionary/z/',]

allwsl=[]
allwre=[]
for j in range(0,len(alp)):
    r=requests.get(alp[j]).text
    soup= BeautifulSoup(r,'lxml')

    #divide 3 parts

    wwd=soup.select('.dictionary-word')
    wsl=soup.select('.dictonary-slang')
    wre=soup.select('.dictonary-replacement')

    #list of repacement 
    strwre=[]
    #list of slang 
    strwsl=[]


    res = r'<dt>(.*?)</dt>'
    ree = r'<dd>(.*?)</dd>'

    for i in range(0,len(wwd)):
        #turn world of replacement into string
        wre[i]=str(wre[i])
        #turn word of slang into string
        wsl[i]=str(wsl[i])
        #list of str between 2 <a>
        slfl=re.findall(res,wsl[i],re.S|re.M)
        refl=re.findall(ree,wre[i],re.S|re.M)
        #turn into str
        slfl=str(slfl)
        refl=str(refl)
        
        strwsl.append(slfl[2:len(slfl)-4])
        #strwre.append(wre[i][40:len(strwre)-12-i])
        strwre.append(refl[2:len(refl)-2])

    for i in range(0,len(strwsl)):
        allwsl.append(strwsl[i])
        allwre.append(strwre[i])
 
print len(allwre)      

    
#################
#creat dict of slang
f=open('slangDict.txt','w')
for i in range(0,len(allwsl)):
    f.write(allwsl[i]+'\t'+allwre[i]+'\n')
f.close()

        







