# Magic Utilities 2006 v4.22 - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## PDF original

Magic Utilities 2006 v4.22.pdf

---

## Introducción

Este tutorial analiza el software **Magic Utilities 2006 v4.22**, una aplicación de mantenimiento para Windows que incluye herramientas para gestionar programas instalados, procesos activos y aplicaciones que se ejecutan al iniciar el sistema.

El objetivo del análisis es estudiar el mecanismo de verificación de licencia implementado por el programa y comprender cómo el ejecutable determina si se encuentra en modo registrado o en modo de evaluación.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal

---

## Identificación del mecanismo de protección

Durante el análisis del ejecutable se observan rutinas encargadas de verificar el estado de registro del programa.

Estas rutinas suelen ejecutarse durante la inicialización del programa y determinan si el usuario ha introducido un número de serie válido.

El flujo de ejecución incluye comparaciones de valores y saltos condicionales que controlan el comportamiento del programa.

---

## Análisis dinámico

Utilizando **OllyDbg** se sigue la ejecución del programa hasta localizar las instrucciones responsables de la validación de la licencia.

Durante el proceso se identifican:

- comparaciones relacionadas con el estado de registro
- saltos condicionales que determinan el modo de ejecución
- llamadas a funciones internas del programa que verifican el número de serie

El análisis dinámico permite comprender cómo el programa decide si se ejecuta como versión registrada o versión de prueba.

---

## Modificación del flujo de ejecución

Una vez localizada la rutina de verificación, se modifica el flujo de ejecución alterando la instrucción que controla la validación del registro.

Este tipo de modificación permite forzar el comportamiento del programa como si estuviera registrado.

---

## Resultado

Tras aplicar las modificaciones necesarias, el programa se ejecuta sin las limitaciones del modo trial.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
