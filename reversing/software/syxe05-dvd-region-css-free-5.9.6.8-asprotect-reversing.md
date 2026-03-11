# DVD Region+CSS Free 5.9.6.8 - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## PDF original

DVD Region+CSS Free 5.9.6.8.pdf

---

## Introducción

En este tutorial se analiza el software **DVD Region+CSS Free 5.9.6.8**, protegido mediante **ASProtect 1.2x – 1.3x (Registered)**.

ASProtect es un sistema de protección de ejecutables Win32 diseñado para dificultar la ingeniería inversa mediante técnicas de cifrado, modificación del flujo de ejecución y verificación de integridad.

El objetivo del análisis es comprender cómo funciona el stub de protección y recuperar el ejecutable original eliminando la capa de protección.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

El ejecutable es identificado mediante herramientas de detección como protegido con:

ASProtect 1.2x – 1.3x (Registered)

Esta versión del protector introduce mecanismos adicionales para ocultar el flujo de ejecución original y dificultar la reconstrucción de las importaciones.

---

## Análisis

El proceso de análisis consiste en:

1. Ejecutar el programa bajo **OllyDbg**.
2. Seguir el flujo de ejecución del stub de ASProtect.
3. Identificar el punto donde se restauran los **stolen bytes**.
4. Localizar el **Original Entry Point (OEP)**.
5. Realizar un **dump del ejecutable desde memoria**.
6. Reconstruir la **Import Address Table (IAT)**.

Una vez reconstruida la IAT y corregido el ejecutable, el programa puede ejecutarse sin la protección.

---

## Conclusión

ASProtect 1.2x–1.3x introduce varias capas de protección que dificultan el análisis estático del ejecutable.

Sin embargo, mediante análisis dinámico es posible seguir el flujo del stub de protección, localizar el OEP y reconstruir el ejecutable original.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
