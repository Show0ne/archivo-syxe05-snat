# File Recover 5.0.1.15 – Armadillo 3.78 Unpacking

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

Armadillo_3.78_File_Recover_5.0.1.15.pdf

---

## Introducción

En este tutorial se analiza el software **File Recover 5.0.1.15**, protegido mediante **Armadillo 3.78**, uno de los protectores comerciales de ejecutables más utilizados en aplicaciones Win32 durante los años 2000.

Armadillo introduce múltiples mecanismos diseñados para dificultar la ingeniería inversa, incluyendo:

- Modificación del **Entry Point**
- Cifrado del código del ejecutable
- Técnicas de **anti‑debugging**
- Protección de la **Import Address Table (IAT)**
- Rutinas de verificación internas

El objetivo del análisis es comprender el funcionamiento del stub del protector y recuperar el ejecutable original eliminando la capa de protección.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

El ejecutable es identificado mediante herramientas de detección como protegido con:

Armadillo 3.78

Esta versión del protector introduce mejoras respecto a versiones anteriores, especialmente en el manejo del cifrado del código y las comprobaciones internas de integridad.

---

## Estrategia de análisis

El proceso de reversing se realiza mediante análisis dinámico:

1. Ejecutar el programa bajo **OllyDbg**.
2. Analizar el stub de carga del protector Armadillo.
3. Seguir el flujo de ejecución hasta que el código original se restaure en memoria.
4. Identificar el **Original Entry Point (OEP)**.
5. Realizar un **dump del proceso en memoria**.
6. Reconstruir la **Import Address Table (IAT)**.

Una vez reconstruida la IAT y corregido el dump, el ejecutable puede ejecutarse sin la capa de protección.

---

## Conclusión

Armadillo 3.78 implementa varias técnicas de protección destinadas a complicar el análisis estático del ejecutable.

Sin embargo, mediante análisis dinámico y seguimiento del flujo de ejecución es posible localizar el OEP, reconstruir el ejecutable original y continuar el análisis del programa sin protección.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
