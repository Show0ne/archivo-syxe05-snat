
# Add Remove Plus! 2002 3.0.0.146 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original

Add Remove Plus! 2002 3.0.pdf

---

## Introducción

En este tutorial se analiza **Add Remove Plus! 2002 3.0.0.146**, una aplicación shareware diseñada para gestionar la instalación y desinstalación de programas en Windows.

El objetivo es estudiar el sistema de protección del programa y localizar la rutina encargada de validar el registro del software.

Este tipo de protecciones era común en aplicaciones shareware de principios de los años 2000.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis inicial

El primer paso consiste en analizar el ejecutable con **PEiD** para determinar si el programa está comprimido o protegido por algún packer.

PEiD permite identificar:

- compresores de ejecutables
- protectores comerciales
- firmas conocidas

En este caso el ejecutable puede analizarse directamente en un depurador.

---

## Análisis dinámico

El programa se carga en **OllyDbg** para observar su comportamiento durante la ejecución.

Durante el análisis se buscan:

- cadenas relacionadas con el registro
- mensajes de error o advertencia
- funciones que procesan el serial

Estas referencias ayudan a localizar la zona del código donde se realiza la verificación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se identifica la rutina encargada de validar el serial.

En esta zona del código suelen aparecer instrucciones como:

- CMP
- TEST
- JE
- JNE

Dependiendo del resultado de estas comparaciones el programa decide si continuar como versión registrada o mostrar limitaciones.

---

## Modificación del flujo de ejecución

Una vez localizada la verificación crítica se puede modificar el flujo del programa.

Las técnicas habituales incluyen:

- invertir un salto condicional
- forzar la rama válida
- eliminar la comprobación

Tras aplicar el parche el programa funcionará como versión registrada.

---

## Verificación

El ejecutable modificado se guarda y se ejecuta fuera del depurador.

Si el proceso se ha realizado correctamente:

- el programa funcionará sin limitaciones
- el registro aparecerá como válido

---

## Conclusión

El análisis de **Add Remove Plus! 2002 3.0.0.146** muestra un ejemplo clásico de protección shareware basada en verificaciones simples.

Mediante técnicas básicas de reversing es posible localizar la rutina de validación y modificar el flujo de ejecución para eliminar las restricciones.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
