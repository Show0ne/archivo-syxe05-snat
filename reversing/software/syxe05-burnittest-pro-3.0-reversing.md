# BurnItTest Pro 3.0 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
BurnItTest Pro v3.0.pdf

---

## Introducción

En este tutorial se analiza **BurnItTest Pro 3.0**, una aplicación utilizada
para probar unidades de grabación de CD/DVD.

El objetivo del análisis consiste en localizar la rutina responsable de la
validación del registro y comprender el mecanismo utilizado por el programa
para determinar si la aplicación está registrada.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se analiza inicialmente con **PEiD** para determinar si el
binario está comprimido mediante algún packer.

El análisis muestra que el ejecutable no está empaquetado, por lo que puede
abrirse directamente en **OllyDbg**.

---

## Análisis dinámico

El programa se ejecuta bajo **OllyDbg** para observar el comportamiento del
proceso de validación del número de serie.

Durante el análisis se buscan referencias a:

- mensajes de versión no registrada
- funciones relacionadas con la validación
- cadenas asociadas al sistema de registro

Estas referencias permiten localizar la función encargada de la comprobación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la función que compara el
número de serie introducido con el valor esperado.

En esta sección del código aparecen instrucciones típicas como:

CMP
TEST
JE
JNE

Estas instrucciones determinan el flujo del programa dependiendo del
resultado de la comparación.

---

## Modificación del flujo

Una vez identificada la verificación principal se puede modificar el flujo
de ejecución para forzar la ruta válida.

Las técnicas habituales incluyen:

- invertir el salto condicional
- modificar la comparación
- forzar el valor de retorno de la función

---

## Verificación

Tras aplicar el parche se ejecuta el programa fuera del depurador para
confirmar que la aplicación funciona correctamente como versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
