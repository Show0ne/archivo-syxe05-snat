# DVD Region+CSS Free 5.9.6.8 - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software  

## PDF original

DVD Region+CSS Free 5.9.6.8.pdf

---

## Introducción

Análisis del software **DVD Region+CSS Free 5.9.6.8** desde la perspectiva de ingeniería inversa.

El programa utiliza el protector **ASProtect 1.2x – 1.3x**, una evolución del protector utilizado en versiones anteriores de software shareware.

El objetivo del análisis es localizar las rutinas de verificación utilizadas por el protector y modificar el flujo de ejecución para evitar las restricciones del modo trial.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal

---

## Análisis

Se examina el ejecutable para identificar la presencia del protector **ASProtect** y estudiar el flujo de ejecución antes de alcanzar el código principal del programa.

Durante el análisis se observan:

- inicialización del protector
- ejecución del código previo al **OEP**
- llamadas internas utilizadas para validar el estado del programa

Mediante el uso de un debugger se identifican comparaciones y saltos condicionales responsables de determinar si el software se ejecuta en modo registrado.

---

## Rutinas de validación

Durante el análisis se identifican varias llamadas internas relacionadas con el control de licencia.

Estas llamadas son documentadas en un archivo auxiliar donde se listan las direcciones de memoria que deben ser analizadas o modificadas.

---

## Modificación del flujo

Una vez localizadas las rutinas relevantes, se procede a modificar el flujo de ejecución alterando las instrucciones responsables de la verificación.

Esto permite forzar el comportamiento del programa como si estuviera registrado.

---

## Resultado

Tras aplicar las modificaciones necesarias, el programa se ejecuta sin las restricciones impuestas por el modo trial.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
