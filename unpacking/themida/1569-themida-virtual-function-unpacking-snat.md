# 1569 - Desempacando Themida 2.x con Función Virtual
Autor: SNAT  
Protector: Themida 2.x  
Categoría: Unpacking / Themida  

## PDF original
Desempacando Themida 2.x con Funcion Virtual por SNAT

---

## Introducción

En este tutorial se analiza un ejecutable protegido con **Themida 2.x** que utiliza técnicas de virtualización mediante funciones virtuales. Estas protecciones complican el análisis porque el código original es transformado en instrucciones que son interpretadas por una máquina virtual interna.

El objetivo es localizar el **Original Entry Point (OEP)** y reconstruir el ejecutable limpio.

---

## Herramientas utilizadas

- OllyDbg / x32dbg
- Import Reconstructor (ImpREC)
- PE Tools
- Conocimientos básicos de reversing

---

## Protecciones de Themida

Themida implementa múltiples mecanismos de defensa:

- Virtualización de funciones
- Anti-debugging
- Ofuscación de código
- Control del flujo de ejecución
- Manipulación de la Import Address Table (IAT)

Estas técnicas obligan a realizar un análisis dinámico para observar cuándo el flujo de ejecución vuelve al código original.

---

## Estrategia de análisis

1. Ejecutar el binario protegido dentro del debugger.
2. Seguir el flujo de ejecución desde el Entry Point inicial.
3. Identificar bloques de código pertenecientes a la máquina virtual.
4. Detectar el salto hacia el código real de la aplicación.
5. Localizar el **OEP**.

---

## Dump del proceso

Una vez alcanzado el OEP:

1. Realizar un **dump del proceso en memoria**.
2. Guardar el ejecutable resultante.
3. Reparar la tabla de importaciones.

---

## Reconstrucción de la IAT

Para reconstruir las importaciones:

1. Cargar el ejecutable dumpeado en ImpREC.
2. Buscar automáticamente las APIs utilizadas.
3. Reconstruir la Import Address Table.
4. Guardar el ejecutable final.

---

## Resultado

Tras reconstruir la IAT y corregir el PE, el ejecutable resultante puede ejecutarse sin la protección de Themida.

---

Repositorio del proyecto:

https://github.com/Show0ne/archivo-syxe05-snat
