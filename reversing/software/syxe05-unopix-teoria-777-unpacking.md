# Desempacando UnOpix – Teoría 777

Autor: SyXe'05  
Categoría: Reversing / Unpacking

## PDF original

C109N3_SyXe'05.pdf

---

## Introducción

Este documento analiza el proceso de **desempaquetado del protector UnOpix**.

UnOpix es un packer utilizado para proteger ejecutables de Windows. Como muchos protectores de su época, introduce un stub que se encarga de preparar el entorno antes de transferir el control al código original del programa.

El objetivo del análisis es comprender cómo funciona este protector y cómo localizar el **Original Entry Point (OEP)** para recuperar el ejecutable original.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- LordPE
- Editor hexadecimal

---

## Identificación del packer

El primer paso consiste en identificar el protector utilizado.

Mediante herramientas como **PEiD** se puede detectar la presencia del packer **UnOpix**.

El protector introduce un stub que realiza varias tareas:

- Inicialización del entorno
- Desencriptado del código
- Preparación de estructuras internas
- Transferencia al código original

---

## Análisis dinámico

Para analizar el protector se ejecuta el programa dentro de **OllyDbg**.

Durante la ejecución se observan las rutinas responsables de:

- Desencriptar o restaurar el código protegido
- Copiar datos en memoria
- Preparar la transferencia al código original

Siguiendo el flujo de ejecución se puede identificar el punto donde finaliza el stub del protector.

---

## Localización del OEP

Una vez finalizado el proceso del stub se alcanza el **Original Entry Point (OEP)**.

Este punto marca el comienzo de la ejecución del programa original.

En este momento es posible realizar un **dump del ejecutable desde memoria**.

---

## Dump del ejecutable

El procedimiento consiste en:

1. Realizar un dump del proceso desde memoria.
2. Guardar el ejecutable reconstruido.
3. Analizar la tabla de importaciones.

---

## Reparación de la IAT

Después del dump el ejecutable puede tener una **Import Address Table (IAT) incorrecta**.

Para solucionarlo se utiliza **Import Reconstructor (ImpREC)**:

1. Seleccionar el proceso activo.
2. Detectar las importaciones.
3. Reparar la IAT.
4. Guardar el ejecutable final.

---

## Conclusión

Protectores como **UnOpix** introducen técnicas diseñadas para dificultar el análisis del ejecutable.

Sin embargo, mediante **análisis dinámico**, seguimiento del flujo de ejecución y reconstrucción de importaciones es posible recuperar el ejecutable original y continuar con el proceso de ingeniería inversa.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
