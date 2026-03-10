# McAfee VirusScan 5.15.002 - Reversing Tutorial
Autor: SyXe'05  
Categoría: Reversing / Software  

## PDF original
McAfee VirusScan 5.15.002.pdf

---

## Introducción

Este tutorial analiza el programa **McAfee VirusScan 5.15.002** desde el punto de vista de ingeniería inversa.  
El objetivo es comprender cómo funciona su mecanismo de protección o validación interna y cómo puede analizarse mediante herramientas de reversing.

El enfoque del tutorial sigue técnicas clásicas utilizadas en el reversing de software shareware y aplicaciones comerciales.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal
- Conocimientos básicos de reversing

---

## Análisis inicial del ejecutable

El primer paso consiste en examinar el ejecutable para identificar:

- Entry Point del programa
- posibles packers o protecciones
- estructura del archivo PE
- llamadas relevantes a APIs de Windows

Esto permite determinar el comportamiento general del programa antes de iniciar el análisis dinámico.

---

## Análisis dinámico

El programa se ejecuta bajo un debugger para observar:

- flujo de ejecución
- comprobaciones internas
- rutinas relacionadas con la licencia o validación

Durante este proceso se identifican comparaciones y saltos condicionales que controlan el acceso a las funciones completas del programa.

---

## Localización de la rutina de validación

El objetivo es encontrar el punto donde el programa decide si:

- el registro es válido
- el programa debe continuar normalmente
- o debe mostrar un mensaje de restricción

Normalmente esto se identifica mediante:

- comparaciones de registros
- llamadas a funciones de validación
- saltos condicionales.

---

## Modificación del flujo de ejecución

Una vez localizada la rutina de validación, el comportamiento puede modificarse mediante:

- parcheo de instrucciones
- modificación de saltos condicionales
- cambios en comparaciones internas

Estas modificaciones permiten forzar el flujo del programa hacia la ruta de ejecución válida.

---

## Resultado

Tras aplicar las modificaciones adecuadas, el programa puede ejecutarse sin las restricciones impuestas por la comprobación original.

---

## Notas

Este tipo de tutoriales representan ejemplos clásicos de reversing aplicado a software protegido mediante verificaciones simples integradas en el propio código.

---

Repositorio del proyecto:

https://github.com/Show0ne/archivo-syxe05-snat
