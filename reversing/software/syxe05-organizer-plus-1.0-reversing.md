# Organizer Plus v1.0 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original
Organizer Plus v1.0.pdf

---

## Introducción

En este tutorial se analiza **Organizer Plus v1.0**, una aplicación diseñada para
gestionar información personal como contactos, notas y tareas. El programa utiliza
un sistema de registro para desbloquear todas sus funcionalidades.

El objetivo del análisis es localizar la rutina encargada de comprobar si el
programa está registrado y entender el mecanismo de validación del número de serie.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis preliminar

El ejecutable se analiza inicialmente con **PEiD** para determinar si el binario
está comprimido o protegido mediante algún packer.

El análisis indica que el ejecutable puede abrirse directamente en el depurador.

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
