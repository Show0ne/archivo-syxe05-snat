# PDF Password Remover v2.2 – Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## Documento original
PDF Password Remover v2.2.pdf

---

## Introducción

En este tutorial se analiza **PDF Password Remover v2.2**, una aplicación diseñada para eliminar restricciones de seguridad en archivos PDF.

El objetivo del análisis es localizar el mecanismo que controla el estado de registro de la aplicación y comprender cómo el programa valida la licencia.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se analiza inicialmente con **PEiD** para determinar si el archivo está comprimido o protegido mediante algún packer.

El resultado indica que el binario puede abrirse directamente con el depurador.

---

## Análisis dinámico

El programa se ejecuta dentro de **OllyDbg** para observar su comportamiento durante la inicialización.

Durante esta fase se buscan:

- mensajes relacionados con la versión de prueba
- referencias al cuadro de registro
- cadenas relacionadas con la verificación del serial

Estas referencias permiten localizar las funciones implicadas en el proceso de validación.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la rutina encargada de validar el número de serie.

En esta sección del código suelen encontrarse instrucciones como:

CMP
TEST
JE
JNE

Estas comparaciones determinan si el programa continúa ejecutándose como versión registrada o como versión limitada.

---

## Modificación del flujo

Una vez localizada la comparación principal se puede modificar el flujo de ejecución para forzar la ruta válida.

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
