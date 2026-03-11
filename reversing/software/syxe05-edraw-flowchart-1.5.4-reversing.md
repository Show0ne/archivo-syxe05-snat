# EDraw Flowchart 1.5.4 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
EDraw_Flowchart_v1.5.4.pdf

---

## Introducción

En este tutorial se analiza **EDraw Flowchart 1.5.4**, una aplicación para crear
diagramas y flowcharts en Windows.

El objetivo es localizar la rutina que comprueba si el programa está
registrado y entender el mecanismo de validación del número de serie.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

Se analiza el ejecutable con **PEiD** para comprobar si está empaquetado.

El resultado muestra que el binario no está protegido por packers conocidos
y puede cargarse directamente en el depurador.

---

## Análisis dinámico

El programa se ejecuta bajo **OllyDbg** y se observan:

- referencias a mensajes de versión trial
- cadenas relacionadas con registro
- funciones que procesan el serial

Estas referencias ayudan a localizar la rutina de verificación.

---

## Localización de la verificación

Siguiendo las referencias se llega a la función que compara el número de serie.

En el código suelen aparecer instrucciones como:

CMP
TEST
JE
JNE

Estas instrucciones determinan si el programa continúa como versión
registrada o limitada.

---

## Modificación del flujo

Una vez localizada la verificación se puede modificar el flujo de ejecución:

- invertir el salto condicional
- modificar la comparación
- forzar el valor de retorno

---

## Verificación

Tras aplicar el parche se ejecuta el programa fuera del depurador para
confirmar que funciona como versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
