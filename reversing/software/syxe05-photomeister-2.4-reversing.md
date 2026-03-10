# PhotoMeister 2.4 - Reversing Tutorial
Autor: SyXe'05  
Categoría: Reversing / Software  

## PDF original
PhotoMeister2.4.pdf

---

## Introducción

Este tutorial analiza el programa **PhotoMeister 2.4** desde la perspectiva de la ingeniería inversa.  
El objetivo es estudiar el mecanismo de protección o validación utilizado por el software y comprender cómo puede analizarse utilizando herramientas clásicas de reversing.

El enfoque sigue técnicas habituales empleadas en el análisis de software shareware.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal
- Conocimientos básicos de reversing

---

## Análisis inicial

El primer paso consiste en examinar el ejecutable para identificar:

- Entry Point del programa
- estructura del archivo PE
- posibles packers o protecciones
- llamadas relevantes a APIs

Este análisis preliminar permite entender cómo arranca el programa.

---

## Ejecución bajo debugger

El programa se ejecuta bajo un debugger para observar:

- flujo de ejecución
- llamadas a funciones internas
- comportamiento durante la validación del programa

Durante esta fase se buscan comparaciones y saltos condicionales relacionados con la verificación del software.

---

## Localización de la rutina de validación

El objetivo principal es localizar la función que determina si el programa:

- está registrado
- está ejecutándose en modo limitado
- debe mostrar mensajes de restricción

Esto suele encontrarse analizando comparaciones y saltos condicionales dentro del código.

---

## Modificación del flujo de ejecución

Una vez localizada la rutina de validación, el comportamiento del programa puede modificarse mediante:

- parcheo de instrucciones
- modificación de saltos condicionales
- alteración de comparaciones

Estas técnicas permiten forzar el flujo de ejecución hacia el camino válido.

---

## Resultado

Después de aplicar las modificaciones adecuadas, el programa puede ejecutarse sin las limitaciones impuestas por el mecanismo original de validación.

---

## Notas

Este tipo de tutoriales son ejemplos clásicos de reversing aplicado a software shareware de principios de los 2000.

---

Repositorio del proyecto:

https://github.com/Show0ne/archivo-syxe05-snat
