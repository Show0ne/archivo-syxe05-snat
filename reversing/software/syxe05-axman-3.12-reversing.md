# AxMan v3.12 – Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## Documento original
AxMan v3.12.pdf

---

## Introducción

En este tutorial se analiza **AxMan v3.12**, una herramienta utilizada para gestionar archivos y directorios en Windows.

El objetivo del análisis es estudiar el mecanismo de protección del programa y localizar la rutina responsable de verificar el estado de registro.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis inicial

El ejecutable se analiza con **PEiD** para comprobar si el binario está comprimido o protegido por algún packer.

El análisis muestra que el ejecutable puede abrirse directamente en el depurador sin necesidad de desempacado previo.

---

## Análisis dinámico

El programa se ejecuta dentro de **OllyDbg** para observar su comportamiento durante la ejecución.

Durante el análisis se buscan:

- mensajes relacionados con el registro
- cadenas que indiquen versión no registrada
- referencias al diálogo de registro

Estas referencias permiten localizar rápidamente la función de verificación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se identifica la rutina que determina si el programa está registrado.

En esta zona del código suelen aparecer instrucciones como:

CMP  
TEST  
JE  
JNE  

Estas comparaciones determinan si el programa se ejecuta como versión registrada.

---

## Modificación del flujo

Una vez localizada la comprobación crítica se puede modificar el flujo de ejecución:

- invertir un salto condicional
- forzar la rama válida
- eliminar la verificación

---

## Verificación

Tras aplicar el parche se ejecuta el programa fuera del depurador para comprobar que funciona correctamente.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
