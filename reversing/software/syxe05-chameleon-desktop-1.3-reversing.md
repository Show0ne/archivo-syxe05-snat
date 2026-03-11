# Chameleon Desktop 1.3 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
Chameleon Desktop 1.3.pdf

---

## Introducción

En este tutorial se analiza **Chameleon Desktop 1.3**, una aplicación destinada a personalizar el escritorio de Windows mediante diferentes temas y configuraciones visuales.

El programa utiliza un sistema de registro para desbloquear todas sus funcionalidades.
El objetivo del análisis es identificar cómo el programa valida el estado de registro.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se analiza con **PEiD** para comprobar si se encuentra comprimido o protegido.

El resultado indica que el ejecutable puede abrirse directamente en el depurador.

---

## Análisis dinámico

Se ejecuta el programa bajo **OllyDbg** para observar su comportamiento durante el proceso de validación.

Durante el análisis se buscan:

- mensajes relacionados con la versión no registrada
- referencias al cuadro de diálogo de registro
- cadenas relacionadas con la validación del serial

Estas referencias ayudan a localizar la rutina de verificación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la función encargada de comparar el número de serie introducido por el usuario.

En esta zona del código suelen aparecer instrucciones como:

CMP
TEST
JE
JNE

Estas instrucciones determinan si el programa continúa como versión registrada.

---

## Modificación del flujo

Una vez localizada la comparación principal se puede modificar el flujo del programa para forzar la ejecución de la rama válida.

Las técnicas habituales incluyen:

- invertir el salto condicional
- modificar la comparación
- eliminar la verificación

---

## Verificación

Tras aplicar la modificación se ejecuta el programa fuera del depurador para comprobar que se comporta como una versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
