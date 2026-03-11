# Rasputín v1.6 – Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## Documento original
Rasputín v1.6.pdf

---

## Introducción

En este tutorial se analiza **Rasputín v1.6**, una aplicación protegida con un sistema de registro que impide el uso completo del programa sin un número de serie válido.

El objetivo del análisis es localizar la rutina que verifica el estado de registro y entender cómo el programa determina si está registrado.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se analiza inicialmente con **PEiD** para comprobar si el archivo está protegido con algún packer.

El resultado indica que el binario puede abrirse directamente con el depurador.

---

## Análisis dinámico

El programa se ejecuta dentro de **OllyDbg**.

Durante esta fase se buscan:

- mensajes de versión no registrada
- referencias al cuadro de registro
- cadenas relacionadas con el sistema de licencias

Estas pistas permiten localizar las funciones implicadas en el proceso de validación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la rutina encargada de validar el número de serie introducido por el usuario.

En esta sección del código aparecen instrucciones típicas como:

CMP  
TEST  
JE  
JNE

Estas instrucciones determinan si el programa continuará como versión registrada o no registrada.

---

## Modificación del flujo

Una vez localizada la comparación principal se puede modificar el flujo de ejecución para forzar la ruta válida.

Las técnicas comunes incluyen:

- invertir el salto condicional
- modificar la comparación
- eliminar la verificación

---

## Verificación

Tras aplicar el parche se ejecuta el programa fuera del depurador para comprobar que el registro se acepta correctamente.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
