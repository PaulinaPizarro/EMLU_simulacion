# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 19:11:03 2019

Plotear

@author: Paulina Pizarro
"""

import math
from copy import copy
import random


# =============================================================================
# CLASES
# =============================================================================

#clase zona con todos sus valores
class zona_obj:
    def __init__(self, idi, comercio, educacion, n_h1, 
                 n_h2, n_h3, cap_res, cap_no_res, precio):
        self.id = idi
        self.comercio = comercio
        self.educacion = educacion
        self.n_h1= n_h1
        self.n_h2= n_h2
        self.n_h3= n_h3
        self.cap_res = cap_res
        self.cap_no_res = cap_no_res
        self.precio = precio

#clase de agentes por localizar por periodo
class por_localizar_obj:
    def __init__(self, periodo, comercio, h1, h2, h3):
        self.periodo = periodo
        self.comercio = comercio
        self.n_h1 = h1
        self.n_h2 = h2
        self.n_h3 = h3


# =============================================================================
# FUNCIONES 
# =============================================================================
       
#abrir archivo con informacion de las zonas en t0
#guarda la info en la lista zonas
def leer_archivo(nombre_archivo):
    lista_datos = []
    archivo_aux=open(nombre_archivo, 'r')
    linea = archivo_aux.readlines()
    for l in linea:
        if linea.index(l)>=1:
            lista_datos.append(l.split())
    archivo_aux.close()
    return lista_datos
        
        
#calcular accesibilidad
#entrega las listas con accesibilidades calculadas
def calcular_accesibilidad(periodo, zona, costos_dict, n_zonas, phi):        
    Accesibilidad_comercio= []
    Accesibilidad_educacion = []
    for i in range(1,(n_zonas+1)):
        acc_aux_comercio = 0
        acc_aux_educacion = 0
        for j in range(1, (n_zonas+1)):
            acc_aux_comercio += zona[periodo,j].comercio*math.exp(-phi*costos_dict[i,j])
            acc_aux_educacion += zona[periodo,j].educacion*math.exp(-phi*costos_dict[i,j])
        Accesibilidad_comercio.append(int(acc_aux_comercio))
        Accesibilidad_educacion.append(int(acc_aux_educacion))
    return Accesibilidad_comercio, Accesibilidad_educacion
        
# calcular disposicion a pagar
#entrega un diccionario que recibe una tupla agente, zona
def calcular_DP(betas, acc_comercio, acc_educacion, zona, periodo):
    n_zonas = len(acc_comercio)
    t = periodo
    DP ={}
    for i in range(1, n_zonas + 1):
        for agente in betas:
            DP[agente,i] = (betas[agente][0]*acc_educacion[i-1] 
                          + betas[agente][1]*acc_comercio[i-1]
                          + betas[agente][2]*zona[t,i].n_h1
                          + betas[agente][3]*zona[t,i].precio)     
    return DP

# Calcular probabilidad
#entrega un diccionario de probabilidades que recibe una tupla zona, agente
def calcular_probabilidad(betas, n_zonas, zona, DP, alpha, mu, t):
    prob_aux2 = 0
    prob_aux1 = {}
    prob= {}
    for h in betas:
        prob_aux = 0
        for i in range(1, (n_zonas + 1)):
            #print(zona[t,i].precio)
            prob_aux += math.exp(mu*(DP[h,i]-alpha*zona[t,i].precio))
        prob_aux1[h] = prob_aux
    
    for h in betas:
        for i in range(1, (n_zonas+1)):
            prob_aux2 = math.exp(mu*(DP[h,i]-alpha*zona[t,i].precio))
            prob_aux3 = prob_aux1[h]
            prob[i,h]= prob_aux2/prob_aux3
    return prob

#funcion para hacer una lista aux para monte carlo
#calcula las probabilidades y las va sumando
def MC_hacerlista(probabiliad,agente, n_zonas, t):
    P_mc = {}
    P_mc2 = {}
    aux_suma = 0
    if agente == "comercio":
        for i in range(1,n_zonas+1):
            if zona[t,i].cap_no_res > 0:
                aux_suma += probabilidad[i, agente]
                P_mc[i]=aux_suma
    else:
        for i in range(1,n_zonas+1):
            if zona[t,i].cap_res > 0:
                aux_suma += probabilidad[i, agente]
                P_mc[i]=aux_suma
    for i in P_mc:
        P_mc2[i] = P_mc[i]/aux_suma
    return P_mc2

#funcion que localiza los agentes
#agrega los agentes a las zonas en cada periodo
def localizar(i_selec, t, agente):
    if agente == "comercio":
        zona[t,i_selec].cap_no_res -= 1
        por_localizar_dict[t].comercio -= 1
        zona[t,i_selec].comercio +=1
    elif agente == "n_h1": 
        zona[t,i_selec].cap_res -= 1
        por_localizar_dict[t].n_h1 -= 1
        zona[t,i_selec].n_h1 +=1
    elif agente == "n_h2": 
        zona[t,i_selec].cap_res -= 1
        por_localizar_dict[t].n_h2 -= 1
        zona[t,i_selec].n_h2 +=1
    elif agente == "n_h3": 
        zona[t,i_selec].cap_res -= 1
        por_localizar_dict[t].n_h3 -= 1
        zona[t,i_selec].n_h3 +=1
        return







# =============================================================================
# EMPIEZA EL CODIGO QUE EJECUTA LAS FUNCIONES
# =============================================================================

#los diccionarios que usar
""" Las variables son globales para poder usarlas en las funciones
sin tener que entregarlas de nuevo a cada una"""
      
global zona
zona = {}
global por_localizar_dict
por_localizar_dict = {}
costos_dict ={}

#listas auxiliares
zonas=[]
por_localizar = []
costos = []

#llamo la funcion leer_archivo para todos mis datos
zonas = leer_archivo("zonas_t0.txt")            
por_localizar = leer_archivo("agentes_por_localizar.txt")
costos = leer_archivo("C_ij.txt")


# diccionario para mis zonas (que son objetos de la clase zona_obj)
""" el diccionario tiene una llave que es una tupla [t,z] donde t es el periodo
y z es la zona"""

for t in range(0, len(por_localizar)):
    for z in zonas:
        idi = int(z[0])
        comercio = int(z[1])
        educacion = int(z[2])
        n_h1 = int(z[3])
        n_h2 = int(z[4])
        n_h3 = int(z[5])
        cap_res = int(z[6])
        cap_no_res = int(z[7])
        precio= int(z[8])
        zona[t ,int(z[0])]=zona_obj(idi, comercio, educacion, n_h1,
                     n_h2, n_h3, cap_res, cap_no_res, precio)

#diccionario para mis agentes por localizar donde la llave es el periodo 
for t in por_localizar:
    periodo, comercio, h1, h2, h3 = int(t[0]), int(t[1]), int(t[2]), int(t[3]), int(t[4])
    por_localizar_dict[int(t[0])]= por_localizar_obj(periodo,comercio,h1, h2,h3)

# diccionario de costos, la llave es una tupla [i,j] entre dos zonas
n_zonas= len(costos)
for fila in costos:
    for n in range(1,(n_zonas+1)):
        costos_dict[int(fila[0]), n] = int(fila[n])

#defino mis parametros
phi = 0.2
mu = 0.1
alpha = 0.2
#genero un vector con mis betas por agente
# OJO: estos numeros estan muy inventados
betas  = {"comercio":[0, 0.9, 0.4, -0.02],"n_h1":[0.03, 0.1, 0.4, 0.01],"n_h2":[0.04, 0.2, 0.25, -0.04],"n_h3":[0.03, 0.2, 0.2, -0.5]}

#empieza la simulacion
for t in range(1, len(por_localizar)):
    #se asume que al comienzo todos los agentes podrian querer localizarse
    #esto puede no ser cierto
    agentes_no_localizados = ["comercio","n_h1","n_h2","n_h3"]
    acc_comercio, acc_educacion = calcular_accesibilidad(t-1, zona, costos_dict, n_zonas, phi)
    DP = calcular_DP(betas, acc_comercio, acc_educacion, zona, t-1)
    probabilidad = calcular_probabilidad(betas, n_zonas, zona, DP, alpha, mu, t-1)
    
    #OJO: calcule las DP segun las localizaciones del periodo anterior
    #la localizacion la hago con el periodo actual
    while agentes_no_localizados:
        #Elijo un agente al azar y aplico monte carlo
        agente_azar= random.choice(agentes_no_localizados)
        P_mc = MC_hacerlista(probabilidad,agente_azar, n_zonas,t)
        dado = random.random()
        for p in P_mc:
            if P_mc[p] >= dado:
                localizar(p, t, agente_azar)
                break
        #despues de localizar reviso que agentes necesitan
        #localizarse para volver hacer el random por agentes
        agentes_no_localizados = []
        if por_localizar_dict[t].comercio > 0:
            agentes_no_localizados.append("comercio")
        if por_localizar_dict[t].n_h1 > 0:
            agentes_no_localizados.append("n_h1")
        if por_localizar_dict[t].n_h2 > 0:
            agentes_no_localizados.append("n_h2")
        if por_localizar_dict[t].n_h3 > 0:
            agentes_no_localizados.append("n_h3")
    #terminando actualizo el periodo t+1 que comienza con las localizaciones
    #del periodo anterior
    """el copy sirve para evitar que se igualen por referencia 
    las variables y solo tome el valor """
    
    for i in range(1, n_zonas+1):
        zona[t+1,i] = copy(zona[t,i])



#esto es para plotear    
from plot import plot_lineas, plot_comparar

#Para comparar dos periodos distintos
plot_comparar(zona,zonas,19,20)

#Para plotear un periodo especifico y mostrar cada agente
plot_lineas(zona,zonas,10)