# PEBundle SWiSHpix – Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## Documento original
PEBundle_SWiSHpix.pdf

---

## Introducción

En este tutorial se analiza **SWiSHpix**, una aplicación empaquetada utilizando **PEBundle**.

PEBundle es una herramienta utilizada para agrupar múltiples archivos dentro de un único ejecutable, lo que complica el análisis directo del programa.

El objetivo del tutorial es identificar el proceso de desempaquetado y recuperar el ejecutable original.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import REConstructor (ImpRec)

---

## Identificación del packer

El ejecutable se analiza inicialmente con **PEiD** para identificar la protección.

El resultado indica que el archivo está empaquetado con **PEBundle**.

---

## Análisis dinámico

El ejecutable se carga en **OllyDbg** para observar el proceso de inicialización del packer.

Durante esta fase se identifican las rutinas encargadas de:

- desempaquetar el código original
- reconstruir la estructura del ejecutable en memoria
- transferir el control al programa real

---

## Localización del OEP

El objetivo principal del análisis es localizar el **Original Entry Point (OEP)**.

Cuando el código desempaquetado está completamente cargado en memoria, el control se transfiere al ejecutable original.

Este punto marca el momento adecuado para realizar el volcado del proceso.

---

## Volcado del ejecutable

Una vez localizado el OEP se realiza un **dump del proceso**.

Posteriormente se reconstruyen las importaciones utilizando **Import REConstructor (ImpRec)**.

---

## Verificación

El ejecutable reconstruido se ejecuta fuera del depurador para confirmar que funciona correctamente sin la capa de empaquetado.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
