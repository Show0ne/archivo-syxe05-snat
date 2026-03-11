# Cool Color Picker 1.1 – ACProtect 1.0x Reversing

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

ACProtect_1.0x_Cool_Color_Picker_1.1.pdf

---

## Introducción

Este tutorial analiza el software **Cool Color Picker 1.1**, protegido mediante **ACProtect 1.0x**.

ACProtect es un protector utilizado para proteger ejecutables Windows contra ingeniería inversa.  
Entre sus características principales se incluyen:

- Compresión del ejecutable
- Modificación del entry point
- Rutinas anti-debug
- Cifrado del código

El objetivo del análisis es estudiar el funcionamiento del stub del protector y recuperar el ejecutable original.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- LordPE / herramientas de dump
- Editor hexadecimal

---

## Identificación de la protección

Mediante herramientas como **PEiD** se puede detectar que el ejecutable está protegido con **ACProtect**.

Este protector utiliza un stub que:

- Descomprime o desencripta el código
- Inicializa estructuras internas
- Transfiere el control al código original

---

## Análisis dinámico

El análisis se realiza ejecutando el programa dentro de **OllyDbg**.

Durante el seguimiento del flujo de ejecución se pueden observar:

- Rutinas de inicialización del protector
- Operaciones de desencriptado del código
- Preparación del entorno de ejecución

Siguiendo el flujo del programa es posible identificar el momento en el que el protector finaliza su trabajo.

---

## Localización del OEP

Una vez finalizado el proceso del stub se alcanza el **Original Entry Point (OEP)**.

En ese punto comienza la ejecución del código real del programa.

Este es el momento adecuado para realizar un **dump del ejecutable desde memoria**.

---

## Dump del ejecutable

El procedimiento habitual consiste en:

1. Realizar un dump del proceso desde memoria.
2. Guardar el ejecutable reconstruido.
3. Analizar la tabla de importaciones.

---

## Reparación de la IAT

Después del dump, el ejecutable puede presentar una **Import Address Table incorrecta**.

Para reconstruirla se utiliza **Import Reconstructor (ImpREC)**:

1. Seleccionar el proceso activo.
2. Detectar automáticamente las importaciones.
3. Reparar la IAT.
4. Guardar el ejecutable final.

---

## Conclusión

Protectores como **ACProtect** añaden una capa adicional de protección contra el análisis estático.

Sin embargo, mediante técnicas de **análisis dinámico**, localización del OEP y reconstrucción de importaciones es posible recuperar el ejecutable original y continuar con el proceso de ingeniería inversa.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
