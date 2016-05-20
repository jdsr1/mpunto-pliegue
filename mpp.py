#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mpp.py
#  Método de punto de pliegue (Pinch point method) para obtener los servicios
#  mínimos de calentamiento y enfriamiento de un sistema de corrientes.
#

class Corriente(object):
	"""
	Una clase para contener las propiedades de las corrientes.
	"""
	
	def __init__(self, Ti, Tf, WCp):
		self.Ti = float(Ti) #Temperatura inicial
		self.Tf = float(Tf) #Temperatura final
		self.Tpp= 0 		#Temperatura del punto de pliegue
		self.WCp = float(WCp)
		self.cal = Ti > Tf  #Verdadero si la corriente es una corriente caliente

def enIntervalo(c, Ta, Tb):
	"""
	Determina si la corriente 'c' pasa por el intervalo de Temperaturas [Ta, Tb].
	"""
	
	if max([c.Ti, c.Tf]) > min([Ta, Tb]):
		if min([c.Ti, c.Tf]) < max([Ta, Tb]):
			return True
	else:
		return False

def mpp(cc, DTmin=20):
	"""
	Regresa los servicios de calentamiento y enfriamiento mínimos, así como la
	temperatura del punto de pliegue para el sistema formado por las corrientes
	en el vector cc.
	"""

	Temperatura = [] #vector de temperaturas
	
	for c in cc:
		if c.cal == True:
			#Ajuste de temperaturas para corrientes calientes
			c.Ti = c.Ti - DTmin/2.0
			c.Tf = c.Tf - DTmin/2.0
		else:
			#Ajuste de temperaturas para corrientes frías
			c.Ti = c.Ti + DTmin/2.0
			c.Tf = c.Tf + DTmin/2.0
		#Agregar las temperaturas ajustadas al vector de Temperatura,
		#excepto si la temperaturas a agregar ya se encuentra en el vector.
		if c.Ti not in Temperatura: Temperatura.append(c.Ti)
		if c.Tf not in Temperatura: Temperatura.append(c.Tf)
	
	#Ordenar el vector de temperaturas de mayor a menor
	Temperatura.sort(reverse=1)
	
	WCp_int = [] 	#WCp por intervalo
	Q_int = []  	#Q por intervalo
	
	#Determinación del Wcp y Q por intervalo
	i = 1 #intervalo 1
	while i < len(Temperatura):
		WCpi = 0
		for c in cc:
			#sólo considerar aquellas corrientes que están en el intervalo
			if enIntervalo(c, Temperatura[i-1], Temperatura[i]):
				if c.cal == True:
					#si la corriente es una corriente caliente:
					#restar su WCp al WCp del intervalo
					WCpi = WCpi - c.WCp
				else:
					#si la corriente es una corriente fría:
					#sumar su WCp al WCp del intervalo
					WCpi = WCpi + c.WCp
		#calcular calor por intervalo
		Qi = WCpi * (Temperatura[i-1] - Temperatura[i])
		WCp_int.append(WCpi) 	#agregar WCpi al vector de WCp
		Q_int.append(Qi) 		#agregar Qi al vector de Q
		i = i + 1
	
	#Cascada de calor. Mismo tamaño que el vector Temperatura
	cascada = [0] * len(Temperatura)
	#Primera iteración. Suponer que el primer valor en la cascada es 0.
	i = 1
	while i < len(Temperatura):
		cascada[i] = cascada[i-1] - Q_int[i-1]
		i = i + 1
	#Comprobación de la cascada de calor. El valor mínimo debería ser un 0.
	while min(cascada) != 0:
		Qmin = min(cascada)
		i = 0
		while i < len(Temperatura):
			#Restar el valor mínimo a cada elemento del vector cascada.
			cascada[i] = cascada[i] - Qmin
			i = i + 1
	
	pp = cascada.index(0)   #el punto de pliegue es el lugar (índice) donde hay un cero
							#en la cascada de calor. (Este método no considera múltiples
							#puntos de pliegue).
	tpp = Temperatura[pp]	#Temperaturaseratura del punto de pliegue
	smcal = cascada[0]		#servicio mínimo de calentamiento
	smenf = cascada[-1]		#servicio mínimo de enfriamiento
	
	#Impresión de la cascada de calor final
	i = 0
	print "T: ",
	while i < len(Temperatura)-1:
		print Temperatura[i],'->',
		i = i + 1
	print Temperatura[i]
	i = 0
	print "Q: ",
	while i < len(cascada)-1:
		print cascada[i],'->',
		i = i + 1
	print cascada[i]
	
	#Restaurando las temperaturas de las corrientes a sus valores originales.
	#Agregando la temperatura de punto de pliegue a cada corriente.
	for c in cc:
		if c.cal == True:
			c.Tpp = tpp + DTmin/2.0
			c.Ti = c.Ti + DTmin/2.0
			c.Tf = c.Tf + DTmin/2.0
		else:
			c.Tpp = tpp - DTmin/2.0
			c.Ti = c.Ti - DTmin/2.0
			c.Tf = c.Tf - DTmin/2.0
	
	#Regresar la temperatura del punto de pliegue y los servicios mínimos
	return tpp, smcal, smenf

#Ejemplo
c1 = Corriente(250, 100, 0.95)
c2 = Corriente(180, 100, 0.84)
c3 = Corriente(110, 200, 1.00)
c4 = Corriente(110, 230, 0.90)

cc = [c1,c2,c3,c4]
mpp(cc)
