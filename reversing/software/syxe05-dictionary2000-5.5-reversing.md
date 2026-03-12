# Dictionary2000 5.5

Autor: SyXe'05  
Tipo: Reversing tutorial  
Protección: Serial / Shareware  
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analizará el sistema de protección utilizado por **Dictionary2000 5.5**.

Las aplicaciones shareware suelen implementar mecanismos simples de registro basados en la introducción de un nombre y un serial que es validado por el programa.

El objetivo del análisis será localizar la rutina encargada de comprobar la validez del serial introducido por el usuario.

---

## Preparación

Ejecutamos el programa y accedemos al cuadro de registro donde se solicitan los datos de usuario.

Introducimos un nombre y un serial cualquiera con el objetivo de provocar que el programa ejecute la rutina de validación.

Antes de confirmar el registro cargamos **SoftICE** para poder seguir el flujo de ejecución del programa.

---

## Colocación de breakpoints

Una técnica habitual consiste en colocar breakpoints en funciones utilizadas para recuperar el texto introducido por el usuario.

Por ejemplo:

bpx GetWindowTextA

Esta función suele utilizarse para leer el contenido de los campos del formulario de registro.

Cuando se active el breakpoint podremos observar cómo el programa recupera el nombre y el serial introducidos.

---

## Seguimiento de la ejecución

Tras introducir los datos y confirmar el registro, SoftICE interceptará la llamada correspondiente.

A partir de este punto podemos continuar la ejecución paso a paso para observar cómo el programa procesa el serial introducido.

Durante este proceso se localizará la rutina encargada de comprobar si el serial es válido.

---

## Localización de la comprobación

En algún punto del código encontraremos una comparación que determina si el serial introducido coincide con el valor esperado.

Normalmente esta comprobación se realiza mediante instrucciones de comparación seguidas de un salto condicional.

Por ejemplo:

cmp eax, valor_correcto  
jne serial_invalido

Si el serial no coincide con el valor esperado el programa ejecutará la rutina que indica que el serial es incorrecto.

---

## Posibles estrategias

Una vez localizada la rutina de validación existen varias formas de proceder.

### Parchear la aplicación

Podemos modificar el salto condicional para que el programa acepte cualquier serial.

Por ejemplo:

jne serial_invalido

puede convertirse en:

je serial_invalido

o eliminar completamente el salto.

### Analizar el algoritmo

Otra opción consiste en estudiar el algoritmo utilizado para generar el serial válido.

Comprendiendo la lógica utilizada por el programa sería posible desarrollar un generador de claves que produzca seriales válidos.

---

## Conclusión

En este tutorial se ha analizado el sistema de registro utilizado por **Dictionary2000 5.5**.

Utilizando herramientas clásicas de reversing como **SoftICE** y **W32Dasm** es posible localizar la rutina encargada de validar el serial.

Este tipo de análisis permite comprender el funcionamiento de las protecciones simples utilizadas en aplicaciones shareware.

---

Autor: SyXe'05
