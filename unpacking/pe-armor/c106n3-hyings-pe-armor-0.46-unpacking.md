# C106N3 — Hyings PE Armor 0.46 Unpacking

| Campo | Valor |
|------|------|
| Protección | Hyings PE Armor 0.46 |
| Autor | SyXe'05 |
| Grupo | CracksLatinoS |
| Año | 2006 |

PDF original: **C106N3_Hyings_PE_Armor_0.46.pdf**

---

## Introducción

Este tutorial corresponde al **Concurso 106 Nivel 3** publicado por CracksLatinoS.
El objetivo es analizar un ejecutable protegido con **Hyings PE Armor 0.46** y
realizar su desempaquetado manual.

Hyings PE Armor fue un protector utilizado en aplicaciones shareware y
software comercial ligero. Su funcionamiento consiste en envolver el
ejecutable original dentro de un stub que se encarga de restaurarlo en memoria
durante la ejecución.

---

## Identificación del packer

Al analizar el ejecutable con herramientas como:

- PEiD
- RDG Packer Detector

se detecta la protección:

Hyings PE Armor 0.46

El packer introduce:

- un stub de carga
- código de desencriptado
- reconstrucción dinámica del ejecutable original

---

## Análisis con debugger

Al ejecutar el programa en **OllyDbg** se observa que la ejecución comienza
en el stub del protector.

Este stub realiza varias tareas:

1. reserva memoria para el ejecutable original
2. desempaqueta el código protegido
3. prepara las estructuras internas
4. transfiere la ejecución al programa real

Durante este proceso se producen múltiples operaciones de copia de memoria.

---

## Localización del OEP

Para localizar el **Original Entry Point (OEP)** se sigue el flujo de ejecución
dentro del debugger.

Una vez finalizada la rutina de desempaquetado se produce un salto hacia el
código original del programa.

Ese salto marca el **OEP real del ejecutable**.

---

## Dump del ejecutable

Cuando se alcanza el OEP se puede realizar el dump del proceso utilizando
herramientas como:

- OllyDump
- LordPE

El archivo generado todavía requiere reparar la tabla de importaciones.

---

## Reconstrucción de la IAT

Para reconstruir la tabla de importaciones se utiliza
**Import Reconstructor (ImpREC)**.

Proceso:

1. cargar el ejecutable dumpeado
2. localizar la dirección de la IAT
3. reconstruir las funciones importadas
4. guardar el ejecutable reparado

Una vez completado este proceso el ejecutable puede ejecutarse correctamente
sin la protección.

---

## Conclusión

El tutorial demuestra cómo desempaquetar manualmente un ejecutable protegido
con **Hyings PE Armor 0.46** utilizando técnicas clásicas de reversing:

- análisis dinámico
- seguimiento del flujo de ejecución
- localización del OEP
- dump del ejecutable
- reconstrucción de la IAT

---

Autor: **SyXe'05**  
Grupo: **CracksLatinoS**
