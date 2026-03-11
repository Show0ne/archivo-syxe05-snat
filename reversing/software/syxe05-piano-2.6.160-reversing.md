# Piano v2.6.160 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
Piano v2.6.160.pdf

---

## Introducción

En este tutorial se analiza **Piano v2.6.160**, una aplicación que simula un piano virtual en el sistema.
El programa utiliza un sistema de registro para habilitar todas las funciones disponibles.

El objetivo del análisis consiste en localizar la rutina encargada de verificar el estado de registro del programa.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se analiza inicialmente con **PEiD** para determinar si está comprimido o protegido.

El resultado muestra que el programa puede cargarse directamente en el depurador sin necesidad de desempaquetarlo previamente.

---

## Análisis dinámico

El programa se ejecuta bajo **OllyDbg** para observar su comportamiento.

Durante esta fase se buscan referencias a:

- mensajes de versión no registrada
- el cuadro de diálogo de registro
- cadenas relacionadas con la verificación del serial

Estas referencias permiten localizar las funciones relacionadas con la validación.

---

## Localización de la rutina de validación

Siguiendo las referencias encontradas se llega a la función que compara el número de serie introducido por el usuario con el valor esperado.

En esta zona del código aparecen comparaciones típicas como:

CMP
TEST
JE
JNE

Estas instrucciones determinan si el programa considera válido el registro.

---

## Modificación del flujo

Una vez localizada la comparación principal se puede modificar el flujo del programa para que siempre siga la ruta válida.

Las técnicas habituales incluyen:

- modificar el salto condicional
- alterar el resultado de la comparación
- eliminar la verificación

---

## Verificación

Después de aplicar la modificación se ejecuta el programa fuera del depurador para comprobar que el estado de registro se mantiene activo.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
