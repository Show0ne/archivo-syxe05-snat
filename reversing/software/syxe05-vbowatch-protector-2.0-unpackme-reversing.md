# UnPackMe – VBOWatch Protector 2.0 (Reversing)

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

UnPackMe_VBOWatch_Protector 2.0.pdf

---

## Introducción

Este documento analiza un ejecutable protegido con **VBOWatch Protector 2.0**.

VBOWatch es un protector utilizado principalmente en aplicaciones desarrolladas en **Visual Basic**, diseñado para:

- Ocultar el código del programa
- Introducir protecciones anti‑debug
- Dificultar la ingeniería inversa

El objetivo del ejercicio es comprender el funcionamiento del stub del protector y recuperar el ejecutable original.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

Mediante herramientas de detección se identifica que el ejecutable está protegido con **VBOWatch Protector 2.0**.

Este tipo de protector suele:

- Alterar el Entry Point del programa
- Introducir comprobaciones anti‑debug
- Cargar dinámicamente partes del código

---

## Análisis dinámico

El análisis se realiza ejecutando el programa dentro de **OllyDbg**.

Durante la ejecución se observan distintas rutinas del stub encargadas de:

- Inicializar el entorno del protector
- Desencriptar el código original
- Preparar la ejecución del programa protegido

Siguiendo el flujo de ejecución se identifica el momento en el que el control se transfiere al código original.

---

## Localización del OEP

Cuando el stub finaliza su trabajo se alcanza el **Original Entry Point (OEP)**.

En ese punto se puede proceder a:

1. Realizar un **dump del proceso desde memoria**.
2. Guardar el ejecutable reconstruido.
3. Reparar la tabla de importaciones.

---

## Reconstrucción de importaciones

El ejecutable reconstruido requiere la reparación de la **Import Address Table (IAT)**.

Para ello se utiliza **Import Reconstructor (ImpREC)**:

1. Seleccionar el proceso.
2. Detectar las importaciones.
3. Reparar la IAT.
4. Guardar el ejecutable final.

---

## Conclusión

Los protectores orientados a aplicaciones Visual Basic como **VBOWatch** introducen varias capas de protección.

Sin embargo, mediante **análisis dinámico y localización del OEP**, es posible reconstruir el ejecutable original y continuar con el análisis del programa.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
