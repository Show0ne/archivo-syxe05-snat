# Cartoonist 1.1 – Reversing Tutorial (Parte 2)

Autor: SyXe'05  
Categoría: Reversing / Software

## PDF original

cartoonist_parte2.pdf

---

## Introducción

Este documento corresponde a la **segunda parte del análisis de Cartoonist 1.1**.  
En esta fase se continúa el estudio del mecanismo de protección utilizado por el software y se profundiza en la localización de la rutina de validación.

El objetivo es comprender completamente el flujo de ejecución del programa y determinar el punto donde se valida la licencia.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Reanudando el análisis

Tras identificar el punto inicial de ejecución en la primera parte del análisis, se continúa el seguimiento del flujo dentro de **OllyDbg**.

Durante la depuración se analizan:

- llamadas a funciones internas
- comparaciones de valores relacionados con el registro
- saltos condicionales que determinan el estado de la licencia

---

## Identificación de la verificación

En el proceso de análisis se localiza una rutina encargada de comprobar la validez del serial.

Esta rutina suele incluir instrucciones como:

- CMP
- TEST
- JNE
- JE

El resultado de estas instrucciones determina si el programa continúa en modo registrado o limitado.

---

## Modificación del flujo

Una vez identificada la comparación crítica se puede alterar el flujo de ejecución.

Las técnicas utilizadas incluyen:

- invertir un salto condicional
- forzar el flujo hacia la ruta válida
- eliminar la comprobación

Este procedimiento permite que el programa se comporte como si el registro fuera válido.

---

## Guardado del ejecutable

Después de modificar las instrucciones necesarias se guarda el ejecutable parcheado.

El archivo resultante se prueba fuera del depurador para confirmar que:

- el programa inicia correctamente
- no aparecen restricciones de licencia

---

## Conclusión

El análisis de **Cartoonist 1.1** muestra un ejemplo clásico de protección basada en verificaciones de serial.

Mediante técnicas de depuración y modificación del flujo de ejecución es posible comprender el funcionamiento del sistema de protección y alterar su comportamiento.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
