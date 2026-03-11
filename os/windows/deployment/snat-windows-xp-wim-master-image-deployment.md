# Creación de una Imagen Maestra de Windows XP (WIM) para Despliegue en Red

Autor: SNAT  
Categoría: OS / Windows Deployment

## Documento original

Creación de una imagen Maestra de Windows XP (WIM).pdf

---

## Introducción

Este documento describe el proceso utilizado para crear una **imagen maestra de Windows XP** con el objetivo de desplegar el sistema operativo en múltiples equipos dentro de una red local.

Este procedimiento era común en entornos como:

- aulas informáticas
- centros educativos
- laboratorios
- redes corporativas

La idea principal consiste en preparar una instalación base completamente configurada y después capturarla en una **imagen WIM**, que posteriormente puede desplegarse rápidamente en múltiples máquinas.

---

## Objetivos

Los objetivos del proceso son:

- reducir el tiempo de instalación del sistema operativo
- mantener configuraciones homogéneas en todos los equipos
- facilitar el mantenimiento de los laboratorios informáticos

---

## Preparación del sistema maestro

El primer paso consiste en preparar un equipo que actuará como **sistema base**.

En este sistema se realiza:

- instalación limpia de Windows XP
- instalación de drivers necesarios
- instalación del software educativo o corporativo
- aplicación de actualizaciones del sistema
- configuración del entorno

Este sistema será posteriormente capturado para crear la imagen maestra.

---

## Uso de Sysprep

Antes de capturar la imagen es necesario generalizar la instalación del sistema operativo.

Para ello se utiliza **Sysprep**, herramienta de Microsoft diseñada para preparar sistemas Windows para su duplicación.

El proceso incluye:

- eliminación de identificadores únicos del sistema
- preparación para detección de hardware en el primer arranque
- configuración del modo de mini-setup

---

## Captura de la imagen WIM

Una vez preparado el sistema se procede a capturar la imagen utilizando herramientas de despliegue.

Las imágenes **WIM (Windows Imaging Format)** permiten almacenar una instalación completa del sistema operativo en un único archivo.

Este archivo puede almacenarse en:

- servidor de red
- repositorio de imágenes
- sistema de despliegue PXE

---

## Despliegue en red

Una vez creada la imagen maestra, el siguiente paso es desplegarla en los equipos del aula o laboratorio.

Esto se puede realizar mediante:

- arranque por red (PXE)
- herramientas de instalación automatizada
- entornos de despliegue de Windows

El proceso permite instalar el sistema operativo completo en cuestión de minutos.

---

## Ventajas del despliegue mediante imágenes

Las ventajas principales de este método son:

- instalación extremadamente rápida
- configuración homogénea en todos los equipos
- simplificación del mantenimiento
- reducción del trabajo administrativo

Este tipo de despliegue fue ampliamente utilizado en entornos educativos y corporativos durante la era de Windows XP.

---

## Conclusión

La creación de **imágenes maestras de sistemas operativos** representa una técnica fundamental para la administración de infraestructuras con múltiples equipos.

Mediante herramientas como **Sysprep** y el uso de **imágenes WIM**, es posible desplegar rápidamente sistemas completos manteniendo consistencia y reduciendo el tiempo de administración.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
