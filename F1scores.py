#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:08:17 2017

@author: wanyy063700
"""
#different conditons of results,e.g. f0[0] is the Num_f1 of system with slang
f=[,
]

#counts of 3 sentiments in twitter-2016test-A
t1=[]
t2=[]
t3=[]
f1=[]
f2=[]
f3=[]


s=[2000,994,681,325]
for i in range(0,len(f)):
   # positive
    t1.append(s[1]-f[i][0]-f[i][1])
    f1.append(f[i][2]+f[i][4])
    #netral
    t2.append(s[2]-f[i][2]-f[i][3])
    f2.append(f[i][0]+f[i][5])
    #negative
    t3.append(s[3]-f[i][4]-f[i][5])
    f3.append(f[i][1]+f[i][3])
    
# evaluation
pre1=[]
pre2=[]
pre3=[]
re1=[]
re2=[]
re3=[]
acc=[]
for i in range(0,len(t1)):
    pre1.append(t1[i]*10000/(t1[i]+f1[i]))
    pre2.append(t2[i]*10000/(t2[i]+f2[i]))
    pre3.append(t3[i]*10000/(t3[i]+f3[i]))
    re1.append(t1[i]*10000/s[1])
    re2.append(t2[i]*10000/s[2])
    re3.append(t3[i]*10000/s[3])
    acc.append((t1[i]+t2[i]+t3[i])*10000/(s[0]))
print pre1
print pre2
print pre3
print re1
print re2
print re3
print acc

print'#########precision, recall and accuracy################'

# F1-scores
F1=[]
F2=[]
F3=[]
F=[]
for i in range(0,len(pre1)):
    F1.append(2*re1[i]*pre1[i]/(pre1[i]+re1[i]))
    F2.append(2*re2[i]*pre2[i]/(pre2[i]+re2[i]))
    F3.append(2*re3[i]*pre3[i]/(pre3[i]+re3[i]))
    F.append((994.00/2000)*F1[i]+(681.00/2000)*F2[i]+(325.00/2000)*F3[i])
print F1
print F2
print F3
print F
"""
#prececision-p
prep=tpns*1000/(tpns+fpns)
print prep
#recall
rep=tp1*1000/s[1]
print rep
#F1-score of P

F=2*rep*prep/(prep+rep)
print F
#F1-score of N0
#F1-score of N1
"""
