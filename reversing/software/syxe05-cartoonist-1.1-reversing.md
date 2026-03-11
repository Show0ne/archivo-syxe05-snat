# Cartoonist 1.1 - Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## PDF original

Cartoonist 1.1.pdf

---

## Introducción

Análisis del software **Cartoonist 1.1** desde la perspectiva de ingeniería inversa.

El programa utiliza **ASProtect 1.1c** como sistema de protección, uno de los protectores más comunes en software shareware de principios de los años 2000.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal

---

## Análisis

Se examina el ejecutable para identificar la presencia del protector **ASProtect** y comprender el flujo de ejecución antes de alcanzar el código principal del programa.

Durante el análisis se observan:

- inicialización del protector
- ejecución del código previo al OEP
- rutinas encargadas de verificar el estado de registro

Mediante el uso de un debugger se identifican comparaciones y saltos condicionales que controlan el comportamiento del programa en modo registrado o modo trial.

---

## Modificación del flujo

Una vez localizada la rutina de validación, se modifica el flujo de ejecución alterando las instrucciones responsables de la verificación.

Esto permite forzar el comportamiento del programa como si estuviera registrado.

---

## Resultado

Tras aplicar las modificaciones necesarias, el programa se ejecuta sin las limitaciones del modo trial.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
