# ASProtect v1.23 RC4 Registered - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

ASProtect v1.23 RC4 Registered__por_SyXe'05.pdf

---

## Introducción

Este tutorial analiza el funcionamiento interno de **ASProtect v1.23 RC4 (Registered)**, uno de los protectores de ejecutables Win32 más utilizados durante los años 2000.

ASProtect implementa diversas técnicas de protección destinadas a dificultar la ingeniería inversa, incluyendo:

- Alteración del **Entry Point**
- Inserción de **stolen bytes**
- Cifrado del código mediante **RC4**
- Comprobaciones anti-debugging
- Protección de la **Import Address Table (IAT)**

El objetivo del análisis es comprender el flujo del protector y recuperar el ejecutable original sin la capa de protección.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

El ejecutable es identificado mediante herramientas de detección como protegido con:

ASProtect 1.23 RC4 (Registered)

Esta versión añade mejoras respecto a versiones anteriores, especialmente en la gestión del cifrado y las verificaciones internas.

---

## Estrategia de análisis

El proceso de reversing se realiza siguiendo estos pasos:

1. Ejecutar el programa bajo **OllyDbg**.
2. Analizar el stub de carga del protector.
3. Seguir el flujo de ejecución hasta que se restaure el código original.
4. Identificar el **Original Entry Point (OEP)**.
5. Realizar un **dump del proceso en memoria**.
6. Reconstruir la **Import Address Table (IAT)**.

Una vez completados estos pasos, el ejecutable puede ejecutarse sin la capa de protección de ASProtect.

---

## Conclusión

ASProtect 1.23 RC4 es una protección relativamente robusta para su época, pero el seguimiento dinámico del flujo de ejecución permite localizar el OEP y reconstruir el ejecutable original.

La restauración de los stolen bytes y la reconstrucción correcta de la IAT son elementos clave para completar el proceso de unpacking.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
