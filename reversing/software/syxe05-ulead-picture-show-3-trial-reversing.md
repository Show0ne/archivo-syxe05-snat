# Ulead CD & DVD PictureShow 3 Trial – Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## Documento original
Ulead CD & DVD PictureShow 3 Trial.pdf

---

## Introducción

En este tutorial se analiza **Ulead CD & DVD PictureShow 3 Trial**, una aplicación utilizada para crear presentaciones multimedia en CD/DVD.

El objetivo del análisis es identificar cómo el programa implementa su sistema de limitación **Trial** y localizar la rutina responsable de verificar el estado de registro.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El primer paso consiste en analizar el ejecutable con **PEiD** para comprobar si el binario está protegido por algún packer.

El análisis muestra que el ejecutable puede abrirse directamente en el depurador.

---

## Análisis dinámico

El programa se ejecuta dentro de **OllyDbg** para observar su comportamiento.

Durante esta fase se buscan:

- mensajes relacionados con versión *Trial*
- referencias al cuadro de registro
- cadenas relacionadas con expiración o limitación

Estas referencias ayudan a localizar la lógica de control de licencia.

---

## Localización de la verificación

Siguiendo las referencias encontradas se llega a la rutina encargada de validar si la aplicación está registrada.

En esta zona del código aparecen típicamente instrucciones como:

CMP  
TEST  
JE  
JNE

Estas comparaciones determinan si el programa continuará ejecutándose como versión registrada o como versión de prueba.

---

## Modificación del flujo

Una vez localizada la comprobación principal se puede modificar el flujo de ejecución para forzar la rama válida.

Las técnicas habituales incluyen:

- invertir el salto condicional
- parchear la comparación
- eliminar la verificación de estado Trial

---

## Verificación

Tras aplicar el parche se ejecuta el programa fuera del depurador para comprobar que funciona correctamente sin las limitaciones de la versión Trial.

---

Repositorio:
https://github.com/Show0ne/archivo-syxe05-snat
