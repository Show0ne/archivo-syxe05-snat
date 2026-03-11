# Web Boomerang 3.0 - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

Web Boomerang 3.0.pdf

---

## Introducción

En este tutorial se analiza el software **Web Boomerang 3.0**, protegido mediante el sistema **Visual Protect**.

Visual Protect fue un sistema de protección shareware utilizado principalmente en aplicaciones desarrolladas con Visual Basic. Este tipo de protección suele implementar rutinas de comprobación del estado de registro que determinan si el programa se ejecuta en modo trial o registrado.

El objetivo del tutorial es localizar dichas rutinas y comprender cómo el programa valida el estado de registro.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal

---

## Identificación de la protección

Al analizar el ejecutable se observan características asociadas con **Visual Protect**, incluyendo rutinas internas encargadas de verificar el estado de registro del programa.

Estas rutinas suelen ejecutarse durante la inicialización de la aplicación y determinan el flujo de ejecución posterior.

---

## Análisis dinámico

Mediante el uso de **OllyDbg** se sigue el flujo de ejecución del programa hasta localizar las comparaciones relacionadas con la verificación del estado de registro.

Durante el análisis se identifican:

- comparaciones de valores internos
- saltos condicionales que controlan el modo de ejecución
- llamadas a funciones relacionadas con la validación de licencia

Estas instrucciones determinan si el programa continúa en modo trial o habilita el modo registrado.

---

## Modificación del flujo de ejecución

Una vez localizada la instrucción responsable de la verificación, es posible modificar el flujo del programa alterando el salto condicional que controla dicha comprobación.

Este tipo de modificación permite forzar el flujo de ejecución hacia el comportamiento correspondiente al programa registrado.

---

## Resultado

Tras modificar la instrucción correspondiente, el programa se ejecuta sin las limitaciones propias del modo trial, comportándose como una versión registrada.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
