# Socket Programming – Referencias

Autor: SNAT  
Categoría: Windows / Networking / Referencias

## PDF original

Socket_Programming.pdf

---

## Introducción

Este documento recopila conceptos fundamentales sobre **programación de sockets en Windows**.  
Los sockets permiten la comunicación entre procesos a través de una red utilizando protocolos como **TCP** y **UDP**.

Comprender el funcionamiento de los sockets es importante para:

- Desarrollo de aplicaciones cliente/servidor
- Análisis de tráfico de red
- Ingeniería inversa de aplicaciones que utilizan comunicación de red
- Investigación de seguridad

---

## Conceptos básicos

Un **socket** es un punto final de comunicación entre dos procesos.  
En sistemas Windows se utilizan normalmente a través de la API **Winsock**.

Las etapas básicas de una comunicación mediante sockets incluyen:

1. Creación del socket
2. Asociación a un puerto (bind)
3. Escucha de conexiones (listen)
4. Aceptación de conexiones (accept)
5. Envío y recepción de datos

---

## Herramientas utilizadas

Para el análisis o depuración de aplicaciones que utilizan sockets pueden emplearse herramientas como:

- Wireshark
- API Monitor
- OllyDbg
- Process Explorer

Estas herramientas permiten observar la interacción entre la aplicación y la pila de red del sistema.

---

## Análisis

Durante el reversing de aplicaciones que utilizan comunicación de red suele analizarse:

1. Inicialización de **Winsock**.
2. Creación de sockets mediante llamadas a la API.
3. Establecimiento de conexiones TCP o envío de datagramas UDP.
4. Procesamiento de los datos transmitidos.
5. Posibles mecanismos de cifrado o codificación.

Comprender estas operaciones permite reconstruir el protocolo utilizado por la aplicación.

---

## Conclusión

El conocimiento de **socket programming** es esencial para el análisis de aplicaciones que utilizan comunicación de red.

Durante la ingeniería inversa, identificar las llamadas a la API de red y observar el tráfico generado permite comprender cómo interactúa la aplicación con otros sistemas.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
