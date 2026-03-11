# Reverseando mIRC 7.43 – Reversing Tutorial

Autor: SNAT
Categoría: Reversing / mIRC

## Documento original

Reverseando mIRC 7.43.pdf

---

## Introducción

En este tutorial se analiza **mIRC 7.43**, uno de los clientes IRC más conocidos para Windows.

El objetivo del análisis es comprender el mecanismo de registro del programa y localizar la rutina encargada de verificar si la aplicación está registrada.

mIRC ha sido históricamente un objetivo frecuente para prácticas de reversing debido a su modelo shareware.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Editor hexadecimal

---

## Análisis inicial

Se analiza el ejecutable con **PEiD** para determinar si está comprimido o protegido por algún packer.

El análisis muestra que el binario puede abrirse directamente en el depurador sin necesidad de desempaquetado previo.

---

## Análisis dinámico

El programa se ejecuta dentro de **OllyDbg** para observar su comportamiento.

Durante el análisis se buscan:

- cadenas relacionadas con el registro
- mensajes de versión no registrada
- referencias al diálogo de registro

Estas referencias permiten localizar rápidamente la rutina de validación.

---

## Localización de la verificación

Siguiendo las referencias a las cadenas relacionadas con el registro se identifica la función responsable de comprobar el estado del registro.

En esta zona aparecen instrucciones típicas como:

- CMP
- TEST
- JE
- JNE

Estas comparaciones determinan si el programa debe ejecutarse como versión registrada.

---

## Modificación del flujo de ejecución

Una vez localizada la comparación crítica se puede modificar el flujo del programa.

Las técnicas habituales incluyen:

- invertir un salto condicional
- forzar la ejecución de la rama válida
- eliminar la comprobación

---

## Verificación

Después de aplicar el parche el ejecutable se guarda y se ejecuta fuera del depurador.

Si el procedimiento se ha realizado correctamente el programa se ejecutará como versión registrada.

---

## Conclusión

El análisis de **mIRC 7.43** muestra un ejemplo clásico de protección shareware simple.

Mediante técnicas básicas de reversing es posible localizar la rutina de verificación y modificar el flujo de ejecución para eliminar las limitaciones.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
