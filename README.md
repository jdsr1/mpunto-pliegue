# Método de punto de pliegue

**Última actualización:** Mayo 29, 2016

Método para obtener los servicios de calentamiento y enfriamiento mínimos
necesarios para integrar completamente un sistema de corrientes.

En esta variante del método la mitad del delta T mínimo (10 grados) se resta a
las temperaturas de las corrientes calientes y se suma a las temperaturas de las
corrientes frías.

Una vez se haya ejecutado la función `mpunto_pliegue()`, puede usarse la función
`diagrama_corrientes()` para visualizar las corrientes en un diagrama que indica
sus temperaturas de origen y finales, así como el punto de pliegue correspondiente 
a las corrientes frías y calientes. Esta función también muestra las cargas
térmicas arriba y debajo del punto de pliegue para cada corriente.

![Diagrama de corrientes](../assets/diagrama_de_corrientes.png?raw=true)

Las curvas compuestas también pueden ser graficadas:

![Curvas compuestas](../assets/curvas_compuestas.png?raw=true)

Más información sobre el método en
[este enlace](https://es.wikipedia.org/wiki/An%C3%A1lisis_Pinch).
