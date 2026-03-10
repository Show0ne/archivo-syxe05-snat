# C110N4 — VMProtect 1.24 (Concurso 110 Nivel 4)

| Campo | Valor |
|------|------|
| Programa | FTP de Ricardo |
| Protección | VMProtect 1.24 |
| Autor | SyXe'05 |
| Grupo | CracksLatinoS |
| Fecha | 19/11/2006 |

PDF original: **C110N4_VMProtect_1.24_SyXe'05.pdf**

---

# Introducción

Este tutorial corresponde al **Concurso 110 Nivel 4** publicado por CracksLatinoS en 2006.
El objetivo del reto es analizar un ejecutable protegido con **VMProtect 1.24** y
realizar su desempaquetado manual.

El programa utilizado en el desafío es un pequeño cliente FTP denominado
"FTP de Ricardo".

---

# Identificación de la protección

Al analizar el ejecutable con herramientas como **PEiD** o **RDG Packer Detector**
no se obtiene una detección clara en el escaneo estándar.

Sin embargo, el análisis heurístico revela la presencia de:

VMProtect 1.24

Este packer introduce múltiples mecanismos de protección:

- virtualización de código
- ofuscación del flujo de ejecución
- destrucción de la IAT
- inserción de código basura

---

# Análisis inicial

Al cargar el ejecutable en **OllyDbg** se observa que el flujo de ejecución
está altamente ofuscado.

El programa realiza múltiples saltos indirectos y llamadas hacia rutinas
virtualizadas.

El objetivo inicial es encontrar el **OEP (Original Entry Point)** del programa.

---

# Estrategia de análisis

Para llegar al OEP se utiliza una combinación de técnicas:

- seguimiento del flujo de ejecución
- análisis de excepciones
- identificación de llamadas a APIs del sistema

Durante el proceso se identifican varias rutinas del packer encargadas
de descifrar el código original del ejecutable.

---

# Localización del OEP

Tras continuar la ejecución dentro del debugger y saltar varias rutinas
del packer se alcanza el punto en el que comienza el código real del
programa protegido.

Este punto corresponde al **Original Entry Point**.

A partir de aquí es posible realizar un **dump del ejecutable**.

---

# Dump del ejecutable

Una vez localizado el OEP se realiza el dump del proceso utilizando
herramientas como:

- OllyDump
- LordPE

El ejecutable resultante todavía contiene problemas en la tabla de
importaciones.

---

# Reconstrucción de la IAT

Para reparar la tabla de importaciones se utiliza **Import Reconstructor (ImpREC)**.

Pasos:

1. cargar el ejecutable dumpeado
2. localizar la dirección de la IAT
3. reconstruir las funciones importadas
4. guardar el ejecutable reparado

Una vez completado este proceso el programa puede ejecutarse sin la
protección VMProtect.

---

# Conclusión

El tutorial muestra el proceso de análisis y desempaquetado manual de
un ejecutable protegido con **VMProtect 1.24**.

Las técnicas utilizadas incluyen:

- análisis dinámico con debugger
- localización del OEP
- dump del ejecutable
- reconstrucción de la IAT

---

Autor: **SyXe'05**  
Grupo: **CracksLatinoS**
