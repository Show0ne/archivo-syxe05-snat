# Diablo II: Lord of Destruction - SecuROM Analysis

Autor: SyXe'05  
Categoría: Reversing / DRM

## PDF original

Diablo II_Lord of Destruction.pdf

---

## Introducción

Este tutorial analiza el sistema de protección **SecuROM v4.x–v5.x** utilizado en el juego *Diablo II: Lord of Destruction*.

SecuROM es un sistema de protección de copia ampliamente utilizado en videojuegos comerciales que implementa múltiples mecanismos anti-copia y anti-debug.

El objetivo del análisis es comprender el funcionamiento del sistema de protección y estudiar cómo interactúa con el ejecutable del juego.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- FileMon / RegMon
- Editor hexadecimal

---

## Análisis de la protección

Durante el análisis se observan varias características típicas de **SecuROM**:

- verificación del disco original
- rutinas anti-debug
- chequeos de integridad
- redirección del flujo de ejecución

El ejecutable protegido contiene múltiples capas de comprobación que se ejecutan antes de alcanzar el código principal del programa.

---

## Flujo de ejecución

El análisis dinámico permite observar:

- llamadas internas del sistema de protección
- verificación de presencia del medio original
- mecanismos de detección de depuración

Estas rutinas se ejecutan antes de transferir el control al **OEP del ejecutable real**.

---

## Observaciones

SecuROM implementa técnicas destinadas a dificultar el análisis mediante:

- ofuscación del flujo de ejecución
- detección de herramientas de depuración
- verificación del entorno de ejecución

Esto obliga a utilizar análisis dinámico para comprender el comportamiento del sistema.

---

## Resultado

El estudio del ejecutable permite comprender cómo SecuROM protege el binario y cómo se estructura el flujo de ejecución antes de llegar al código del programa.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
