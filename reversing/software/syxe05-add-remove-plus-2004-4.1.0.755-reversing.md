# Add Remove Plus! 2004 v4.1.0.755

Autor: SyXe'05
Tipo: Reversing tutorial
Protección: Serial / registro
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analiza el sistema de registro utilizado por el programa Add Remove Plus! 2004 v4.1.0.755.

El objetivo es localizar la rutina encargada de validar el número de serie introducido por el usuario y comprender cómo se realiza dicha comprobación.

Este tipo de protecciones basadas en serial eran muy habituales en aplicaciones shareware.

---

## Preparación

Instalamos el programa y ejecutamos la aplicación.

Abrimos la ventana de registro e introducimos un nombre y un serial incorrecto para forzar al programa a ejecutar la rutina de validación.

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

Cuando alguno de estos breakpoints se active podremos seguir el flujo de ejecución.

---

## Localización de la rutina de validación

Tras introducir un serial incorrecto el programa ejecutará la rutina encargada de verificar la clave.

Siguiendo el flujo de ejecución encontraremos una comparación seguida de un salto condicional similar a:

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

Comprendiendo el funcionamiento del algoritmo es posible desarrollar un generador de claves que produzca seriales válidos.

---

## Conclusión

En este tutorial se ha analizado el sistema de registro utilizado por Add Remove Plus! 2004 v4.1.0.755.

Utilizando herramientas clásicas de reversing como SoftICE y W32Dasm es posible localizar la rutina encargada de validar el serial.

Este tipo de análisis permite comprender mejor los mecanismos de protección utilizados en aplicaciones shareware.

---

Autor: SyXe'05
