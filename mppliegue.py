#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# mppliegue.py
# Método de punto de pliegue (pinch point) para obtener los servicios mínimos de
# calentamiento y enfriamiento necesarios para integrar completamente un sistema
# de corrientes.
# ------------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from corriente import *

def mpunto_pliegue(cc, dt_min=10):
    """
    Argumentos:
        cc    = vector de corrientes
        dt_min= delta T mínimo (opcional)
    Valor de retorno:
        Tpp   = temperatura de punto de pliegue
        smCal = servicio mínimo de calentamiento
        smEnf = servicio mínimo de enfriamiento
        
    Modifica la propiedad Tpp de cada corriente en cc. Es necesario ejecutar
    esta función antes que diagrama_corrientes() o curvas_compuestas() sobre el
    mismo vector de corrientes.
    """

    vTemp = []
    for c in cc:
        if c.cal == True:
            c.Ti = c.Ti - dt_min/2.0
            c.Tf = c.Tf - dt_min/2.0
        else:
            c.Ti = c.Ti + dt_min/2.0
            c.Tf = c.Tf + dt_min/2.0
        if c.Ti not in vTemp: vTemp.append(c.Ti)
        if c.Tf not in vTemp: vTemp.append(c.Tf)
    
    vTemp.sort(reverse=1)
    
    # Determinación del Wcp y Q por intervalo
    WCpInt = []
    QInt = []
    
    i = 1
    while i < len(vTemp):
        WCpi = 0
        for c in cc:
            if c.en_intervalo(vTemp[i-1], vTemp[i]):
                if c.cal == True:
                    WCpi = WCpi - c.WCp
                else:
                    WCpi = WCpi + c.WCp
        Qi = WCpi * (vTemp[i-1] - vTemp[i])

        WCpInt.append(WCpi)
        QInt.append(Qi)
        i = i + 1
    
    # Cascada de calor
    cascada = [0] * len(vTemp)

    i = 1
    while i < len(vTemp):
        cascada[i] = cascada[i-1] - QInt[i-1]
        i = i + 1

    while min(cascada) != 0:
        Qmin = min(cascada)
        i = 0
        while i < len(cascada):
            cascada[i] = cascada[i] - Qmin
            i = i + 1
    
    # Punto de pliegue
    pp = cascada.index(0)
    Tpp = vTemp[pp]
    smCal = cascada[0]
    smEnf = cascada[-1]
    
    # Imprimir la cascada de calor final
    ln_tem = "T:"
    for t in vTemp:
        ln_tem += f"{t:6.1f}"
    print(ln_tem)

    ln_tem = "Q:"
    for c in cascada:
        ln_tem += f"{c:6.1f}"
    print(ln_tem)
    
    # Restaura temperaturas orinales de las corrientes
    for c in cc:
        if c.cal == True:
            c.Tpp = Tpp + dt_min/2.0
            c.Ti = c.Ti + dt_min/2.0
            c.Tf = c.Tf + dt_min/2.0
        else:
            c.Tpp = Tpp - dt_min/2.0
            c.Ti = c.Ti - dt_min/2.0
            c.Tf = c.Tf - dt_min/2.0
    
    round2 = lambda x: round(x, 2)
    return list(map(round2, [Tpp, smCal, smEnf]))

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
    
    cfrs = [c for c in cc if c.cal == False]
    ccal = [c for c in cc if c.cal == True]
    
    plt.figure('Diagrama de Corrientes')
    
    i = 1
    while i <= len(cc):
        c = cc[i-1]
        sep = abs(c.Ti - c.Tf)/10
        x = np.linspace(c.Ti, c.Tf, 2)
        y = [i for v in x]
        if c.cal == True:
            plt.plot(x, y, 'r<-')
        else:
            plt.plot(x, y, 'b>-')

        if c.Qapp != 0:
            if c.cal == True:
                if c.Qapp != c.Qtotal: xm = (c.Tpp + c.Ti)/2
                else: xm = (c.Tf + c.Ti)/2 - sep
            else:
                if c.Qapp != c.Qtotal: xm = (c.Tpp + c.Tf)/2
                else: xm = (c.Ti + c.Tf)/2 - sep
            ym = i + 0.1
            plt.annotate(c.Qapp, xy=(xm,ym), xytext=(xm,ym))
        if c.Qdpp != 0:
            if c.cal == True:
                if c.Qdpp != c.Qtotal: xm = (c.Tpp + c.Tf)/2
                else: xm = (c.Ti + c.Tf)/2 - sep
            else:
                if c.Qdpp != c.Qtotal: xm = (c.Tpp + c.Ti)/2
                else: xm = (c.Tf + c.Ti)/2 - sep
            ym = i + 0.1
            plt.annotate(c.Qdpp, xy=(xm,ym), xytext=(xm,ym))
        i = i + 1
    
    minT, maxT = cc[0].Ti, cc[0].Tf
    for c in cc:
        if min(c.Ti, c.Tf) < minT: minT = min(c.Ti, c.Tf)
        if max(c.Ti, c.Tf) > maxT: maxT = max(c.Ti, c.Tf)
            
    #Graficar temperaturas de punto de pliegue
    TppCal = ccal[0].Tpp
    TppFrs = cfrs[0].Tpp
    plt.plot([TppFrs, TppFrs], [0, i], 'b--')
    plt.plot([TppCal, TppCal], [0, i], 'r--')
    
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
    
    cfrs = [c for c in cc if c.cal == False]
    ccal = [c for c in cc if c.cal == True]
    
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
            if c.en_intervalo(vTempCal[i], vTempCal[i-1]):
                Qi = Qi + (vTempCal[i] - vTempCal[i-1])*c.WCp
        hCal[i] = hCal[i-1] + Qi
        i = i + 1
    
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
            if c.en_intervalo(vTempFrs[i], vTempFrs[i-1]):
                Qi = Qi + (vTempFrs[i] - vTempFrs[i-1])*c.WCp
        hFrs[i] = hFrs[i-1] + Qi
        i = i + 1
    
    plt.figure('Curvas Compuestas')
    plt.plot(hCal, vTempCal, 'rs-')
    plt.plot(hFrs, vTempFrs, 'bs-')
    
    plt.grid(True)
    if u:
        plt.xlabel(u'Entalpía [%s]' %u[1])
        plt.ylabel(u'Temperatura [°%s]' %u[0])
    else:
        plt.xlabel(u'Entalpía')
        plt.ylabel('Temperatura')
    plt.title('Curvas Compuestas')
    plt.show()
    