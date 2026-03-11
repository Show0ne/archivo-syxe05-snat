# ARWizard 3.1 – Armadillo + CopyMemII Reversing

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

Armadillo+CopyMemII_ARWizard_3.1.pdf

---

## Introducción

Este tutorial analiza el programa **ARWizard 3.1**, protegido con **Armadillo** y técnicas adicionales basadas en **CopyMemII**.

Armadillo fue uno de los protectores comerciales más utilizados en aplicaciones Windows.  
Entre sus características principales se incluyen:

- Compresión del ejecutable
- Protección del entry point
- Anti-debug
- Encriptación del código

En este caso el protector utiliza además técnicas relacionadas con **CopyMemII**, que complican el análisis del flujo de ejecución.

El objetivo del reversing es:

- Analizar el stub del protector
- Identificar el flujo de desencriptado
- Localizar el **Original Entry Point (OEP)**
- Reconstruir el ejecutable original

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- LordPE / herramientas de dump
- Editor hexadecimal

---

## Identificación de la protección

Mediante herramientas de detección como **PEiD** se identifica que el ejecutable está protegido con **Armadillo**.

Durante la ejecución se observan:

- Rutinas de desencriptado
- Manipulación de memoria
- Transferencias indirectas de ejecución

El uso de **CopyMemII** introduce movimientos de memoria diseñados para ocultar el flujo real del programa.

---

## Análisis dinámico

El análisis se realiza ejecutando el programa dentro de **OllyDbg**.

Durante la ejecución del stub se identifican varias fases:

1. Inicialización del protector
2. Desencriptado del código original
3. Restauración de estructuras del ejecutable
4. Transferencia del control al programa original

Siguiendo cuidadosamente el flujo de ejecución se puede identificar el momento en el que termina la rutina del protector.

---

## Localización del OEP

Una vez finalizado el proceso de inicialización del protector se alcanza el **Original Entry Point (OEP)**.

En ese punto el código que se ejecuta ya pertenece al programa original.

Este es el momento adecuado para realizar un **dump del ejecutable desde memoria**.

---

## Dump del ejecutable

El proceso consiste en:

1. Realizar un dump del proceso desde memoria.
2. Guardar el ejecutable reconstruido.
3. Analizar la tabla de importaciones.

---

## Reparación de la IAT

Tras el dump el ejecutable suele presentar una **Import Address Table incorrecta**.

Para reconstruirla se utiliza **Import Reconstructor (ImpREC)**:

1. Seleccionar el proceso activo.
2. Detectar las importaciones.
3. Reparar la IAT.
4. Guardar el ejecutable final reconstruido.

---

## Conclusión

La combinación de **Armadillo + CopyMemII** introduce una capa adicional de complejidad durante el análisis.

Sin embargo, mediante técnicas de **análisis dinámico**, seguimiento del flujo de ejecución y reconstrucción de importaciones es posible recuperar el ejecutable original y continuar con el reversing.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
