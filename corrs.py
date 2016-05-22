#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# corrs.py
# JuanDiego.SR92@gmail.com
# ------------------------------------------------------------------------------
# Clases y funciones necesarias para simular un objeto de tipo corriente. (No,
# no un objeto cualquiera).
# ------------------------------------------------------------------------------

class Corriente(object):
    """
    Una clase para contener las propiedades necesarias para simular una corriente.
    """
    
    def __init__(self, Ti, Tf, WCp):
        self.Ti = float(Ti) #temperatura inicial
        self.Tf = float(Tf) #temperatura final
        self.Tpp = 0        #temperatura del punto de pliegue
        self.WCp = float(WCp)
        self.cal = Ti > Tf  #verdadero si la corriente es una corriente caliente
    
    @property
    def Qapp(self):
        """
        Calcula el calor necesario arriba del punto de pliegue
        """
        if self.cal == True:
            return (self.Ti-self.Tpp)*self.WCp
        else:
            return (self.Tf-self.Tpp)*self.WCp
    @property
    def Qdpp(self):
        """
        Calcula el calor necesario debajo del punto de pliegue
        """
        if self.cal == True:
            return (self.Tpp-self.Tf)*self.WCp
        else:
            return (self.Tpp-self.Ti)*self.WCp
    
def enIntervalo(c, Ta, Tb):
    """
    Determina si la corriente c pasa por el intervalo de temperaturas [Ta, Tb].
    """
    
    if max([c.Ti, c.Tf]) > min([Ta, Tb]):
        if min([c.Ti, c.Tf]) < max([Ta, Tb]):
            return True
    else:
        return False
