# Ace Screensaver 2.40 - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software  

---

## Introducción

Este tutorial analiza el programa **Ace Screensaver 2.40** desde la perspectiva de la ingeniería inversa.
El objetivo es estudiar el mecanismo de protección utilizado por el software y comprender cómo se
verifica el estado de registro del programa.

Este tipo de ejercicios era habitual en la escena de reversing de principios de los años 2000,
donde aplicaciones shareware se utilizaban como entorno de aprendizaje para analizar
mecanismos de protección y validación.

---

## Herramientas utilizadas

Durante el análisis se emplean herramientas clásicas de reversing:

- OllyDbg
- Desensambladores
- Herramientas de análisis de ejecutables PE
- Monitorización de llamadas a la API de Windows

---

## Análisis inicial

El primer paso consiste en examinar el ejecutable para identificar:

- Entry Point del programa
- estructura del archivo PE
- posibles packers o protecciones
- llamadas relevantes a APIs del sistema

Este análisis inicial permite comprender cómo se inicia el programa
y qué partes del código pueden estar relacionadas con la verificación
del estado de registro.

---

## Ejecución bajo debugger

El programa se ejecuta dentro de un debugger para observar:

- flujo de ejecución durante el arranque
- comparaciones relacionadas con el estado de registro
- comportamiento del programa en modo trial

Durante esta fase se buscan instrucciones de comparación (CMP)
y saltos condicionales (JE, JNE, JNZ) que determinan si el programa
se encuentra registrado.

---

## Localización de la rutina de validación

Analizando el flujo de ejecución se identifica la función responsable de:

- verificar si el software está registrado
- habilitar o deshabilitar funcionalidades
- mostrar mensajes de limitación

Estas rutinas suelen encontrarse cerca de comparaciones o llamadas
a funciones internas relacionadas con el sistema de licencia.

---

## Modificación del flujo de ejecución

Una vez localizada la rutina de verificación, el comportamiento del
programa puede modificarse mediante:

- parcheo de saltos condicionales
- modificación de comparaciones
- alteración del valor de retorno de funciones internas

Esto permite redirigir el flujo de ejecución hacia el camino
correspondiente al modo registrado.

---

## Resultado

Tras aplicar las modificaciones adecuadas, el programa se ejecuta
como si estuviera registrado, eliminando las restricciones del
modo trial.

---

## Notas

Este tipo de tutoriales representan ejemplos clásicos de reversing
aplicado a software shareware, característicos de la escena de
ingeniería inversa de principios de los años 2000.

Repositorio del proyecto:
https://github.com/Show0ne/archivo-syxe05-snat
