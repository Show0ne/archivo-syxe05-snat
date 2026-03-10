# 1567 - Desempacando Themida 2.2.6.0 en Visual Basic
**Autor:** SNAT  
**Protector:** Themida 2.2.6.0  
**Lenguaje objetivo:** Visual Basic  
**Categoría:** Unpacking / Themida  

## PDF original
Themida en Visual Basic.pdf

---

## Introducción

Este tutorial muestra el proceso de análisis y desempacado de un ejecutable protegido con **Themida 2.2.6.0** cuyo programa original está desarrollado en **Visual Basic**.

Themida introduce múltiples capas de protección:

- Virtualización de código
- Anti‑debugging
- Ofuscación del Entry Point
- Manipulación de la Import Address Table (IAT)

El objetivo es recuperar el ejecutable original eliminando la capa de protección.

---

## Herramientas utilizadas

- OllyDbg
- Import Reconstructor (ImpREC)
- PE Tools
- Conocimientos de reversing en VB

---

## Proceso general

1. Ejecutar el programa protegido bajo el debugger.
2. Localizar el **Entry Point real (OEP)**.
3. Detectar cuándo Themida transfiere el control al código original.
4. Realizar un **dump del proceso en memoria**.
5. Reconstruir la **IAT**.
6. Corregir el ejecutable para que pueda ejecutarse de forma independiente.

---

## Localización del OEP

Durante la ejecución en el debugger se deben observar:

- saltos desde el código virtualizado
- cambios en el flujo de ejecución
- llamadas a APIs que indican el retorno al código real

Cuando se alcanza el **OEP**, se realiza el dump del proceso.

---

## Reconstrucción de la IAT

Una vez realizado el dump:

1. Cargar el ejecutable dumpeado en ImpREC.
2. Buscar automáticamente las importaciones.
3. Corregir la tabla de imports.
4. Guardar el ejecutable reconstruido.

---

## Resultado

El ejecutable resultante puede ejecutarse sin la protección de Themida.

---

## Notas

Themida es uno de los protectores más avanzados usados en software comercial.  
El análisis de aplicaciones protegidas requiere combinar **análisis estático y dinámico**.

---

Repositorio del proyecto:

https://github.com/Show0ne/archivo-syxe05-snat
