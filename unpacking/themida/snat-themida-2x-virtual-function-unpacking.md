# Desempacando Themida 2.x con Función Virtual – Reversing Tutorial

Autor: SNAT  
Categoría: Unpacking / Themida

## Documento original
Themida en Visual C++.pdf

---

## Introducción

En este tutorial se analiza una técnica para **desempacar ejecutables protegidos con Themida 2.x** cuando la protección utiliza llamadas a **funciones virtuales**.

Themida es uno de los protectores más complejos utilizados en software comercial, incorporando múltiples técnicas de ofuscación y protección contra depuración.

El objetivo del tutorial es identificar el punto en el que el código original del programa vuelve a ejecutarse.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import REConstructor (ImpRec)

---

## Identificación de la protección

El primer paso consiste en analizar el ejecutable con **PEiD** para identificar el protector.

El resultado indica que el binario está protegido por **Themida 2.x**.

---

## Análisis en el depurador

El ejecutable se carga en **OllyDbg**.

Durante la ejecución inicial se observan múltiples capas de código protector diseñadas para:

- detectar depuradores
- ocultar el código real
- redirigir la ejecución mediante funciones virtuales

---

## Localización del OEP

El objetivo principal es localizar el **Original Entry Point (OEP)**.

Para ello se analizan las llamadas indirectas a funciones virtuales que finalmente transfieren el control al código original.

Una vez identificado el punto donde comienza la ejecución del programa real se puede proceder al volcado del ejecutable.

---

## Volcado del ejecutable

Cuando se alcanza el OEP se realiza un **dump de memoria** del proceso.

Posteriormente se reconstruyen las importaciones utilizando **Import REConstructor**.

---

## Verificación

El ejecutable reconstruido se prueba fuera del depurador para confirmar que funciona correctamente sin la capa de protección.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
