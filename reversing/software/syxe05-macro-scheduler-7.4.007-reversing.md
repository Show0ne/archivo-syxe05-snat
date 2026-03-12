# Macro Scheduler 7.4.007

Autor: SyXe'05
Tipo: Reversing tutorial
Protección: Serial / registro
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analiza el sistema de protección utilizado por el programa Macro Scheduler 7.4.007.

El objetivo es localizar la rutina encargada de validar el número de serie introducido por el usuario y comprender el funcionamiento del mecanismo de registro.

Las protecciones basadas en serial eran muy comunes en aplicaciones shareware y constituyen un buen ejercicio de ingeniería inversa.

---

## Preparación

Instalamos el programa y lo ejecutamos.

Abrimos la ventana de registro e introducimos un nombre y un serial incorrecto para provocar que el programa ejecute la rutina de validación.

Antes de confirmar el registro iniciamos el depurador SoftICE.

---

## Breakpoints iniciales

Para observar cómo el programa procesa los datos introducidos colocamos breakpoints en funciones comunes relacionadas con el manejo de texto.

Por ejemplo:

bpx GetWindowTextA
bpx lstrcmpA
bpx hmemcpy

Estas funciones suelen utilizarse para:

- leer el contenido de los campos del formulario
- comparar cadenas
- copiar datos en memoria

Cuando alguno de estos breakpoints se active podremos seguir el flujo de ejecución del programa.

---

## Localización de la rutina de validación

Tras introducir un serial incorrecto el programa ejecutará la rutina encargada de verificar la clave.

Siguiendo la ejecución encontraremos una comparación seguida de un salto condicional similar a:

cmp eax, 1
jne bad_serial

Si la comparación falla el programa saltará a la rutina que muestra el mensaje indicando que el serial es inválido.

---

## Posibles técnicas de bypass

Una vez localizada la rutina de validación existen varias estrategias posibles.

### Parchear la aplicación

Podemos modificar el salto condicional para que el programa acepte cualquier serial.

Por ejemplo:

jne bad_serial

puede cambiarse por:

je bad_serial

o eliminar completamente el salto.

---

### Analizar el algoritmo

Otra alternativa consiste en estudiar el algoritmo utilizado para generar el serial válido.

Comprendiendo el funcionamiento del algoritmo es posible desarrollar un generador de claves que produzca seriales válidos para cualquier nombre.

---

## Conclusión

En este tutorial se ha analizado el sistema de registro utilizado por Macro Scheduler 7.4.007.

Utilizando herramientas clásicas de reversing como SoftICE y W32Dasm es posible localizar la rutina encargada de validar el serial.

Este tipo de análisis permite comprender mejor los mecanismos de protección utilizados en aplicaciones shareware.

---

Autor: SyXe'05
