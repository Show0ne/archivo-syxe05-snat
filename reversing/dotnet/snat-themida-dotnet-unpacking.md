# Desempacando Themida en un .NET

Autor: SNAT  
Categoría: Reversing / .NET / Unpacking

## PDF original

Themida en .NET.pdf

---

## Introducción

Este documento analiza un ejecutable **.NET protegido con Themida**.

Themida es uno de los protectores comerciales más conocidos y complejos utilizados para proteger software contra ingeniería inversa.  
Cuando se aplica a aplicaciones **.NET**, introduce capas adicionales de protección diseñadas para dificultar el análisis del ensamblado.

El objetivo del análisis es comprender cómo funciona el protector y recuperar el ensamblado original para poder analizarlo con herramientas de reversing.

---

## Herramientas utilizadas

- dnSpy
- OllyDbg / x64dbg
- PEiD
- Detect It Easy (DIE)
- Herramientas de dump de memoria

---

## Identificación de la protección

Al analizar el ejecutable con herramientas de detección se identifica la presencia de **Themida**.

Themida introduce mecanismos como:

- Anti-debug
- Anti-dump
- Cifrado del código
- Protección del entry point

En aplicaciones .NET además puede alterar el ensamblado y la estructura del código IL.

---

## Análisis dinámico

El análisis se realiza ejecutando el programa dentro de un **debugger**.

Durante la ejecución se puede observar cómo el stub del protector:

1. Inicializa el entorno de protección.
2. Realiza comprobaciones anti-debug.
3. Desencripta el código original en memoria.
4. Transfiere la ejecución al código real del programa.

---

## Recuperación del ensamblado

Una vez que el código original ha sido restaurado en memoria se puede proceder a:

1. Realizar un **dump del ensamblado desde memoria**.
2. Reconstruir el archivo ejecutable.
3. Cargar el ensamblado en **dnSpy** para continuar el análisis.

---

## Análisis con dnSpy

Tras recuperar el ensamblado, **dnSpy** permite:

- Descompilar el código IL a C#
- Analizar clases y métodos
- Modificar el código del programa
- Recompilar el ensamblado

Esto facilita enormemente el proceso de reversing de aplicaciones .NET.

---

## Conclusión

Aunque protectores como **Themida** introducen múltiples mecanismos de protección, mediante análisis dinámico y técnicas de dumping es posible recuperar el ensamblado original.

Una vez recuperado, herramientas como **dnSpy** permiten continuar el análisis del programa y comprender su funcionamiento interno.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
