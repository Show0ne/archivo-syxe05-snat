# Themida 2.3.9.0 – VBA Password Remover

Autor: SNAT & Apuromafo
Categoría: Reversing / VBA / Themida

## Documento original

Themida 2.3.9.0 Vba Password Remover por Snat & Apuromafo.pdf

---

## Introducción

Este tutorial describe el proceso de análisis de una herramienta protegida con **Themida 2.3.9.0** cuyo objetivo es eliminar contraseñas de proyectos **VBA (Visual Basic for Applications)**.

Themida es uno de los protectores más complejos utilizados en software comercial. Introduce múltiples técnicas anti-debug, virtualización de código y mecanismos de protección diseñados para dificultar la ingeniería inversa.

El objetivo del análisis es comprender el funcionamiento de la protección y localizar las rutinas relevantes dentro del ejecutable.

---

## Herramientas utilizadas

- OllyDbg
- Themida unpacking techniques
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación del protector

El primer paso consiste en identificar el protector utilizado por el ejecutable.

Herramientas como **PEiD** o análisis manual del encabezado PE permiten detectar la presencia de **Themida**.

Las características típicas incluyen:

- código altamente ofuscado
- presencia de anti-debug
- saltos indirectos
- código virtualizado

---

## Técnicas de anti-debug

Themida utiliza diversas técnicas para impedir el análisis con depuradores:

- detección de breakpoints
- verificación de flags del sistema
- comprobaciones del entorno de depuración

Durante el análisis es necesario neutralizar o evitar estas protecciones para continuar el estudio del programa.

---

## Análisis dinámico

El ejecutable se carga en **OllyDbg** y se analiza paso a paso.

El objetivo es localizar el momento en el que:

- finaliza la rutina de protección
- el programa transfiere el control al código real

Este punto suele corresponder al **Original Entry Point (OEP)**.

---

## Localización del OEP

Una vez alcanzado el OEP es posible realizar un **dump del ejecutable desde memoria**.

Esto permite obtener una versión del programa con gran parte de la protección eliminada.

---

## Reparación de la IAT

Después del dump es necesario reconstruir la **Import Address Table (IAT)**.

Para ello se utiliza **Import Reconstructor (ImpREC)**.

El proceso incluye:

1. detectar las importaciones
2. reconstruir la tabla
3. guardar el ejecutable reparado

---

## Análisis del funcionamiento

Una vez eliminado el protector principal se puede analizar el funcionamiento interno del programa.

En este caso el software se encarga de eliminar contraseñas de proyectos **VBA**, permitiendo acceder al código protegido dentro de documentos de Office.

---

## Conclusión

Themida representa uno de los sistemas de protección más complejos utilizados en software comercial.

Mediante técnicas de análisis dinámico, localización del OEP y reconstrucción del ejecutable es posible superar la protección y estudiar el funcionamiento real del programa.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
