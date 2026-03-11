# SVKP v1.3x – Registry Medic (Parte 1) Reversing

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

SVKP_v1.3x_Registry_Medic_parte1.pdf

---

## Introducción

En este tutorial se analiza el software **Registry Medic**, protegido mediante **SVKP v1.3x**.

SVKP (Software Virtual Key Protector) es un protector utilizado en aplicaciones Windows que introduce diversas técnicas de protección diseñadas para dificultar la ingeniería inversa, entre ellas:

- Modificación del flujo de ejecución
- Cifrado del código
- Protección del entry point
- Verificaciones internas de integridad

El objetivo del análisis es comprender cómo funciona el stub del protector y localizar el **Original Entry Point (OEP)** del programa.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

El ejecutable es identificado como protegido mediante:

SVKP v1.3x

Este protector utiliza un stub que controla el flujo inicial del ejecutable antes de transferir la ejecución al código original del programa.

---

## Análisis

El proceso seguido durante el reversing consiste en:

1. Ejecutar el programa bajo **OllyDbg**.
2. Analizar el stub inicial del protector.
3. Seguir el flujo de ejecución hasta identificar la restauración del código original.
4. Localizar el **Original Entry Point (OEP)**.
5. Realizar un **dump del ejecutable desde memoria**.
6. Reconstruir la **Import Address Table (IAT)**.

Durante el análisis se identifican las rutinas responsables de restaurar el código original y transferir el control al programa protegido.

---

## Conclusión

SVKP v1.3x implementa mecanismos de protección destinados a dificultar el análisis estático del ejecutable.  
Sin embargo, mediante análisis dinámico y seguimiento del flujo de ejecución es posible localizar el OEP y reconstruir el ejecutable original.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
