# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 19:11:03 2019

Plotear

@author: Paulina Pizarro
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_lineas(zona,zonas, t):
    comercio = []
    H1 = []
    H2 = []
    H3 = []
    eje_zonas = []
    for i in range(1, len(zonas)+1):
        comercio.append(zona[t, i].comercio)
        H1.append(zona[t, i].n_h1)
        H2.append(zona[t, i].n_h2)
        H3.append(zona[t, i].n_h3)
        eje_zonas.append(i)
    ind = [x for x, _ in enumerate(eje_zonas)]
    H1 = np.array(H1)
    H2 = np.array(H2)
    H3 = np.array(H3)
    comercio= np.array(comercio)
    plt.figure(figsize=(20,12))
    plt.bar(ind, H1, width=0.8, label='H1', color='#3498DB', bottom=H3+H2)
    plt.bar(ind, H2, width=0.8, label='H2', color='#2874A6', bottom=H3)
    plt.bar(ind, H3, width=0.8, label='H3', color='#1B4F72')
    plt.bar(ind, comercio, width=0.8, label='Comercio', color='#AF7AC5',bottom=H3+H2+H1)
    
            
    plt.xticks(ind, eje_zonas)
    plt.ylabel("Agentes")
    plt.xlabel("zonas")
    plt.legend(loc="upper right")
    plt.title("Localizacion periodo " + str(t))    
    plt.show()
    
def plot_comparar(zona,zonas, t,t2):
    localizados1 = []
    localizados2 = []
    aux = 0
    aux2 = 0
    eje_zonas = []
    for i in range(1, len(zonas)+1):
        aux = (zona[t, i].comercio +
        zona[t, i].n_h1 + zona[t, i].n_h2
        + zona[t, i].n_h3)
        aux2 = (zona[t2, i].comercio +
        zona[t2, i].n_h1 + zona[t2, i].n_h2
        + zona[t2, i].n_h3)
        eje_zonas.append(i)
        localizados1.append(aux)
        localizados2.append(aux2)
    print(localizados2[93])
    ind = [x for x, _ in enumerate(eje_zonas)]
    t1 = np.array(localizados1)
    t22 = np.array(localizados2)
    plt.figure(figsize=(25,13))
    plt.plot(ind, t1, label='periodo ' + str(t), color='red')
    plt.plot(ind, t22, label='periodo ' + str(t2), color='blue')   
    plt.xticks(ind, eje_zonas)
    plt.ylabel("Agentes")
    plt.xlabel("zonas")
    plt.legend(loc="upper right")
    plt.title("Localizacion periodo " + str(t) + " y "+ str(t2))    
    plt.show()