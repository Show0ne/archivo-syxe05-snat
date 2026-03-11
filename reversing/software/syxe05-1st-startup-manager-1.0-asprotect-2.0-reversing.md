# 1st Startup Manager 1.0 – ASProtect 2.0 Reversing

Autor: SyXe'05
Categoría: Reversing / Software Protection

## PDF original

1st Startup Manager 1.0.pdf

---

## Introducción

Este tutorial analiza el software **1st Startup Manager 1.0**, protegido mediante **ASProtect 2.0 (Registered)**.

ASProtect es un protector de ejecutables Win32 ampliamente utilizado para dificultar la ingeniería inversa mediante múltiples técnicas de protección como cifrado del ejecutable, modificación del flujo de ejecución y mecanismos anti‑debugging.

El objetivo del análisis es comprender el funcionamiento del stub del protector y localizar el **Original Entry Point (OEP)** para recuperar el ejecutable original.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

El ejecutable es identificado como protegido mediante:

ASProtect 2.0 (Registered)

Esta versión del protector introduce mejoras en las rutinas de cifrado del código y verificaciones adicionales de integridad para dificultar el análisis.

---

## Análisis

El proceso de reversing se realiza siguiendo los siguientes pasos:

1. Ejecutar el programa bajo **OllyDbg**.
2. Analizar el stub de carga de ASProtect.
3. Seguir el flujo de ejecución hasta la restauración del código original.
4. Localizar el **Original Entry Point (OEP)**.
5. Realizar un **dump del proceso en memoria**.
6. Reconstruir la **Import Address Table (IAT)**.

Una vez reconstruida la IAT y corregido el ejecutable, el programa puede ejecutarse sin la capa de protección.

---

## Conclusión

ASProtect 2.0 introduce varias capas de protección diseñadas para dificultar el análisis estático del ejecutable. Sin embargo, mediante análisis dinámico y seguimiento del flujo de ejecución es posible localizar el OEP y reconstruir el ejecutable original.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
