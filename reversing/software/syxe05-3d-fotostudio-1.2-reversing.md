# 3D FotoStudio 1.2 - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software  

---

## Introducción

Este tutorial analiza el software **3D FotoStudio 1.2** desde la perspectiva de la ingeniería inversa.
El objetivo es comprender el mecanismo de protección utilizado por la aplicación y estudiar cómo puede
analizarse mediante herramientas clásicas de reversing.

Este tipo de análisis era habitual en la escena de reversing de principios de los años 2000,
utilizando software shareware como laboratorio para estudiar técnicas de protección y validación.

---

## Herramientas utilizadas

Las herramientas empleadas en el análisis suelen incluir:

- Debuggers como **OllyDbg**
- Desensambladores
- Utilidades para analizar ejecutables **PE**
- Herramientas de inspección de llamadas a API

---

## Análisis inicial

El primer paso consiste en examinar el ejecutable para identificar:

- Punto de entrada del programa (Entry Point)
- Estructura del archivo PE
- Posibles packers o protecciones
- Llamadas relevantes a la API de Windows

Este análisis permite comprender cómo se inicializa el programa y qué partes del código
pueden estar relacionadas con el sistema de registro.

---

## Ejecución bajo debugger

El programa se ejecuta dentro de un debugger para observar:

- Flujo de ejecución durante el arranque
- Comparaciones relacionadas con el estado de registro
- Rutinas que controlan restricciones del modo trial

Durante esta fase se buscan instrucciones de comparación (`CMP`) y saltos condicionales
(`JE`, `JNE`, `JNZ`, etc.) que determinan si el programa está registrado.

---

## Localización de la rutina de validación

Analizando el flujo de ejecución se identifica la función encargada de determinar si:

- El programa está registrado
- Debe ejecutarse en modo limitado
- Deben mostrarse mensajes de advertencia

Estas rutinas suelen encontrarse cerca de comparaciones relacionadas con datos
de licencia o valores internos del programa.

---

## Modificación del flujo de ejecución

Una vez localizada la rutina de verificación, el comportamiento del programa puede
alterarse mediante técnicas como:

- Parcheo de saltos condicionales
- Modificación de comparaciones
- Alteración de valores de retorno de funciones

Esto permite redirigir la ejecución hacia el camino correspondiente al modo registrado.

---

## Resultado

Tras aplicar las modificaciones necesarias en el binario, el programa se comporta como
si estuviera correctamente registrado, eliminando las restricciones del modo trial.

---

## Notas

Este tutorial es un ejemplo clásico de reversing aplicado a software shareware,
muy común en los tutoriales de la escena de cracking y reversing de principios
de los 2000.

Repositorio del proyecto:
https://github.com/Show0ne/archivo-syxe05-snat
