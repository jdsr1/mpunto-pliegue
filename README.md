# Método de punto de pliegue

**Última actualización:** Mayo 25, 2016

Método para obtener los servicios de calentamiento y enfriamiento mínimos
necesarios para integrar completamente un sistema de corrientes.

El delta T mínimo por default es de 20 grados, que en esta variante del método
se resta (la mitad) a las temperaturas de las corrientes calientes a la vez que
se suma (también la mitad) a las temperaturas de las corrientes frías.

Una vez se haya ejecutado la función `mpunto_pliegue()`, puede usarse la función
`diagrama_corrientes()` para visualizar las corrientes en un diagrama que indica
sus temperaturas de origen y finales, así como el punto de pliegue correspondiente 
a las corrientes frías y calientes.

---
**Requerimientos:** Python 2.7, matplotlib y numpy.
