# Método del punto de pliegue
*Pinch-point method*

Método para obtener los servicios de calentamiento y enfriamiento mínimos
necesarios para integrar completamente un sistema de corrientes.

El delta T mínimo por default es de 10 grados, que en esta variante del método
se resta (la mitad) a las temperaturas de las corrientes calientes a la vez que
se suma (también la mitad) a las temperaturas de las corrientes frías.

Sintaxis de la función principal:

`>> mpp(vectorDeCorrientes) #DTmin = 10 por default`

`>> mpp(vectorDeCorrientes, DTmin)`

Una vez se haya ejecutado la función `mpp()`, puede usarse la función `ddc()`
para visualizar las corrientes en un diagrama que indica sus temperaturas de 
origen y finales, así como el punto de pliegue correspondiente a las corrientes
frías y calientes.

Sintaxis de la función `ddc()`:

`>> ddc(vectorDeCorrientes)`
