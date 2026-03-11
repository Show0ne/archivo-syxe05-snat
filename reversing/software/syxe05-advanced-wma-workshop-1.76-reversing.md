# Advanced WMA Workshop 1.76 – Reversing Tutorial

Autor: SyXe'05
Categoría: Reversing / Software

## Documento original

Advanced WMA Workshop 1.76.pdf

---

## Introducción

En este tutorial se analiza el programa **Advanced WMA Workshop 1.76** mediante técnicas de ingeniería inversa.

El objetivo del análisis es comprender el mecanismo de protección utilizado por el software y localizar las rutinas responsables de validar el registro del programa.

Este tipo de aplicaciones shareware solían implementar protecciones basadas en seriales y comparaciones internas relativamente simples.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Identificación inicial

El primer paso consiste en analizar el ejecutable para determinar si está protegido por algún packer o protector.

Herramientas como **PEiD** permiten detectar:

- compresores de ejecutables
- packers conocidos
- protectores comerciales

En este caso el ejecutable puede analizarse directamente en un depurador.

---

## Análisis dinámico

El programa se ejecuta dentro de **OllyDbg** para observar su comportamiento.

Durante el análisis se buscan:

- referencias a mensajes de registro
- comparaciones relacionadas con seriales
- saltos condicionales asociados a la validación

Estas pistas ayudan a localizar la función encargada de comprobar el estado de registro.

---

## Localización de la rutina de validación

Siguiendo el flujo de ejecución se identifica una función que procesa el serial introducido por el usuario.

En esta rutina suelen aparecer instrucciones como:

- CMP
- TEST
- JE
- JNE

Dependiendo del resultado de estas comparaciones el programa decide si ejecutarse como versión registrada o limitar su funcionalidad.

---

## Modificación del flujo de ejecución

Una vez localizada la verificación crítica se puede modificar el comportamiento del programa.

Las técnicas más comunes incluyen:

- invertir un salto condicional
- forzar la rama válida del código
- eliminar la comprobación

Esto permite que el programa continúe su ejecución como si estuviera correctamente registrado.

---

## Verificación

Después de aplicar el parche se guarda el ejecutable modificado y se ejecuta fuera del depurador.

Si el procedimiento ha sido correcto:

- el programa se ejecutará sin restricciones
- el software se comportará como versión registrada

---

## Conclusión

El análisis de **Advanced WMA Workshop 1.76** muestra un ejemplo típico de protección shareware basada en validaciones internas simples.

Mediante técnicas básicas de depuración es posible localizar la rutina de verificación y modificar el flujo de ejecución para alterar el comportamiento del programa.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
