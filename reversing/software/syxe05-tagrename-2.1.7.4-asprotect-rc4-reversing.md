# TagRename 2.1.7.4 - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## PDF original

ASProtect_v1.23_RC4_en_TagRename v2.1.7.4__SyXe'05.pdf

---

## Introducción

Análisis del software **TagRename 2.1.7.4** protegido mediante **ASProtect v1.23 RC4** desde la perspectiva de ingeniería inversa.

ASProtect es un protector de ejecutables Win32 utilizado para dificultar el análisis del código mediante técnicas como cifrado del ejecutable, modificación del flujo de ejecución y protección de las tablas de importación.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

El ejecutable es identificado como protegido con:

ASProtect 1.23 RC4

Esta versión del protector introduce cifrado RC4 y múltiples verificaciones internas que dificultan el volcado directo del ejecutable.

---

## Análisis

El proceso seguido para el análisis del ejecutable consiste en:

1. Ejecutar el programa bajo **OllyDbg**.
2. Analizar el stub de protección cargado por ASProtect.
3. Seguir el flujo de ejecución hasta la restauración del código original.
4. Localizar el **Original Entry Point (OEP)**.
5. Realizar un **dump del proceso en memoria**.
6. Reconstruir la **Import Address Table (IAT)**.

Una vez restauradas las importaciones y corregido el ejecutable, el programa puede ejecutarse sin el protector.

---

## Conclusión

ASProtect 1.23 RC4 introduce diversas técnicas de protección que complican el análisis estático del ejecutable.  
Sin embargo, siguiendo el flujo de ejecución en tiempo de ejecución es posible localizar el OEP, reconstruir la IAT y obtener una versión funcional del ejecutable sin protección.

---

Repositorio del proyecto:

https://github.com/Show0ne/archivo-syxe05-snat
