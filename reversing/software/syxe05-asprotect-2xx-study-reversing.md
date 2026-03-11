# Estudio de ASProtect 2.xx - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

Estudio de ASProtect 2.xx - [SyXe'05].pdf

---

## Introducción

Este documento presenta un estudio del protector **ASProtect 2.xx**, uno de los sistemas de protección shareware más utilizados en aplicaciones Windows durante la primera mitad de los años 2000.

ASProtect protege ejecutables mediante técnicas de ofuscación del flujo de ejecución, inserción de código adicional y rutinas de verificación que se ejecutan antes de alcanzar el código real del programa.

El objetivo del análisis es comprender la estructura del protector y estudiar cómo se comporta el ejecutable protegido durante su inicialización.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal

---

## Características de ASProtect

Durante el análisis se observan varias características típicas del protector:

- código inicial previo al OEP
- múltiples saltos cortos destinados a dificultar el seguimiento del flujo
- secciones de código ofuscadas
- rutinas internas de verificación

Estas técnicas complican el análisis estático y obligan a utilizar depuración dinámica para comprender el comportamiento del ejecutable.

---

## Flujo de ejecución

Al ejecutar el programa protegido se observa que el flujo de ejecución pasa primero por el código del protector.

Durante esta fase se ejecutan varias rutinas internas encargadas de:

- inicializar el entorno del protector
- verificar el estado del programa
- preparar la transferencia de control al código original

Finalmente el flujo alcanza el **Original Entry Point (OEP)** del programa protegido.

---

## Observaciones

ASProtect utiliza técnicas de ofuscación relativamente complejas para su época, incluyendo un gran número de saltos cortos y código polimórfico que dificultan la lectura directa del flujo de ejecución.

Estas técnicas hacen necesario el uso de depuración paso a paso para comprender la lógica interna del protector.

---

## Resultado

El análisis permite comprender cómo ASProtect 2.xx organiza su código de protección y cómo el ejecutable protegido transfiere finalmente el control al programa original.

Este conocimiento resulta útil para el estudio de aplicaciones protegidas con este sistema.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
