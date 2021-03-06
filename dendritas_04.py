# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 11:46:33 2022

@author: Muri
"""

import numpy as np 
import matplotlib.pyplot as plt

#Definición de la función Save_Li0
def Save_Li0(nn0,mm,lixx_d,liyy_d,exx,eyy,lixx_0,liyy_0,lixx_aux,liyy_aux):
    lixx_0 = np.zeros(mm)
    liyy_0 = np.zeros(mm)
    
    for i in range(nn0):
        lixx_aux[i] = lixx_d[i]
        liyy_aux[i] = liyy_d[i]
        
    lixx_aux[mm] = exx
    liyy_aux[mm] = eyy
    
    for i in range(mm):
        lixx_0[i] = lixx_aux[i]
        liyy_0[i] = liyy_aux[i]
        
    #PBC
    for i in range(mm):
        lixx_0[i] = lixx_0[i] - int(lixx_0[i]-0.5)
        liyy_0[i] = liyy_0[i] - int(liyy_0[i]+0.5) +1
    
    return lixx_0,liyy_0,lixx_aux,liyy_aux



# Inicialización de variables

dt = 1e-6
n0 = 77     #comienzo con este numero de li0 depositados sobre la sup
n0max = 600 #numero maximo de particulas li0
rli0 = 1.67e-10  #radio atomico del li0
rlim = 1.2e-10   #radio atomico del li+
nm = 50          #Este numero debe mantenerse a lo largo de la ev temporal
D = 1.4e-14      #coef de dif del Li+ en el electrolito
tita = 0
gx = 0
gy = 0
x=0
y=0
Long = 16.7e-9
datt = 1.3*rli0/Long     #que es rli0/(pi/4)
q = np.sqrt(2*D*dt)/Long   #desplazamiento medio debido a la difusion

alfa = 0
mod_li0 = 0

Rli_mx = 0
Rli_my = 0
Rli_0x = 0
Rli_0y = 0
modd = 0

u = 5.6e-13
E0_x = 0
E0_y = -1.7e7

rx = u*E0_x*dt/Long
ry = u*E0_y*dt/Long #mu+*E*dt/Long es el desplazamiento debido al campo electrico

#Inicialización de vectores 
ex = np.zeros(nm)
ey = np.zeros(nm)
ex_0 = np.zeros(nm)
ey_0 = np.zeros(nm)
lix_d = np.zeros(n0)
liy_d = np.zeros(n0)
lix_aux = np.zeros(n0max)
liy_aux = np.zeros(n0max)

#Creación de la monocapa de Li0 depositado

for i in range(n0):
    lix_d[i] = 1.3*rli0*i/Long
    liy_d[i] = 0/Long

#Creación de las posiciones iniciales de los iones

dx = rli0/(2*Long)
dy = rli0/(2*Long)

for i in range(nm):
    ex_0[i] = int(np.random.rand()*200)*dx
    ey_0[i] = int(np.random.rand()*200)*dy
    
#Comienza el loop de evolución temporal


m = n0      #Número inicial de Li0
nt = 1000   #Número de pasos temporales

#Los vectores lix_0 y liy_0 son los que van aumentando de dimension y me van contando en cada paso temporal cuantos li+ pasan a ser li0.
#Yo los puedo definir inicialmente como los litios depositados ya que m=n0
#Habria que ver que efectivamente aumenten de dimension dentro del loop temporal cuando m>n0

lix_0 = lix_d
liy_0 = liy_d 


lix_aux = np.zeros(n0max)
liy_aux = np.zeros(n0max)

for i in range(nt):
    for j in range(nm):
        tita = 2*np.pi*np.random.rand()
        #Definición del vector unitario g
        gx = np.cos(tita)
        gy = np.sin(tita)
        #Evolución de la posición de los iones
        ex[j] = ex_0[j] + q*gx + rx
        ey[j] = ey_0[j] + q*gy + ry
        #Meto las PBC en la caja de tamaño 1x1 (normalizada)
        ex[j] = ex[j] - int(ex[j]-0.5)
        ey[j] = ey[j] - int(ey[j]+0.5) + 1
        #Definición de la condición Li+-->Li0
        for k in range(m):
           # print('k = ',k)
            #if (m==600): 
                #break
            if (m<=n0):
                distx = ex[j] - lix_d[k]
                disty = ey[j] - liy_d[k]
                dist = np.sqrt(distx*distx + disty*disty)
            elif (m>n0):
                distx = ex[j] - lix_0[k]
                disty = ey[j] - liy_0[k]
                dist = np.sqrt(distx*distx + disty*disty)
                
            if (dist<datt):
                print('entró al dist < datt')
                if (m<=n0):
                    modd = np.sqrt((ex[j] - lix_d[k])*(ex[j] - lix_d[k]) + (ey[j] - liy_d[k])*(ey[j] - liy_d[k]))
                    exs = (ex[j]-lix_d[k])*datt/modd + lix_d[k]
                    eys = (ey[j]-liy_d[k])*datt/modd + liy_d[k]
                elif (m>n0):
                    modd = np.sqrt((ex[j] - lix_0[k])*(ex[j] - lix_0[k]) + (ey[j] - liy_0[k])*(ey[j] - liy_0[k]))
                    exs = (ex[j]-lix_0[k])*datt/modd + lix_0[k]
                    eys = (ey[j]-liy_0[k])*datt/modd + liy_0[k]
                
                print('m = ',m)
                m = m+1
                Save_Li0(n0,m,lix_d,liy_d,exs,eys,lix_0,liy_0,lix_aux,liy_aux)
                #repongo el ion
                ex[j] = int(np.random.rand()*200)*dx
                ey[j] = int(np.random.rand()*200)*dy
                #Las PBC
                ex[j] = ex[j] - int(ex[j]-0.5)
                ey[j] = ey[j] - int(ey[j]+0.5) + 1
            #else:
            #   if (m<=n0):
             #       modd = np.sqrt((ex[j] - lix_d[k])*(ex[j] - lix_d[k]) + (ey[j] - liy_d[k])*(ey[j] - liy_d[k]))
              #      exs = (ex[j]-lix_d[k])*datt/modd + lix_d[k]
               #     eys = (ey[j]-liy_d[k])*datt/modd + liy_d[k]
                #elif (m>n0):
                 #   modd = np.sqrt((ex[j] - lix_0[k])*(ex[j] - lix_0[k]) + (ey[j] - liy_0[k])*(ey[j] - liy_0[k]))
                  #  exs = (ex[j]-lix_0[k])*datt/modd + lix_0[k]
                   # eys = (ey[j]-liy_0[k])*datt/modd + liy_0[k]
                
                #Save_Li0(n0,m,lix_d,liy_d,exs,eys,lix_0,liy_0,lix_aux,liy_aux)
    t = (i+1)*dt
    ex_0 = ex
    ey_0 = ey
    print('i = ',i)
    
                
        
        
        
        
        
        
        
        
