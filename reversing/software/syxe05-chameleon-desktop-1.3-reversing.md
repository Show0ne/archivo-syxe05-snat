# Chameleon Desktop 1.3

Autor: SyXe'05  
Categoría: Reversing / Software  
Software analizado: Chameleon Desktop 1.3  

---

## Introducción
En este tutorial se analiza el software **Chameleon Desktop 1.3**, una aplicación destinada a la personalización del entorno de escritorio en sistemas Windows.

El objetivo del análisis es comprender el mecanismo de verificación de licencia implementado por el programa y estudiar cómo se determina el estado de registro del software.

---

## Herramientas utilizadas

- OllyDbg
- W32Dasm

---

## Análisis inicial

Se examina el ejecutable para identificar el punto de entrada del programa y las rutinas relacionadas con el control de licencia.

---

## Ejecución bajo debugger

El programa se ejecuta bajo un debugger para observar el flujo de ejecución durante el arranque y localizar comparaciones relacionadas con el estado de registro.

---

## Rutina de validación

Se identifica la función responsable de determinar si el programa se encuentra registrado.

---

## Modificación del flujo

Se modifica la instrucción que determina el resultado de la verificación para forzar el comportamiento registrado.

---

## Resultado

El programa se ejecuta como versión registrada tras modificar el flujo de ejecución.
