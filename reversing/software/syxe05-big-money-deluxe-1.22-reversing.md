# Big Money Deluxe v1.22 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
WinBM.pdf

---

## Introducción

En este tutorial se analiza **Big Money Deluxe v1.22**, un juego casual
de gestión financiera para Windows.

El objetivo del análisis consiste en localizar la rutina responsable
de verificar el estado de registro del programa y comprender el
mecanismo utilizado para validar el número de serie.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

Se analiza el ejecutable con **PEiD** para comprobar si el binario está
empaquetado mediante algún packer.

El análisis muestra que el ejecutable puede cargarse directamente en
el depurador sin necesidad de desempaquetado.

---

## Análisis dinámico

El programa se ejecuta bajo **OllyDbg** para observar el proceso de
validación del serial.

Durante el análisis se buscan:

- mensajes de versión trial
- cadenas relacionadas con el registro
- funciones que procesen el número de serie

Estas referencias ayudan a localizar la rutina responsable de la
verificación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la función que compara
el número de serie introducido con el valor esperado.

En el código aparecen instrucciones típicas como:

CMP
TEST
JE
JNE

Estas instrucciones controlan el flujo dependiendo del resultado de la
comparación.

---

## Modificación del flujo

Una vez localizada la verificación principal se puede modificar el flujo
de ejecución para forzar la ruta válida:

- invertir el salto condicional
- modificar la comparación
- forzar el valor de retorno de la función

---

## Verificación

Tras aplicar el parche se ejecuta el programa fuera del depurador para
confirmar que funciona correctamente como versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
