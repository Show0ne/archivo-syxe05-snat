# System Mechanic Professional 6

Autor: SyXe'05
Tipo: Reversing tutorial
Protección: Sistema de registro / serial
Herramientas: SoftICE, W32Dasm, editor hexadecimal

---

## Introducción

En este tutorial se analiza el sistema de protección utilizado por System Mechanic Professional 6.
El objetivo es comprender cómo el programa valida el registro y localizar la rutina encargada de verificar el serial.

El procedimiento sigue el enfoque clásico de reversing utilizado en muchos programas de principios de los años 2000: localizar la función de validación del serial y estudiar su comportamiento.

---

## Análisis inicial

Primero ejecutamos el programa y abrimos el cuadro de registro.

Introducimos datos aleatorios en los campos de nombre y serial para provocar que el programa ejecute la rutina de validación.

Mientras tanto abrimos el depurador SoftICE para interceptar las funciones utilizadas durante la verificación.

---

## Breakpoints útiles

Para observar cómo el programa procesa los datos introducidos podemos colocar breakpoints en funciones comunes utilizadas para manejar texto y memoria.

Por ejemplo:

bpx GetWindowTextA
bpx lstrcmpA
bpx hmemcpy

Estas funciones suelen utilizarse para:

- obtener el contenido de los campos del formulario
- comparar cadenas
- copiar datos en memoria

Cuando se dispare uno de estos breakpoints podremos seguir el flujo de ejecución.

---

## Localización de la rutina de validación

Una vez interceptada la llamada correspondiente, seguimos la ejecución hasta encontrar el punto donde el programa decide si el serial es válido o no.

Normalmente esto se identifica mediante una comparación seguida de un salto condicional, por ejemplo:

cmp eax, 1
jne bad_serial

Si la comparación falla, el programa salta a la rutina que muestra el mensaje de error.

---

## Posibles enfoques

Existen varias formas de continuar el análisis.

### 1. Parchear la aplicación

Podemos modificar el salto condicional para que el programa acepte cualquier serial.

Por ejemplo:

jne bad_serial

puede cambiarse por:

je bad_serial

o incluso eliminar el salto.

---

### 2. Analizar el algoritmo

Otra opción consiste en estudiar el algoritmo que genera el serial esperado.

Si se consigue entender el proceso completo, es posible desarrollar un keygen que genere seriales válidos para cualquier nombre.

---

## Conclusión

En este tutorial se ha analizado el mecanismo de registro utilizado por System Mechanic Professional 6.

Utilizando herramientas clásicas de reversing como SoftICE y W32Dasm se ha localizado la rutina encargada de validar el serial.

A partir de este punto se pueden aplicar diferentes técnicas:

- parchear el programa
- reconstruir el algoritmo de generación de claves
- desarrollar un generador de seriales

Este tipo de protecciones basadas en serial eran muy comunes en el software de la época y constituyen un buen ejercicio de análisis en ingeniería inversa.

---

Autor: SyXe'05
