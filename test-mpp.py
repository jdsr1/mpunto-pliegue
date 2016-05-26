#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# main-mpp.py
# JuanDiego.SR92@gmail.com
# ------------------------------------------------------------------------------
# Archivo de prueba.
# ------------------------------------------------------------------------------

from mppliegue import mpunto_pliegue as mpp
from mppliegue import diagrama_corrientes as ddc
from corriente import Corriente

# Definición del problema
c1 = Corriente(353, 313, 9.802)
c2 = Corriente(347, 246, 2.931)
c3 = Corriente(255,  80, 6.161)
c4 = Corriente(224, 340, 7.179)
c5 = Corriente(116, 303, 0.641)
c6 = Corriente( 53, 113, 7.627)
c7 = Corriente( 40, 293, 1.690)

cc = [c1,c2,c3,c4,c5,c6,c7]
print mpp(cc)
ddc(cc)
