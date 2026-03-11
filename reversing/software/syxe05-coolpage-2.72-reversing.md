# CoolPage 2.72 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
CoolPage 2.72.pdf

---

## Introducción

En este tutorial se analiza **CoolPage 2.72**, una herramienta utilizada para la creación
y edición de páginas web. El programa incluye un sistema de registro que desbloquea
las funciones completas del software.

El objetivo del análisis es localizar la rutina que comprueba si el programa se
encuentra registrado y entender el mecanismo de validación del número de serie.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se examina inicialmente con **PEiD** para determinar si está
comprimido o protegido por algún packer.

El resultado indica que el ejecutable puede cargarse directamente en el depurador.

---

## Análisis dinámico

El programa se ejecuta dentro de **OllyDbg** para observar su comportamiento
durante la validación del registro.

Durante esta fase se buscan:

- mensajes relacionados con la versión no registrada
- referencias al cuadro de diálogo de registro
- cadenas relacionadas con la verificación del serial

Estas referencias permiten localizar la función encargada de validar el registro.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la rutina que compara el número
de serie introducido con el valor esperado.

En esta zona del código suelen aparecer instrucciones como:

CMP
TEST
JE
JNE

Estas instrucciones determinan si el programa continuará ejecutándose como versión
registrada o como versión limitada.

---

## Modificación del flujo

Una vez localizada la comparación principal se puede modificar el flujo de ejecución
para forzar la rama válida.

Las técnicas habituales incluyen:

- invertir el salto condicional
- modificar la comparación
- eliminar la verificación

---

## Verificación

Después de aplicar el parche se ejecuta el programa fuera del depurador para
comprobar que funciona correctamente como versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
