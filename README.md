# Método del punto de pliegue
# Pinch-point method

Método para obtener los servicios de calentamiento y enfriamiento mínimos
necesarios para integrar completamente un sistema de corrientes.

El delta T mínimo por default es de 10 grados, que en esta variante del método
se resta (la mitad) a las temperaturas de las corrientes calientes a la vez que
se suma (también la mitad) a las temperaturas de las corrientes frías.

Sintaxis de la función principal:

`>> mpp(vectorDeCorrientes) #DTmin = 10 por default`

`>> mpp(vectorDeCorrientes, DTmin)`

También se define la función `diaCc()`, útil para visualizar las corrientes
en un gráfico, una vez se ha ajustado la propiedad Tpp de cada corriente.
