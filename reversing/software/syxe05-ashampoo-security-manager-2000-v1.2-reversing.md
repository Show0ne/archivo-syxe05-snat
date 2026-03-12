# Ashampoo Security Manager 2000 v1.2

Autor: SyXe'05
Tipo: Reversing tutorial
Protección: Serial / registro
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analiza el sistema de registro utilizado por el programa Ashampoo Security Manager 2000 v1.2.

El objetivo es comprender cómo la aplicación valida el número de serie introducido por el usuario y localizar la rutina responsable de dicha verificación.

Este tipo de protecciones basadas en serial eran extremadamente comunes en el software shareware de principios de los años 2000.

---

## Preparación del análisis

Primero instalamos el programa y ejecutamos la aplicación.

Abrimos la ventana de registro e introducimos un nombre cualquiera junto con un serial incorrecto para forzar al programa a ejecutar la rutina de validación.

Antes de confirmar el registro iniciamos el depurador SoftICE.

---

## Breakpoints iniciales

Para observar cómo el programa procesa la información introducida podemos colocar breakpoints en funciones típicas de manejo de cadenas.

Por ejemplo:

bpx GetWindowTextA
bpx lstrcmpA
bpx hmemcpy

Estas funciones suelen utilizarse para:

- obtener el texto introducido en los campos del formulario
- comparar cadenas
- copiar datos en memoria

Cuando alguno de estos breakpoints se active podremos seguir el flujo de ejecución del programa.

---

## Análisis de la validación

Tras introducir datos incorrectos en el formulario de registro el programa ejecutará la rutina encargada de verificar el serial.

Siguiendo la ejecución podremos localizar una comparación que determina si el serial introducido es válido.

Un ejemplo típico sería:

cmp eax, 1
jne bad_serial

Si el resultado de la comparación no coincide con el valor esperado el programa saltará a la rutina que muestra el mensaje de error.

---

## Posibles técnicas de bypass

Una vez localizada la rutina de validación existen varias estrategias posibles.

### Parchear la comprobación

Podemos modificar el salto condicional para que el programa acepte cualquier serial.

Por ejemplo:

jne bad_serial

puede convertirse en:

je bad_serial

o incluso eliminar completamente el salto.

---

### Analizar el algoritmo de generación

Otra opción consiste en estudiar el algoritmo que genera el serial esperado.

Comprendiendo la lógica utilizada por el programa es posible crear un generador de claves que produzca seriales válidos.

---

## Conclusión

En este tutorial se ha analizado el sistema de registro del programa Ashampoo Security Manager 2000 v1.2.

Utilizando herramientas clásicas de reversing como SoftICE y W32Dasm se ha localizado la rutina encargada de validar el serial.

Una vez identificada dicha rutina es posible:

- parchear la aplicación
- comprender el algoritmo de generación de claves
- desarrollar un keygen

Este tipo de ejercicios resulta muy útil para comprender cómo funcionan las protecciones simples utilizadas en software shareware.

---

Autor: SyXe'05
