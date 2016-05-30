#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mppliegue.py
# JuanDiego.SR92@gmail.com
# ------------------------------------------------------------------------------
# Método de punto de pliegue (pinch point) para obtener los servicios mínimos de
# calentamiento y enfriamiento necesarios para integrar completamente un sistema
# de corrientes.
# ------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from corriente import *

def mpunto_pliegue(cc, DTmin=10):
    """
    Argumentos:
        cc    = vector de corrientes
        DTmin = delta T mínimo (opcional)
    Valor de retorno:
        Tpp   = temperatura de punto de pliegue
        smCal = servicio mínimo de calentamiento
        smEnf = servicio mínimo de enfriamiento
        
    Modifica la propiedad Tpp de cada corriente en cc. Es necesario ejecutar
    esta función antes que diagrama_corrientes() o curvas_compuestas() sobre el
    mismo vector de corrientes.
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
        #excepto si la temperatura a agregar ya se encuentra en el vector
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
            if c.enIntervalo(vTemp[i-1], vTemp[i]):
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
        while i < len(cascada):
            #Restar el valor mínimo a cada elemento del vector cascada
            cascada[i] = cascada[i] - Qmin
            i = i + 1
    
    pp = cascada.index(0) #el punto de pliegue es el lugar (índice) donde hay un
                          #cero en la cascada de calor. En caso de múltiples
                          #puntos de pliegue este método elegirá al primero.
    Tpp = vTemp[pp]       #temperatura del punto de pliegue
    smCal = cascada[0]    #servicio mínimo de calentamiento
    smEnf = cascada[-1]   #servicio mínimo de enfriamiento
    
    #Impresión de la cascada de calor final
    i = 0
    print "T:",
    while i < len(vTemp)-1:
        print vTemp[i],'->',
        i = i + 1
    print vTemp[i]
    i = 0
    print "Q:",
    while i < len(cascada)-1:
        print "%.2f %s" % (cascada[i],'->'),
        i = i + 1
    print "%.2f" % cascada[i]
    
    #Restaurar las temperaturas de las corrientes a sus valores originales
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
    
    round2 = lambda x: round(x,2)
    return map(round2, [Tpp, smCal, smEnf])

def diagrama_corrientes(cc, u=None):
    """
    Argumentos:
        cc = vector de corrientes
        u  = unidades de temperatura (str)
    Valor de retorno:
        Sin valor de retorno
    
    Esta función permite visualizar las corrientes dadas en el vector cc. Todas
    las corrientes se grafican entre x=Ti y x=Tf. La primera corriente en y=1,
    la segunda en y=2, la n-ésima en y=n. Las corrientes frías se grafican en
    azul y las calientes en rojo. La temperatura de punto de pliegue se grafica
    en el color correspondiente. En la gráfica también aparecen las cargas de las
    corrientes, tanto arriba como debajo del punto de pliegue si es el caso.
    Es necesario ejecutar mpunto_pliegue(cc) antes que esta función para obtener
    los resultados deseados.
    """
    
    cfrs = [c for c in cc if c.cal == False] #corrientes frías
    ccal = [c for c in cc if c.cal == True]  #corrientes calientes
    
    plt.figure('Diagrama de Corrientes')
    
    i = 1
    while i <= len(cc):
        c = cc[i-1]
        sep = abs(c.Ti - c.Tf)/10
        x = np.linspace(c.Ti, c.Tf,2)
        y = [i for v in x]
        if c.cal == True:
            plt.plot(x,y,'r<-') #rojo para las calientes
        else:
            plt.plot(x,y,'b>-') #azul para las frías
        #Calores arriba/debajo del punto de pliegue
        if c.Qapp != 0:
            if c.cal == True:
                if c.Qapp != c.Qtotal: xm = (c.Tpp+c.Ti)/2
                else: xm = (c.Tf+c.Ti)/2-sep
            else:
                if c.Qapp != c.Qtotal: xm = (c.Tpp+c.Tf)/2
                else: xm = (c.Ti+c.Tf)/2-sep
            ym = i + 0.1
            plt.annotate(c.Qapp, xy=(xm,ym), xytext=(xm,ym))
        if c.Qdpp != 0:
            if c.cal == True:
                if c.Qdpp != c.Qtotal: xm = (c.Tpp+c.Tf)/2
                else: xm = (c.Ti+c.Tf)/2-sep
            else:
                if c.Qdpp != c.Qtotal: xm = (c.Tpp+c.Ti)/2
                else: xm = (c.Tf+c.Ti)/2-sep
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
    plt.plot([TppFrs, TppFrs], [0, i], 'b--')
    plt.plot([TppCal, TppCal], [0, i], 'r--')
    
    #Ajustes del gráfico
    plt.axis([minT-10, maxT+10, 0, i])
    plt.title('Diagrama de Corrientes')
    if u: plt.xlabel(u'Temperatura [°%s]' %u)
    else: plt.xlabel('Temperatura')
    plt.ylabel('Corrientes')
    plt.show()

def curvas_compuestas(cc, smEnf, u=None):
    """
    Argumentos:
        cc    = vector de corrientes
        smEnf = servicio mínimo de enfriamiento
        u     = vector de unidades (0 => temperatura, 1 => entalpía)
    Valor de retorno:
        Sin valor de retorno
        
    Grafica la curva compuesta fría y la curva compuesta caliente en un diagrama
    de entalpía (X) contra temperatura (Y).
    """
    
    cfrs = [c for c in cc if c.cal == False] #corrientes frías
    ccal = [c for c in cc if c.cal == True]  #corrientes calientes
    
    # Curva compuesta caliente
    vTempCal = []
    for c in ccal:
        if c.Ti not in vTempCal: vTempCal.append(c.Ti)
        if c.Tf not in vTempCal: vTempCal.append(c.Tf)
    vTempCal.sort()
    
    hCal = [0] * len(vTempCal)
    i = 1
    while i < len(hCal):
        Qi = 0
        for c in ccal:
            if c.enIntervalo(vTempCal[i], vTempCal[i-1]):
                Qi = Qi + (vTempCal[i]-vTempCal[i-1]) * c.WCp
        hCal[i] = hCal[i-1] + Qi
        i = i + 1
    
    # Curva compuesta fría
    vTempFrs = []
    for c in cfrs:
        if c.Ti not in vTempFrs: vTempFrs.append(c.Ti)
        if c.Tf not in vTempFrs: vTempFrs.append(c.Tf)
    vTempFrs.sort()
    
    hFrs = [smEnf] * len(vTempFrs)
    i = 1
    while i < len(hFrs):
        Qi = 0
        for c in cfrs:
            if c.enIntervalo(vTempFrs[i], vTempFrs[i-1]):
                Qi = Qi + (vTempFrs[i]-vTempFrs[i-1]) * c.WCp
        hFrs[i] = hFrs[i-1] + Qi
        i = i + 1
    
    #Gráficas
    plt.figure('Curvas Compuestas')
    plt.plot(hCal, vTempCal, 'rs-')
    plt.plot(hFrs, vTempFrs, 'bs-')
    
    #Ajustes del gráfico
    plt.grid(True)
    if u:
        plt.xlabel(u'Entalpía [%s]' %u[1])
        plt.ylabel(u'Temperatura [°%s]' %u[0])
    else:
        plt.xlabel(u'Entalpía')
        plt.ylabel('Temperatura')
    plt.title('Curvas Compuestas')
    plt.show()
    
