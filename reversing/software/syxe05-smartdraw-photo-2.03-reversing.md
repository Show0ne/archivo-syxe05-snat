# SmartDraw Photo v2.03 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
SmartDraw Photo v2.03.pdf

---

## Introducción

En este tutorial se analiza **SmartDraw Photo v2.03**, una aplicación de edición y organización de imágenes que utiliza un sistema clásico de registro shareware.

El objetivo del análisis es localizar la rutina de verificación del serial y comprender cómo el programa determina si la copia está registrada.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis inicial

El ejecutable se analiza con **PEiD** para determinar si está comprimido o protegido por algún packer.

El análisis muestra que el binario puede abrirse directamente en el depurador.

---

## Análisis dinámico

El programa se ejecuta dentro de **OllyDbg** para observar su comportamiento.

Durante el análisis se buscan:

- cadenas relacionadas con el registro
- mensajes de versión no registrada
- referencias al cuadro de diálogo de registro

Estas referencias permiten localizar rápidamente la rutina de validación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se identifica la función responsable de comprobar el estado del registro.

En esta zona del código suelen aparecer instrucciones como:

- CMP
- TEST
- JE
- JNE

Estas comparaciones determinan si el programa debe ejecutarse como versión registrada.

---

## Modificación del flujo de ejecución

Una vez localizada la comparación crítica se puede modificar el flujo del programa.

Las técnicas habituales incluyen:

- invertir un salto condicional
- forzar la ejecución de la rama válida
- eliminar la comprobación

---

## Verificación

Después de aplicar el parche el ejecutable se ejecuta fuera del depurador para comprobar que el programa funciona como versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
