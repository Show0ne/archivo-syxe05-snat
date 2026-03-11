# Add Remove Plus! 2002 v3.0 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
Add Remove Plus! 2002 v3.0.pdf

---

## Introducción

En este tutorial se analiza **Add Remove Plus! 2002 v3.0**, una herramienta para gestionar
aplicaciones instaladas en Windows y mejorar las funciones del panel clásico
“Agregar o quitar programas”.

El programa utiliza un sistema de registro que desbloquea las funcionalidades
completas. El objetivo del análisis es localizar la rutina que comprueba el
estado de registro del software.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se analiza inicialmente con **PEiD** para comprobar si está
empaquetado o protegido.

El análisis muestra que el binario puede cargarse directamente en el depurador
sin necesidad de desempaquetarlo.

---

## Análisis dinámico

El programa se ejecuta bajo **OllyDbg** para observar el comportamiento del
ejecutable durante la validación del registro.

Durante esta fase se buscan:

- mensajes relacionados con la versión no registrada
- referencias al cuadro de diálogo de registro
- cadenas relacionadas con la comprobación del serial

Estas pistas permiten localizar la rutina de validación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la función encargada de comparar
el número de serie introducido por el usuario.

En esta zona del código suelen encontrarse instrucciones como:

CMP
TEST
JE
JNE

Estas instrucciones determinan si el programa continuará ejecutándose como
versión registrada.

---

## Modificación del flujo

Una vez localizada la comparación principal se puede modificar el flujo de
ejecución para forzar la ruta válida.

Las técnicas habituales incluyen:

- invertir el salto condicional
- modificar la comparación
- eliminar la verificación

---

## Verificación

Tras aplicar el parche se ejecuta el programa fuera del depurador para comprobar
que funciona correctamente como versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
