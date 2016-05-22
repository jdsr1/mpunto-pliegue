#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mppliegue.py
# JuanDiego.SR92@gmail.com
# ------------------------------------------------------------------------------
# Método de punto de pliegue (Pinch point method) para obtener los servicios   
# mínimos de calentamiento y enfriamiento necesarios para integrar completamente
# un sistema de corrientes.
# ------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from corrs import *

def mpp(cc, DTmin=10):
	"""
	Regresa los servicios de calentamiento y enfriamiento mínimos, así como la
	temperatura del punto de pliegue para el sistema formado por las corrientes
	en el vector cc. Modifica la propiedad Tpp de cada corriente en cc.
	"""

	vTemp = [] #vector de temperaturas
	
	for c in cc:
		if c.cal == True:
			#Ajuste de temperaturas para corrientes calientes
			c.Ti = c.Ti - DTmin/2.0
			c.Tf = c.Tf - DTmin/2.0
		else:
			#Ajuste de temperaturas para corrientes frías
			c.Ti = c.Ti + DTmin/2.0
			c.Tf = c.Tf + DTmin/2.0
		#Agregar las temperaturas ajustadas al vector de temperaturas,
		#excepto si la temperaturas a agregar ya se encuentra en el vector
		if c.Ti not in vTemp: vTemp.append(c.Ti)
		if c.Tf not in vTemp: vTemp.append(c.Tf)
	
	#Ordenar el vector de temperaturas de mayor a menor
	vTemp.sort(reverse=1)
	
	WCpInt = [] #WCp por intervalo
	QInt = []   #Q por intervalo
	
	#Determinación del Wcp y Q por intervalo
	i = 1 #intervalo 1
	while i < len(vTemp):
		WCpi = 0
		for c in cc:
			#sólo considerar aquellas corrientes que están en el intervalo
			if enIntervalo(c, vTemp[i-1], vTemp[i]):
				if c.cal == True:
					#si la corriente es una corriente caliente
					#restar su WCp al WCp del intervalo
					WCpi = WCpi - c.WCp
				else:
					#si la corriente es una corriente fría
					#sumar su WCp al WCp del intervalo
					WCpi = WCpi + c.WCp
		#calcular el calor por intervalo
		Qi = WCpi * (vTemp[i-1] - vTemp[i])
		WCpInt.append(WCpi) #agregar WCpi al vector de WCp
		QInt.append(Qi)     #agregar Qi al vector de Q
		i = i + 1
	
	#Cascada de calor. Mismo tamaño que el vector vTemp
	cascada = [0] * len(vTemp)
	#Primera iteración. Suponer que el primer valor en la cascada es 0
	i = 1
	while i < len(vTemp):
		cascada[i] = cascada[i-1] - QInt[i-1]
		i = i + 1

	#Comprobación de la cascada de calor. El valor mínimo debería ser un 0
	while min(cascada) != 0:
		Qmin = min(cascada)
		i = 0
		while i < len(vTemp):
			#Restar el valor mínimo a cada elemento del vector cascada
			cascada[i] = cascada[i] - Qmin
			i = i + 1
	
	pp = cascada.index(0) #el punto de pliegue es el lugar (índice) donde hay un cero
	                      #en la cascada de calor. (Este método no considera múltiples
	                      #puntos de pliegue)
	Tpp = vTemp[pp]	      #temperatura del punto de pliegue
	smcal = cascada[0]    #servicio mínimo de calentamiento
	smenf = cascada[-1]   #servicio mínimo de enfriamiento
	
	#Impresión de la cascada de calor final
	i = 0
	print "T: ",
	while i < len(vTemp)-1:
		print vTemp[i],'->',
		i = i + 1
	print vTemp[i]
	i = 0
	print "Q: ",
	while i < len(cascada)-1:
		print cascada[i],'->',
		i = i + 1
	print cascada[i]
	
	#Restaurar las temperaturas de las corrientes a sus valores originales.
	#Agregar la temperatura de punto de pliegue a cada corriente
	for c in cc:
		if c.cal == True:
			c.Tpp = Tpp + DTmin/2.0
			c.Ti = c.Ti + DTmin/2.0
			c.Tf = c.Tf + DTmin/2.0
		else:
			c.Tpp = Tpp - DTmin/2.0
			c.Ti = c.Ti - DTmin/2.0
			c.Tf = c.Tf - DTmin/2.0
	
	#Regresar la temperatura del punto de pliegue y los servicios mínimos
	round2 = lambda x: round(x,2)
	return map(round2, [Tpp, smcal, smenf])

def ddc(cc):
    """
    Una función para visualizar las corrientes dadas en el vector cc, una vez la
    propiedad Tpp de cada corriente ha sido ajustada. Todas las corrientes se
    grafican entre x=Ti y x=Tf. La primera corriente en y=1, la segunda en y=2,
    la n-ésima en y=n. Primero se grafican las corrientes frías (azules) y luego
    las corrientes calientes (rojas).
    """
    
    cfrs = [c for c in cc if c.cal == False] #corrientes frías
    ccal = [c for c in cc if c.cal == True]  #corrientes calientes
    cc = cfrs + ccal #graficar primero las corrientes frías
    j = len(cfrs)
    
    i = 1
    while i <= len(cc):
        c = cc[i-1]
        sep = abs(c.Ti - c.Tf)/10
        x = np.linspace(c.Ti, c.Tf, sep)
        y = [i for v in x]
        if c.cal == True:
            plt.plot(x,y,'r<-') #rojo para las calientes
        else:
            plt.plot(x,y,'b>-') #azul para las frías
        #Anotar calores arriba/debajo del punto de pliegue
        if c.Qapp != 0:
            if c.cal == True:
                xm = (c.Tpp+c.Ti)/2
            else:
                xm = (c.Tpp+c.Tf)/2
            ym = i + 0.1
            plt.annotate(c.Qapp, xy=(xm,ym), xytext=(xm,ym))
        if c.Qdpp != 0:
            if c.cal == True:
                xm = (c.Tpp+c.Tf)/2
            else:
                xm = (c.Tpp+c.Ti)/2
            ym = i + 0.1
            plt.annotate(c.Qdpp, xy=(xm,ym), xytext=(xm,ym))
        i = i + 1
    
    minT, maxT = cc[0].Ti, cc[0].Tf
    for c in cc:
        if min(c.Ti,c.Tf) < minT: minT = min(c.Ti,c.Tf)
        if max(c.Ti,c.Tf) > maxT: maxT = max(c.Ti,c.Tf)
            
    #Graficar temperaturas de punto de pliegue
    TppCal = ccal[0].Tpp
    TppFrs = cfrs[0].Tpp
    plt.plot([TppFrs, TppFrs], [0, j+0.25], 'b-.')
    plt.plot([TppFrs, TppCal], [j+0.25, j+0.75], 'k-.')
    plt.plot([TppCal, TppCal], [j+0.75, i], 'r-.')
    
    #Ajustes del gráfico
    plt.axis([minT-10, maxT+10, 0, i])
    plt.title("Diagrama de Corrientes")
    plt.grid(True)
    plt.xlabel("Temperatura")
    plt.ylabel("Corrientes")
    plt.show()

## Ejemplo
#c1 = Corriente(175,45, 10)
#c2 = Corriente(125,65, 40)
#c3 = Corriente(20,155, 20)
#c4 = Corriente(40,112, 15)

#vc = [c1,c2,c3,c4]
#mpp(vc, 20)
#ddc(vc)
