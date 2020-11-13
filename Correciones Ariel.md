# Correciones Ariel

- Agregar una explicación sobre los juegos matriciales conocidos en el capítulo 3.
  - esto sería ejemplos clásicos como dilema del prisionero, coordinacion simetrica, etc?

- / Cambiar los ^t por ^k en los índices, para no confundir con la transposición, sobre todo en la sección 4, porque quizá necesitemos usar la transpuesta.

- La equivalencia (quizá mejor un lema y no un teorema) dudo que sea para demostrar con inducción. Quizá calculando directamente x^(k+1), y^(k+1). Y, de acuerdo a como está escrito todo, parece que debería formularse desde k=0 en vez de 1. Quizá separar en casos (k=0 y k>0).
  - k = 0 no es una iteracion. es (0, 0) por definicion y como que da las condiciones iniciales (todas las acciones estan en el conjunto mejor respuesta (si, esta esta bueno para aclararlo en la tesis))

- En un lado dice teorema de desempate, debería ser hipótesis de desempate.
  - No encontre esto. Se habla de regla de desempate.

- Dar más explicación sobre el tamaño en bits de un juego como entrada. Aprovechar para discutir el hecho de que si se diera una entrada en forma extensiva (árbol) quizá ocuparía menos espacio.
  - lo dejo para despues

- / En la def. de suma cero dice "una de estas matrices", mejor decir "la matriz A".

- / En la def. de degenerado, dice existen i,i', agregar "con $i \neq i$'", y lo mismo para j,j'.

- En la def. 3.3.0.1, en FP simultáneo ver si mencionar la pertenencia a NxM sólo para i1, j1, o bien decirlo para todos, y en ese caso en FP alternante habría que poner también que son de NxM.
  - poner que el primero es arbitrario

- En la def. 3.3.0.2 se habla de que los vectores son números reales, pero al final serán naturales. Ver si no conviene decirlo en forma más precisa.

- Al comparar SFP con AFP, agregar alguna observación acerca de que las secuencias de AFP no son sólo un shift de la de SFP (es decir no es algo trivial), y que eso puede verse en los ejemplos de los teo. 1 y 2.

- / En el teo. 4.2.1, aunque parece claro mejor decir que el equilibrio de Nash es puro.

- / En el teo. de 2x3 para AFP, donde dice (a2,a3) debería decir (a2,b3) (ocurre en dos lugares y en otro lugar parte con "el jugador columna").

- Ver si no será mejor enunciar el teorema de 2x3 generalizado a 2xn, poniendo nros. chicos en las otras celdas irrelevantes. Para hablar..
  - Son subconjunto, pero dado que es el resultado de Berger, sí, puede ser...

- Ese mismo teorema y el de 3x3, en vez de epsilon = 2^-k, casi me animaría a enunciarlos en forma más general tomando epsilon = b^(-k) con b>1, reemplazando el 2 por b en las demostraciones.
  - El 2 me parece que esta para que sea mas evidente la codificacion en bits.

- Casi todas las fórmulas tienen número a la derecha. Si se puede, sería mejor dejar los números de aquellas a las que el texto se refiera.
  - Esto es porque voy aprendiendo a escribir LaTex sobre la marcha, jeje.

- Para ganar tiempo, corregir typos mientras se va editando. Ej., "suma zero" -> suma cero, y otros... En la def. 3.3.6.2 separar la palabra donde de vi y de vj.
  - De nuevo, aprendiendo LaTex.

- No pensar que es sólo un paper con espacio limitado. Explayarse más en general. No ahorrar explicaciones, ejemplos e introducción.
  - Correcto.

- i \in 1..N
- usar tau para tiempo?
- el maximo no cambia con el escalado
- es lema
- en principio hacer tambien para alternante y ver. si quedan una fotocopia lo saco y le pongo que es analogo
- teorema de estabilidad:
  - tambien para alternante
- en los contraejemplos se busca cuanto mas chico mejor y se entiende que es extendible a juegos mas grandes
- non-degenerate de intereses identicos
- tightness para alternantes
- llavesitas de conjuntos para N y M