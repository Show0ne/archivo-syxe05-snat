# 007 Starr Commander 2.0 – Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## Documento original

007 Starr Commander 2.0.pdf

---

## Introducción

En este tutorial se analiza **007 Starr Commander 2.0**, un gestor de archivos clásico para Windows.

El objetivo es comprender el sistema de protección implementado por la aplicación y localizar las rutinas responsables de validar el registro del software.

Durante la época del shareware era habitual que programas como este implementaran mecanismos de protección simples basados en seriales o flags internos.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Identificación del ejecutable

El primer paso consiste en analizar el ejecutable para identificar si está protegido o comprimido por algún packer.

Para ello se utilizan herramientas como **PEiD**, que permiten detectar:

- packers conocidos
- compresores de ejecutables
- protectores comerciales

En este caso el ejecutable puede analizarse directamente en un depurador.

---

## Análisis dinámico

El programa se carga en **OllyDbg** y se ejecuta paso a paso.

Durante el análisis se buscan:

- referencias a cadenas relacionadas con el registro
- funciones que procesan el serial
- comparaciones que determinan si el programa está registrado

Estas referencias permiten localizar rápidamente la rutina de validación.

---

## Localización de la rutina de validación

Siguiendo el flujo de ejecución se identifica la función que verifica el serial introducido por el usuario.

En esta sección del código suelen aparecer instrucciones como:

- CMP
- TEST
- JE
- JNE

Dependiendo del resultado de estas comparaciones el programa decide si ejecutarse como versión registrada o mostrar limitaciones.

---

## Modificación del flujo de ejecución

Una vez localizada la verificación crítica se puede modificar el comportamiento del programa.

Las técnicas más habituales incluyen:

- invertir un salto condicional
- forzar la ejecución de la rama válida
- eliminar la comprobación

Esto permite que el programa continúe ejecutándose como si estuviera registrado.

---

## Verificación

Tras aplicar el parche se guarda el ejecutable modificado y se ejecuta fuera del depurador.

Si el procedimiento ha sido correcto:

- el programa funcionará sin restricciones
- se comportará como versión registrada.

---

## Conclusión

El análisis de **007 Starr Commander 2.0** muestra un ejemplo clásico de protección shareware simple.

Mediante técnicas básicas de depuración y análisis del flujo de ejecución es posible localizar la rutina de verificación y modificar el comportamiento del programa.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
