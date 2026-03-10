# Ulead CD & DVD PictureShow 3 Trial - Reversing Tutorial
Autor: SyXe'05
Categoría: Reversing / Software

## PDF original
Ulead CD & DVD PictureShow 3 Trial.pdf

---

## Introducción

Este tutorial analiza el software **Ulead CD & DVD PictureShow 3 Trial** desde la perspectiva de la ingeniería inversa.

El objetivo es estudiar el mecanismo de protección del modo trial y comprender cómo el programa controla:

- limitaciones de uso
- verificación de licencia
- comportamiento del modo registrado

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal
- Conocimientos básicos de reversing

---

## Análisis inicial

El ejecutable es analizado para identificar:

- Entry Point
- estructura del archivo PE
- posibles protecciones o packers
- APIs relevantes utilizadas por el programa

Este análisis permite comprender la estructura general del binario.

---

## Ejecución bajo debugger

El programa se ejecuta dentro de un debugger para observar:

- flujo de ejecución
- comportamiento del modo trial
- funciones relacionadas con validación de registro

Durante esta fase se identifican comparaciones y saltos condicionales que controlan el acceso a funcionalidades.

---

## Localización de la verificación de licencia

Mediante el análisis del flujo de ejecución se localiza la rutina responsable de:

- verificar si el software está registrado
- activar o desactivar funciones del programa

Estas rutinas suelen contener comparaciones y saltos condicionales claves.

---

## Modificación del flujo de ejecución

Una vez identificada la rutina de validación, el comportamiento del programa puede alterarse mediante:

- modificación de saltos condicionales
- parcheo de instrucciones
- alteración de comparaciones

Esto permite dirigir la ejecución hacia el flujo correspondiente al modo registrado.

---

## Resultado

Tras aplicar las modificaciones necesarias, el programa puede ejecutarse sin las restricciones del modo trial.

---

## Notas

Este tipo de tutoriales eran comunes en la escena de reversing de principios de los 2000, utilizando software shareware para aprender técnicas de ingeniería inversa.

---

Repositorio del proyecto:
https://github.com/Show0ne/archivo-syxe05-snat
