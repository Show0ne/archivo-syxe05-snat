# QuizTotal v0.82 – Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## Documento original
quiztotal v0.82.pdf

---

## Introducción

En este tutorial se analiza **QuizTotal v0.82**, una aplicación que utiliza un sistema de registro para habilitar todas las funciones del programa.

El objetivo del análisis es localizar la rutina que verifica el estado de registro y entender cómo el programa determina si está registrado o en modo limitado.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se analiza inicialmente con **PEiD** para determinar si el binario está comprimido o protegido con algún packer.

El resultado indica que el ejecutable puede abrirse directamente en el depurador.

---

## Análisis dinámico

El programa se ejecuta dentro de **OllyDbg** para observar su comportamiento durante la inicialización.

Durante esta fase se buscan:

- mensajes relacionados con versión no registrada
- referencias al cuadro de registro
- cadenas relacionadas con la verificación del serial

Estas referencias permiten localizar las funciones responsables del sistema de registro.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la rutina que valida el número de serie introducido por el usuario.

En esta sección del código suelen aparecer instrucciones como:

CMP  
TEST  
JE  
JNE

Estas comparaciones determinan si el programa continúa ejecutándose como versión registrada o como versión limitada.

---

## Modificación del flujo

Una vez localizada la comparación principal se puede modificar el flujo de ejecución para forzar la rama válida.

Las técnicas habituales incluyen:

- invertir el salto condicional
- modificar la comparación
- eliminar la verificación

---

## Verificación

Después de aplicar el parche se ejecuta el programa fuera del depurador para comprobar que funciona correctamente como versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
