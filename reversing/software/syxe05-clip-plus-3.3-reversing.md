# Clip Plus 3.3 - Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## PDF original

Clip Plus 3.3.pdf

---

## Introducción

Análisis del software **Clip Plus 3.3** desde la perspectiva de ingeniería inversa.

El programa se encuentra protegido con **ASProtect 1.23 RC4**, una versión del protector ampliamente utilizada en aplicaciones shareware.

El objetivo del análisis es comprender el funcionamiento del sistema de protección y localizar las rutinas encargadas de verificar el estado de registro del programa.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal

---

## Análisis

Se examina el ejecutable para identificar la presencia del protector **ASProtect** y estudiar el flujo de ejecución antes de alcanzar el código principal del programa.

Durante el análisis se observan:

- inicialización del protector
- ejecución del código previo al OEP
- llamadas internas relacionadas con la verificación de licencia

Mediante el uso de un debugger se identifican comparaciones y saltos condicionales que controlan el comportamiento del programa en modo registrado o modo trial.

---

## Modificación del flujo

Una vez localizada la rutina de validación, se modifica el flujo de ejecución alterando las instrucciones responsables de la verificación.

Esto permite forzar el comportamiento del programa como si estuviera registrado.

---

## Resultado

Tras aplicar las modificaciones necesarias, el programa se ejecuta sin las restricciones del modo trial.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
