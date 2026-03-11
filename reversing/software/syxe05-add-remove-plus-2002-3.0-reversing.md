# Add Remove Plus! 2002 3.0 - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software  

---

## Introducción

Este tutorial analiza el software **Add Remove Plus! 2002 3.0** desde la perspectiva
de la ingeniería inversa. El objetivo es estudiar el mecanismo de protección
implementado por el programa y comprender cómo se determina el estado de registro.

Durante los primeros años de la escena de reversing, este tipo de aplicaciones
shareware se utilizaban frecuentemente para aprender técnicas de análisis
de protecciones y validaciones de licencia.

---

## Herramientas utilizadas

Para realizar el análisis se emplean herramientas clásicas de ingeniería inversa:

- OllyDbg
- Desensambladores
- Analizadores de ejecutables PE
- Herramientas de monitorización de APIs

---

## Análisis inicial

El primer paso consiste en examinar el ejecutable para identificar:

- Entry Point del programa
- estructura del archivo PE
- posibles packers o protecciones
- llamadas relevantes a APIs del sistema

Este análisis permite comprender cómo se inicia el programa y localizar
las zonas del código potencialmente relacionadas con el sistema de registro.

---

## Ejecución bajo debugger

El programa se ejecuta bajo un debugger para observar:

- el flujo de ejecución durante el arranque
- comparaciones relacionadas con el estado de registro
- comportamiento del programa en modo limitado

Durante esta fase se buscan instrucciones de comparación (CMP)
y saltos condicionales (JE, JNE, JNZ) que determinan si el
software se encuentra registrado.

---

## Localización de la rutina de validación

Mediante el análisis del flujo de ejecución se identifica la función
responsable de:

- comprobar el estado de registro
- habilitar o restringir funcionalidades
- mostrar mensajes de advertencia del modo trial

Estas rutinas suelen contener comparaciones o llamadas internas
relacionadas con el sistema de licencia.

---

## Modificación del flujo de ejecución

Una vez localizada la rutina de verificación, el comportamiento del
programa puede modificarse mediante:

- parcheo de saltos condicionales
- modificación de comparaciones
- alteración de valores de retorno

Esto permite redirigir la ejecución hacia el flujo correspondiente
al modo registrado.

---

## Resultado

Tras aplicar las modificaciones necesarias, el programa se ejecuta
como versión registrada, eliminando las restricciones del modo trial.

---

## Notas

Este tipo de tutoriales representan ejemplos clásicos de reversing
aplicado a software shareware de principios de los años 2000.

Repositorio del proyecto:
https://github.com/Show0ne/archivo-syxe05-snat
