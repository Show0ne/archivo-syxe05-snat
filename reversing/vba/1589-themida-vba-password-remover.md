# 1589 — Themida 2.3.9.0 VBA Password Remover

| Campo | Valor |
|------|------|
| Protección | Themida 2.3.9.0 |
| Objetivo | VBA Password Remover |
| Autor | SNAT & Apuromafo |
| Grupo | CracksLatinoS |

PDF original: **Themida 2.3.9.0 Vba Password Remover por Snat & Apuromafo.pdf**

---

## Introducción

Este documento describe el análisis de una herramienta protegida con **Themida 2.3.9.0** cuyo propósito es eliminar la contraseña de proyectos **VBA** (Visual Basic for Applications).  

El tutorial muestra cómo estudiar el ejecutable protegido, identificar los mecanismos de protección introducidos por Themida y aplicar técnicas de reversing para comprender el funcionamiento del programa.

---

## Identificación de la protección

Mediante herramientas como:

- PEiD
- RDG Packer Detector

se puede identificar que el ejecutable está protegido con **Themida 2.3.9.0**.

Themida introduce múltiples mecanismos de protección:

- virtualización de código
- anti-debugging
- ofuscación del flujo
- anti-dumping

---

## Análisis dinámico

El análisis se realiza ejecutando el programa bajo debugger.

Durante esta fase se observa cómo el stub de Themida:

1. inicializa estructuras internas
2. realiza rutinas de desencriptado
3. transfiere la ejecución al código real del programa

Siguiendo el flujo de ejecución se puede localizar el **OEP (Original Entry Point)**.

---

## Dump del ejecutable

Una vez alcanzado el OEP se procede a realizar un dump del ejecutable desde memoria.

Herramientas utilizadas:

- OllyDump
- LordPE

Posteriormente es necesario reparar la tabla de importaciones.

---

## Reconstrucción de la IAT

Para reconstruir la **Import Address Table** se utiliza **Import Reconstructor (ImpREC)**.

Proceso:

1. cargar el ejecutable dumpeado
2. localizar la dirección de la IAT
3. reconstruir las funciones importadas
4. guardar el ejecutable reparado

---

## Análisis del funcionamiento

Una vez eliminado el protector Themida, el programa puede analizarse con mayor facilidad.

El análisis permite comprender cómo el software elimina la contraseña de proyectos VBA protegidos.

---

## Conclusión

Este tutorial muestra cómo analizar una aplicación protegida con **Themida 2.3.9.0** y estudiar su funcionamiento interno mediante técnicas clásicas de reversing.

Las técnicas utilizadas incluyen:

- debugging dinámico
- localización del OEP
- dump del ejecutable
- reconstrucción de la IAT

---

Autor: **SNAT & Apuromafo**  
Grupo: **CracksLatinoS**
