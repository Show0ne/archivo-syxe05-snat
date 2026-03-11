# DVD Region+CSS Free 5.9.6.8 (TimeTrial) - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software

## PDF original

DVD Region+CSS Free 5.9.6.8_parte2.pdf

---

## Introducción

Este documento continúa el análisis del software **DVD Region+CSS Free 5.9.6.8**, protegido mediante **ASProtect 1.2x – 1.3x**.

En esta segunda parte del tutorial se estudia específicamente el mecanismo de **TimeTrial** implementado por el protector.  
Los sistemas TimeTrial limitan el tiempo de uso del software mediante verificaciones internas que controlan la fecha de instalación, ejecución o número de ejecuciones.

El objetivo del análisis es comprender cómo se implementa este mecanismo y cómo puede localizarse dentro del flujo del programa protegido.

---

## Herramientas utilizadas

- OllyDbg
- PEiD
- Import Reconstructor (ImpREC)
- Editor hexadecimal

---

## Identificación de la protección

El ejecutable se encuentra protegido mediante:

ASProtect 1.2x – 1.3x

Esta versión del protector incorpora mecanismos adicionales como:

- Control de licencias
- TimeTrial
- Verificación de integridad
- Anti-debugging

---

## Análisis

El proceso de reversing seguido es el siguiente:

1. Ejecutar el programa bajo **OllyDbg**.
2. Seguir el flujo de ejecución del stub de ASProtect.
3. Identificar las rutinas responsables del control **TimeTrial**.
4. Analizar las comprobaciones de fecha y contador de ejecuciones.
5. Localizar el **Original Entry Point (OEP)** del ejecutable.
6. Realizar un **dump del proceso** y reconstruir la **IAT**.

Durante el análisis se identifican las funciones responsables de validar el tiempo de prueba y se observa cómo el protector intercepta la ejecución del programa original.

---

## Conclusión

El mecanismo TimeTrial implementado por ASProtect se basa en verificaciones internas que controlan el estado de ejecución del programa.

Mediante análisis dinámico es posible localizar estas rutinas, comprender su funcionamiento y continuar el proceso de análisis del ejecutable protegido.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
