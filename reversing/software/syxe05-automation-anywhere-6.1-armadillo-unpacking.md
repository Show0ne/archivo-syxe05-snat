# Automation Anywhere 6.1 - Armadillo Unpacking Tutorial

Autor: SNAT  
Categoría: Reversing / Unpacking

## PDF original

Automation Anywhere 6.1.pdf

---

## Introducción

Este tutorial analiza el software **Automation Anywhere 6.1**, protegido mediante **Armadillo**, uno de los protectores comerciales de ejecutables más utilizados en aplicaciones Win32.

El objetivo del análisis es comprender el funcionamiento del protector y recuperar el ejecutable original eliminando la capa de protección.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

El ejecutable es identificado como protegido con:

Armadillo

Armadillo introduce múltiples técnicas de protección como:

- Modificación del Entry Point
- Cifrado del código
- Anti-debugging
- Protección de importaciones

---

## Análisis

El proceso seguido durante el reversing consiste en:

1. Ejecutar el programa bajo **OllyDbg**.
2. Analizar el stub de protección de Armadillo.
3. Seguir el flujo de ejecución hasta que el código original es restaurado en memoria.
4. Localizar el **Original Entry Point (OEP)**.
5. Realizar un **dump del proceso** desde memoria.
6. Reconstruir la **Import Address Table (IAT)**.

Una vez reconstruidas las importaciones y reparado el ejecutable, el programa puede ejecutarse sin la capa de protección.

---

## Conclusión

Armadillo implementa varias técnicas destinadas a complicar el análisis estático del ejecutable.

Sin embargo, mediante análisis dinámico y seguimiento del flujo de ejecución es posible localizar el OEP y reconstruir el ejecutable original.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
