# PCInvestigator v2.05 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
PCInvestigator v2.05.pdf

---

## Introducción

En este tutorial se analiza **PCInvestigator v2.05**, una herramienta utilizada para
recuperación y análisis de archivos eliminados. Como muchas aplicaciones
shareware de la época, el programa utiliza un sistema de registro para habilitar
todas sus funcionalidades.

El objetivo del análisis es localizar la rutina que comprueba el estado de
registro del programa y entender cómo se valida el número de serie.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se analiza inicialmente con **PEiD** para determinar si está
comprimido o protegido mediante algún packer.

El análisis indica que el ejecutable puede abrirse directamente con el
depurador sin necesidad de desempaquetarlo.

---

## Análisis dinámico

El programa se ejecuta bajo **OllyDbg** para observar su comportamiento durante
la validación del registro.

Durante esta fase se buscan:

- mensajes relacionados con la versión no registrada
- referencias al cuadro de diálogo de registro
- cadenas relacionadas con la verificación del serial

Estas referencias permiten localizar la rutina de validación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la función que compara el número
de serie introducido por el usuario con el valor esperado.

En esta zona del código suelen aparecer instrucciones como:

CMP
TEST
JE
JNE

Estas instrucciones determinan si el programa continuará ejecutándose como
versión registrada o como versión limitada.

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

Después de aplicar el parche se ejecuta el programa fuera del depurador para
comprobar que funciona correctamente como versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
