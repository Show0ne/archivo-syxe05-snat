# MDT Server 2012 – Credential Error Troubleshooting

## Autor
Snat

## Descripción

Durante el despliegue de sistemas operativos en red utilizando **Microsoft Deployment Toolkit (MDT) sobre Windows Server 2012**, se detectó un problema relacionado con la validación de credenciales durante el proceso de deployment.

Este documento describe el proceso de investigación realizado para localizar el origen del problema y la solución aplicada.

El análisis incluye:

- revisión del flujo de autenticación en MDT
- inspección del proceso de conexión al Deployment Share
- análisis de tráfico de red
- uso de herramientas de diagnóstico como Wireshark
- modificación de scripts utilizados durante el proceso de despliegue

---

## Entorno de pruebas

Infraestructura utilizada durante el análisis:

- Windows Server 2012
- Microsoft Deployment Toolkit
- Windows Automated Installation Kit (WAIK)
- entorno de despliegue PXE
- clientes Windows en proceso de instalación automatizada

---

## Problema detectado

Durante el proceso de instalación del sistema operativo, el cliente solicitaba credenciales para acceder al recurso compartido del servidor MDT.

A pesar de que las credenciales introducidas eran correctas, el sistema devolvía un error de autenticación y el proceso de despliegue se detenía.

El problema impedía continuar con la instalación automatizada del sistema operativo.

---

## Análisis realizado

Para localizar el origen del problema se realizaron varias pruebas:

- revisión de los logs generados por MDT
- análisis del tráfico de red
- verificación de permisos en el recurso compartido
- revisión del comportamiento de los scripts utilizados durante el deployment

Durante el análisis se detectó un comportamiento incorrecto en la gestión de credenciales dentro del proceso de despliegue.

---

## Solución aplicada

La solución consistió en modificar el comportamiento de los scripts utilizados durante el proceso de deployment para gestionar correctamente las credenciales necesarias para acceder al Deployment Share.

Para ello se desarrollaron varios scripts que se ejecutan en distintos contextos durante el proceso de instalación.

Estos scripts permiten:

- inicializar correctamente las credenciales
- evitar conflictos durante la autenticación
- asegurar el acceso al recurso compartido del servidor MDT

---

## Resultado

Tras aplicar la solución, el proceso de despliegue del sistema operativo se ejecuta correctamente sin solicitar credenciales adicionales ni producir errores de autenticación.

El sistema puede completar la instalación automatizada sin intervención manual.

---

## Archivo original

El documento completo del análisis puede encontrarse en el PDF original incluido en este repositorio.

---

Autor: SyXe'05 / Snat
