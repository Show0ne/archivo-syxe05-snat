# SVKP v1.3x – Registry Medic (Parte 2) Reversing

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

SVKP_v1.3x_Registry_Medic_parte2.pdf

---

## Introducción

Esta segunda parte continúa el análisis del software **Registry Medic** protegido con **SVKP v1.3x**.

Tras haber identificado el comportamiento inicial del protector en la primera parte, el objetivo ahora es:

- Localizar con precisión el **Original Entry Point (OEP)**
- Realizar el **dump del ejecutable desde memoria**
- Reconstruir correctamente la **Import Address Table (IAT)**

---

## Herramientas utilizadas

- OllyDbg
- Import Reconstructor (ImpREC)
- PE Tools
- Editor hexadecimal

---

## Localización del OEP

Durante la ejecución del stub del protector se observan varias rutinas encargadas de:

- Desencriptar el código original
- Restaurar estructuras internas del ejecutable
- Transferir el control al programa protegido

Siguiendo el flujo de ejecución en **OllyDbg** se identifica el momento en el que el protector finaliza su proceso de inicialización.

En ese punto se alcanza el **Original Entry Point** del programa.

---

## Dump del ejecutable

Una vez localizado el OEP se procede a:

1. Realizar un **dump del proceso desde memoria**.
2. Guardar el ejecutable reconstruido.
3. Analizar las importaciones faltantes.

---

## Reconstrucción de la IAT

El ejecutable reconstruido todavía contiene una **tabla de importaciones incorrecta**.

Para solucionar esto se utiliza **Import Reconstructor (ImpREC)**:

1. Seleccionar el proceso en ejecución.
2. Detectar automáticamente las importaciones.
3. Reparar la IAT.
4. Guardar el ejecutable final reconstruido.

---

## Resultado

Tras reconstruir correctamente la IAT el ejecutable puede ejecutarse sin depender del stub de protección de SVKP.

Esto demuestra que, incluso con protecciones diseñadas para dificultar el análisis, es posible recuperar el ejecutable original mediante técnicas de **análisis dinámico y reconstrucción de importaciones**.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
