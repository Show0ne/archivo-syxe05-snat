# Themida 2.2.6.0 – Unpacking en Visual Basic

Autor: SNAT  
Categoría: Reversing / Unpacking

## PDF original

Themida en Visual Basic.pdf

---

## Introducción

Este tutorial analiza el proceso de **desempaquetado de un ejecutable protegido con Themida 2.2.6.0** en una aplicación desarrollada en **Visual Basic**.

Themida es uno de los protectores comerciales más avanzados para ejecutables Windows y utiliza múltiples técnicas para dificultar la ingeniería inversa, entre ellas:

- Virtualización de código
- Anti-debugging
- Anti-dumping
- Ofuscación del flujo de ejecución
- Protección de la Import Address Table (IAT)

El objetivo del tutorial es comprender el funcionamiento de la protección y recuperar el ejecutable original para su análisis.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

El ejecutable es identificado como protegido mediante:

Themida 2.x

Themida introduce técnicas avanzadas como virtualización de código y comprobaciones anti-debugging que complican el análisis directo del ejecutable.

---

## Análisis

El proceso seguido durante el reversing consiste en:

1. Ejecutar el programa bajo **OllyDbg**.
2. Analizar el stub inicial del protector Themida.
3. Seguir el flujo de ejecución hasta localizar el **Original Entry Point (OEP)**.
4. Identificar las rutinas que restauran el código original en memoria.
5. Realizar un **dump del proceso** desde memoria.
6. Reconstruir la **Import Address Table (IAT)**.

En aplicaciones desarrolladas en Visual Basic, es importante identificar correctamente las estructuras internas del runtime para restaurar correctamente el ejecutable.

---

## Conclusión

Themida es uno de los protectores más complejos utilizados en software comercial. Sin embargo, mediante análisis dinámico y seguimiento del flujo de ejecución es posible localizar el OEP y reconstruir el ejecutable original para continuar el análisis.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
