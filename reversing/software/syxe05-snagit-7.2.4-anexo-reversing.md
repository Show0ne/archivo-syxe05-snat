# SnagIt 7.2.4 (Anexo) – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
SnagIt 7.2.4_anexo.pdf

---

## Introducción

En este tutorial se analiza **SnagIt 7.2.4**, una conocida herramienta de captura
de pantalla para Windows. Este documento corresponde a un **anexo** al tutorial
principal, donde se revisan detalles adicionales del proceso de análisis y
registro del programa.

El objetivo del análisis es localizar la rutina que verifica si el programa
está registrado y comprender el mecanismo de validación del número de serie.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se inspecciona con **PEiD** para determinar si el binario está
empaquetado o protegido por algún packer.

El análisis muestra que el ejecutable puede cargarse directamente en el
depurador sin necesidad de desempaquetado previo.

---

## Análisis dinámico

El programa se ejecuta bajo **OllyDbg** para observar el proceso de validación
del registro.

Durante el análisis se buscan:

- mensajes de versión no registrada
- referencias al cuadro de diálogo de registro
- cadenas relacionadas con la verificación del serial

Estas referencias permiten localizar la función responsable de la verificación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se alcanza la función que compara el
número de serie introducido por el usuario con el valor esperado.

En el código aparecen instrucciones típicas como:

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
confirmar que funciona correctamente como versión registrada.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
