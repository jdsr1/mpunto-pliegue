#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# corriente.py
# Clases y funciones necesarias para simular un objeto de tipo corriente.
# ------------------------------------------------------------------------------


class Corriente(object):
    def __init__(self, Ti, Tf, WCp):
        self.Ti = float(Ti)
        self.Tf = float(Tf)
        self.Tpp = self.Ti
        self.WCp = float(WCp)
        self.cal = Ti > Tf
    
    @property
    def Qtotal(self):
        """Carga térmica de la corriente en valor absoluto."""
        q = abs(self.Tf - self.Ti)*self.WCp
        q = round(q, 2)
        return q
    
    @property
    def Qdpp(self):
        """
        Calcula el calor que necesita la corriente debajo del punto de pliegue.
        Regresa el valor absoluto.
        """

        if self.cal == True:
            # La corriente no cruza el punto de pliegue
            if self.Ti <= self.Tpp:
                q = self.Qtotal
            else:
                q = (self.Tpp - self.Tf)*self.WCp
        else:
            # La corriente no cruza el punto de pliegue
            if self.Tf <= self.Tpp:
                q = self.Qtotal
            else:
                q = (self.Tpp - self.Ti)*self.WCp
        
        q = round(q, 2)
        return q if q > 0 else 0
        
    @property
    def Qapp(self):
        """
        Calcula el calor que necesita la corriente arriba del punto de pliegue.
        Regresa el valor absoluto.
        """

        if self.cal == True:
            # La corriente no cruza el punto de pliegue
            if self.Tf >= self.Tpp:
                q = self.Qtotal
            else:
                q = (self.Ti-self.Tpp)*self.WCp
        else:
            # La corriente no cruza el punto de pliegue
            if self.Ti >= self.Tpp:
                q = self.Qtotal
            else:
                q = (self.Tf-self.Tpp)*self.WCp

        q = round(q, 2)        
        return q if q > 0 else 0
                
    def en_intervalo(self, Ta, Tb):
        """
        Determina si la corriente pasa por el intervalo de temperaturas [Ta, Tb].
        """
        
        if max([self.Ti, self.Tf]) > min([Ta, Tb]):
            if min([self.Ti, self.Tf]) < max([Ta, Tb]):
                return True
        else:
            return False
