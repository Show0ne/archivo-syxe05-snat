# ExeSax 0.91 – Unpacking Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

C111N3_ExeSax_0.91.pdf

---

## Introducción

Este tutorial analiza el software **ExeSax 0.91**, un protector utilizado para empaquetar ejecutables de Windows.

ExeSax es un tipo de **packer**, cuyo objetivo es:

- Comprimir el ejecutable original
- Proteger el código contra análisis estático
- Dificultar la ingeniería inversa

Durante el proceso de ejecución, el stub del packer se encarga de restaurar el código original en memoria.

El objetivo del reversing es localizar el **Original Entry Point (OEP)** y reconstruir el ejecutable original.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación del packer

Mediante herramientas de detección como **PEiD** se puede identificar que el ejecutable está protegido con **ExeSax**.

Este packer utiliza un stub que:

- Descomprime el ejecutable en memoria
- Reconstruye estructuras internas
- Transfiere el control al código original

---

## Análisis del stub

El análisis se realiza ejecutando el programa bajo **OllyDbg**.

Durante el seguimiento del flujo de ejecución se identifican las rutinas encargadas de:

- Descomprimir el código protegido
- Restaurar las secciones originales del ejecutable
- Preparar la transferencia al OEP

---

## Localización del OEP

Siguiendo la ejecución del stub se puede identificar el momento en el que el código original del programa comienza a ejecutarse.

Ese punto corresponde al **Original Entry Point (OEP)**.

---

## Dump del ejecutable

Una vez alcanzado el OEP se procede a:

1. Realizar un **dump del ejecutable desde memoria**.
2. Guardar el archivo reconstruido.
3. Reparar la **Import Address Table (IAT)**.

---

## Reconstrucción de importaciones

Para reconstruir las importaciones se utiliza **Import Reconstructor (ImpREC)**:

1. Seleccionar el proceso en ejecución.
2. Detectar automáticamente la tabla de importaciones.
3. Reparar la IAT.
4. Guardar el ejecutable final reconstruido.

---

## Conclusión

Aunque packers como **ExeSax** introducen una capa adicional de protección, mediante análisis dinámico es posible:

- Localizar el OEP
- Recuperar el ejecutable original
- Reconstruir correctamente las importaciones

Estas técnicas forman parte del flujo habitual en procesos de **unpacking durante ingeniería inversa**.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
