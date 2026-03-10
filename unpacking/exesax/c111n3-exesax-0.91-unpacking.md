# C111N3 — ExeSax 0.91 Unpacking

| Campo | Valor |
|------|------|
| Protección | ExeSax 0.91 |
| Autor | SyXe'05 |
| Grupo | CracksLatinoS |
| Año | 2006 |

PDF original: **C111N3_ExeSax_0.91.pdf**

---

## Introducción

Este tutorial explica el proceso de análisis y desempaquetado de un ejecutable protegido con **ExeSax 0.91**.

ExeSax fue un packer bastante popular en aplicaciones shareware de principios de los años 2000. Su funcionamiento consiste en comprimir o cifrar el ejecutable original y restaurarlo en memoria durante la ejecución mediante un stub de carga.

Objetivos del análisis:

- identificar la protección utilizada
- localizar el **OEP (Original Entry Point)**
- realizar el dump del ejecutable desde memoria
- reconstruir la **IAT (Import Address Table)**

---

## Identificación del packer

Utilizando herramientas de identificación como:

- PEiD
- RDG Packer Detector

se detecta que el ejecutable está protegido con:

ExeSax 0.91

Este packer introduce varias modificaciones en el ejecutable:

- stub de carga inicial
- código de desencriptado
- restauración dinámica del código original

---

## Análisis con debugger

Al cargar el ejecutable en **OllyDbg** se observa que la ejecución comienza en el stub del packer.

El stub realiza varias operaciones:

1. reserva memoria
2. copia el ejecutable original desempaquetado
3. reconstruye estructuras internas
4. transfiere la ejecución al programa original

Durante este proceso se producen múltiples operaciones de copia de memoria.

---

## Localización del OEP

Para localizar el **Original Entry Point** se puede seguir el flujo de ejecución dentro del debugger.

Una vez que el stub finaliza la rutina de desempaquetado se produce un salto hacia el código original del programa.

Ese salto marca el **OEP real del ejecutable**.

---

## Dump del ejecutable

Una vez localizado el OEP se puede realizar el dump del proceso utilizando herramientas como:

- OllyDump
- LordPE

El archivo generado aún contiene errores en la tabla de importaciones.

---

## Reconstrucción de la IAT

Para reparar la tabla de importaciones se utiliza **Import Reconstructor (ImpREC)**.

Proceso:

1. cargar el ejecutable dumpeado
2. localizar el inicio de la IAT
3. reconstruir las funciones importadas
4. guardar el ejecutable reparado

Una vez completado este proceso el programa puede ejecutarse correctamente.

---

## Conclusión

El tutorial demuestra cómo desempaquetar manualmente un ejecutable protegido con **ExeSax 0.91** mediante técnicas clásicas de reversing:

- análisis dinámico con debugger
- localización del OEP
- dump del ejecutable
- reconstrucción de la IAT

---

Autor: **SyXe'05**  
Grupo: **CracksLatinoS**
