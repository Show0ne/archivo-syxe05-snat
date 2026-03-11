# Primer acercamiento al Stolen Code (Parte 1) - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Protectores / Técnicas

## PDF original

Primer_acercamiento_al_Stolen_Code_parte_1 - [por SyXe'05].pdf

---

## Introducción

Este tutorial introduce una técnica utilizada por algunos protectores y packers conocida como **Stolen Code**.

El objetivo de esta técnica es dificultar el análisis del programa protegido moviendo fragmentos del código original a otra ubicación dentro del ejecutable.  
Esto rompe el flujo esperado de ejecución y complica la reconstrucción del **OEP (Original Entry Point)**.

En este primer tutorial se explica el concepto general y se muestran ejemplos básicos de cómo identificar este comportamiento durante un análisis con debugger.

---

## Concepto de Stolen Code

La técnica consiste en:

1. Copiar instrucciones del programa original.
2. Colocarlas dentro del stub del protector.
3. Redirigir la ejecución hacia ese código desplazado.
4. Volver al flujo original posteriormente.

Esto provoca que:

- El flujo de ejecución aparente sea distinto al original.
- Las primeras instrucciones del programa no correspondan al código real.
- Se complique la reconstrucción del binario original tras el unpacking.

---

## Entorno de análisis

Herramientas utilizadas en el tutorial:

- **OllyDbg**
- **PE Tools**
- **Editor hexadecimal**

Se recomienda ejecutar el programa bajo debugger y observar:

- Cambios en el flujo de ejecución
- Saltos inesperados
- Código ejecutado fuera de las secciones habituales

---

## Identificación del código robado

Durante el análisis pueden observarse varios indicios:

- Instrucciones movidas fuera de su contexto original
- Saltos hacia direcciones inesperadas
- Restauración del flujo original después de ejecutar el stub

Esto se detecta normalmente siguiendo el flujo de ejecución paso a paso con el debugger.

---

## Flujo típico del protector

Un flujo simplificado sería:

1. Entrada en el stub del protector
2. Ejecución de código de inicialización
3. Ejecución del **stolen code**
4. Restauración del contexto
5. Salto al **OEP real**

---

## Objetivo del tutorial

El propósito de este documento es que el reverser:

- Comprenda el concepto de **stolen code**
- Identifique esta técnica en ejecutables protegidos
- Entienda cómo afecta al proceso de unpacking

La segunda parte del tutorial profundiza en la localización del OEP cuando esta técnica está presente.

---

## Parte 2

El análisis continúa en:
