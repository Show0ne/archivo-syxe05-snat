# MDT 2012 Credential Error Troubleshooting

Este documento describe el análisis y resolución de un problema de credenciales durante el despliegue de sistemas operativos utilizando Microsoft Deployment Toolkit (MDT) y Windows Automated Installation Kit (WAIK).

## Entorno

- Microsoft Deployment Toolkit 2012
- Windows Server
- WAIK
- entorno de despliegue de sistemas operativos en red

## Problema

Durante el proceso de despliegue los clientes no podían autenticarse correctamente contra el deployment share, generando errores de credenciales.

## Investigación

Para diagnosticar el problema se analizaron múltiples componentes del proceso de despliegue:

- tráfico de red mediante Wireshark
- llamadas WMI
- interacción con NDIS
- integración de MDT con el entorno de despliegue
- análisis de logs y configuración

## Material de investigación

El repositorio incluye material utilizado durante el análisis:

- diagramas de arquitectura
- capturas de tráfico de red
- análisis de componentes WMI
- documentación de integración MDT

Todo este material se encuentra en:

os/windows/deployment/mdt-server-2012-credential-error-troubleshooting/

## Documento original

El análisis completo se encuentra en el documento:

Credentials Error en MDT 2012 y WAIK.pdf

## Autor

Autor: <tu nombre real>
Alias: SyXe'05 / Snat
