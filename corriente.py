#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# corriente.py
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
        self.Tpp = self.Ti  #temperatura del punto de pliegue
        self.WCp = float(WCp)
        self.cal = Ti > Tf  #verdadero si la corriente es una corriente caliente
    
    @property
    def Qtotal(self):
        """Carga térmica de la corriente en valor absoluto."""
        return abs(self.Tf-self.Ti) * self.WCp
    
    @property
    def Qdpp(self):
        """
        Calcula el calor que necesita la corriente debajo del punto de pliegue.
        Regresa el valor absoluto.
        """

        if self.cal == True:
            if self.Ti <= self.Tpp:
                #la corriente no cruza el punto de pliegue
                q = self.Qtotal
            else:
                q = (self.Tpp-self.Tf)*self.WCp
        else:
            if self.Tf <= self.Tpp:
                #la corriente no cruza el punto de pliegue
                q = self.Qtotal
            else:
                q = (self.Tpp-self.Ti)*self.WCp
        
        if q > 0: return q
        else: return 0
        
    @property
    def Qapp(self):
        """
        Calcula el calor que necesita la corriente arriba del punto de pliegue.
        Regresa el valor absoluto.
        """

        if self.cal == True:
            if self.Tf >= self.Tpp:
                #la corriente no cruza el punto de pliegue
                q = self.Qtotal
            else:
                q = (self.Ti-self.Tpp)*self.WCp
        else:
            if self.Ti >= self.Tpp:
                #la corriente no cruza el punto de pliegue
                q = self.Qtotal
            else:
                q = (self.Tf-self.Tpp)*self.WCp
                
        if q > 0: return q
        else: return 0
                
    def enIntervalo(self, Ta, Tb):
        """
        Determina si la corriente pasa por el intervalo de temperaturas [Ta, Tb].
        """
        
        if max([self.Ti, self.Tf]) > min([Ta, Tb]):
            if min([self.Ti, self.Tf]) < max([Ta, Tb]):
                return True
        else:
            return False
