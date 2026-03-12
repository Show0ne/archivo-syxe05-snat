# CD-R Diagnostic 0.1.2.0

Autor: SyXe'05  
Tipo: Reversing tutorial  
Protección: Serial / Shareware  
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analizará el sistema de protección utilizado por el programa **CD-R Diagnostic 0.1.2.0**.

Este tipo de aplicaciones shareware suelen implementar mecanismos simples de registro basados en la validación de un serial introducido por el usuario.

El objetivo del análisis será localizar la rutina encargada de validar el serial para comprender el funcionamiento del sistema de protección.

---

## Preparación

Ejecutamos el programa y accedemos al cuadro de registro donde se solicita el nombre y el serial.

Introducimos datos arbitrarios con el objetivo de provocar que el programa ejecute la rutina de validación del serial.

Antes de confirmar el registro cargamos **SoftICE** para poder interceptar el flujo de ejecución.

---

## Colocación de breakpoints

Un método habitual consiste en colocar breakpoints en funciones utilizadas para obtener el texto introducido por el usuario.

Por ejemplo:

bpx GetWindowTextA

Esta función suele utilizarse para leer el contenido de los campos del formulario de registro.

Cuando se active el breakpoint podremos observar cómo el programa procesa el nombre y el serial introducidos.

---

## Seguimiento de la validación

Tras introducir un nombre y un serial cualquiera pulsamos el botón de registro.

SoftICE interceptará la llamada a la función monitorizada y podremos seguir la ejecución paso a paso.

A partir de este punto es posible observar cómo el programa compara el serial introducido con el valor esperado.

---

## Localización de la comprobación

Durante el análisis encontraremos una comparación que determina si el serial introducido es válido.

Normalmente esta comprobación se implementa mediante instrucciones de comparación seguidas de un salto condicional.

Por ejemplo:

cmp eax, valor_correcto  
jne serial_invalido

Si el serial no coincide con el valor esperado el programa ejecutará la rama correspondiente al error.

---

## Posibles estrategias

Una vez localizada la rutina de validación existen varias estrategias posibles.

### Parchear la aplicación

Podemos modificar el salto condicional para que el programa acepte cualquier serial.

Por ejemplo:

jne serial_invalido

puede convertirse en:

je serial_invalido

o eliminar completamente el salto.

### Analizar el algoritmo

Otra opción consiste en estudiar el algoritmo utilizado para generar el serial válido.

Comprendiendo el funcionamiento del algoritmo sería posible desarrollar un generador de claves que produzca seriales válidos.

---

## Conclusión

En este tutorial se ha analizado el sistema de registro utilizado por **CD-R Diagnostic 0.1.2.0**.

Utilizando herramientas clásicas de reversing como **SoftICE** y **W32Dasm** es posible localizar la rutina encargada de validar el serial.

Este tipo de análisis permite comprender cómo funcionan las protecciones simples utilizadas en aplicaciones shareware.

---

Autor: SyXe'05
