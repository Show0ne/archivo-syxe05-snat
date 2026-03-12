# Cinematograph 2.1.3.0

Autor: SyXe'05
Tipo: Reversing tutorial
Protección: Registro / Serial
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analiza el sistema de registro utilizado por el programa Cinematograph 2.1.3.0.

El objetivo del análisis es localizar la rutina encargada de validar el número de serie introducido por el usuario y comprender cómo se realiza dicha verificación.

Este tipo de protecciones basadas en serial eran muy habituales en aplicaciones shareware de principios de los años 2000.

---

## Preparación

Instalamos y ejecutamos el programa.

Abrimos la ventana de registro e introducimos un nombre y un serial cualquiera para provocar que el programa ejecute la rutina de validación.

Antes de confirmar el registro iniciamos el depurador SoftICE.

---

## Breakpoints iniciales

Para observar el comportamiento del programa colocamos breakpoints en funciones comunes utilizadas para manejar texto.

Por ejemplo:

bpx GetWindowTextA
bpx lstrcmpA
bpx hmemcpy

Estas funciones suelen utilizarse para:

- obtener el contenido de los campos del formulario
- comparar cadenas
- copiar datos en memoria

Cuando alguno de estos breakpoints se active podremos seguir el flujo de ejecución.

---

## Localización de la rutina de validación

Tras introducir un serial incorrecto el programa ejecutará la rutina encargada de verificar la clave.

Siguiendo la ejecución encontramos una comparación seguida de un salto condicional similar a:

cmp eax, 1
jne bad_serial

Si la comparación falla el programa salta a la rutina que muestra el mensaje indicando que el serial es inválido.

---

## Posibles técnicas de bypass

Una vez localizada la rutina de validación existen varias posibilidades.

### Parchear la aplicación

Podemos modificar el salto condicional para que el programa acepte cualquier serial.

Por ejemplo:

jne bad_serial

puede cambiarse por:

je bad_serial

o eliminar completamente el salto.

---

### Analizar el algoritmo

Otra posibilidad consiste en estudiar el algoritmo que genera el serial válido.

Comprendiendo el funcionamiento del algoritmo es posible desarrollar un generador de seriales que produzca claves válidas.

---

## Conclusión

En este tutorial se ha analizado el sistema de registro utilizado por Cinematograph 2.1.3.0.

Utilizando herramientas clásicas de reversing como SoftICE y W32Dasm es posible localizar la rutina de validación del serial y comprender su funcionamiento.

Este tipo de análisis resulta muy útil para entender los mecanismos de protección utilizados en software shareware.

---

Autor: SyXe'05
