# Hying's PE Armor 0.46 – Unpacking Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

C106N3_Hyings_PE_Armor_0.46.pdf

---

## Introducción

Este tutorial analiza un ejecutable protegido mediante **Hying's PE Armor 0.46**.

PE Armor es un **packer/protector para ejecutables Windows** diseñado para:

- Comprimir el ejecutable
- Ocultar el código original
- Introducir mecanismos anti-debug
- Dificultar el análisis estático

Durante la ejecución, el stub del protector restaura el ejecutable original en memoria antes de transferir la ejecución al programa real.

El objetivo del análisis es identificar el flujo del protector y recuperar el ejecutable original.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- LordPE / herramientas de dump
- Editor hexadecimal

---

## Identificación del protector

Al analizar el ejecutable con **PEiD** se detecta la presencia de **Hying's PE Armor**.

Este protector utiliza un stub que:

- Descomprime el código protegido
- Inicializa estructuras internas
- Prepara la transferencia al código original

---

## Análisis dinámico

El análisis se realiza ejecutando el programa dentro de **OllyDbg**.

Durante el seguimiento del flujo de ejecución se pueden observar las rutinas responsables de:

- Desencriptar o descomprimir el código
- Restaurar las secciones originales
- Preparar la ejecución del programa protegido

Siguiendo cuidadosamente el flujo se puede identificar el punto donde termina la rutina del protector.

---

## Localización del OEP

Una vez finalizado el proceso del stub se alcanza el **Original Entry Point (OEP)**.

En este punto el código que se ejecuta ya pertenece al programa original.

Este es el momento adecuado para realizar el **dump del ejecutable desde memoria**.

---

## Dump del ejecutable

El procedimiento consiste en:

1. Realizar un dump del proceso desde memoria.
2. Guardar el ejecutable reconstruido.
3. Analizar y reparar la tabla de importaciones.

---

## Reparación de la IAT

Tras el dump el ejecutable suele tener una **Import Address Table incorrecta**.

Para reconstruirla se utiliza **Import Reconstructor (ImpREC)**:

1. Seleccionar el proceso activo.
2. Detectar las importaciones.
3. Reparar la IAT.
4. Guardar el ejecutable final reconstruido.

---

## Conclusión

Protectores como **Hying's PE Armor** introducen una capa adicional de dificultad en el análisis de ejecutables.

Sin embargo, mediante **análisis dinámico**, localización del OEP y reconstrucción de importaciones es posible recuperar el ejecutable original y continuar con el reversing.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
