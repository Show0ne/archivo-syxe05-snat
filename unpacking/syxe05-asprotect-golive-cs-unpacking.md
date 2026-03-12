# GoLive CS — Unpacking ASProtect

Autor: SyXe'05  
Tipo: Unpacking tutorial  
Protección: ASProtect  
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analiza el ejecutable del programa GoLive CS protegido con ASProtect.

ASProtect es un sistema de protección desarrollado por Alexey Solodovnikov que fue ampliamente utilizado en aplicaciones shareware. Este protector introduce varias técnicas destinadas a dificultar el análisis del ejecutable, como compresión del código, verificación de integridad y mecanismos anti-debug.

El objetivo del tutorial consiste en localizar el punto donde finaliza el proceso de desempaquetado y el programa original recupera el control de la ejecución.

---

## Información sobre ASProtect

Entre las características principales de ASProtect se encuentran:

- Compresión del ejecutable
- Verificación de integridad del código
- Protección frente a depuradores
- Sistemas de licencia y registro

Cuando cargamos un ejecutable protegido con ASProtect en un depurador, el código que observamos inicialmente pertenece al loader del protector y no al programa original.

---

## Análisis inicial

Al ejecutar el programa bajo el depurador observamos que el Entry Point pertenece a ASProtect.

Esto significa que el código visible inicialmente es parte del proceso de inicialización del protector. El programa original aún no se ha cargado completamente en memoria.

El primer objetivo consiste en seguir el flujo de ejecución hasta localizar el **Original Entry Point (OEP)**.

---

## Seguimiento del flujo de ejecución

Durante la ejecución del protector se realizan varias tareas internas:

- Desempaquetado del ejecutable
- Inicialización del entorno protegido
- Comprobaciones anti-debug
- Preparación del entorno de ejecución

Siguiendo la ejecución paso a paso mediante el depurador podremos identificar el momento en el que el protector finaliza su trabajo y transfiere el control al código original del programa.

---

## Localización del OEP

El punto donde el programa original comienza a ejecutarse se denomina **Original Entry Point (OEP)**.

Una vez alcanzado este punto el código que observamos pertenece a la aplicación real y no al protector.

Este momento suele identificarse porque el código adquiere una estructura más clara y aparecen llamadas a funciones habituales del sistema.

---

## Análisis del ejecutable original

Una vez localizado el OEP es posible continuar el análisis del programa original.

En este punto el ejecutable ya se encuentra desempaquetado en memoria, lo que permite estudiar su funcionamiento interno o reconstruir el binario original.

Este procedimiento resulta muy útil para analizar aplicaciones protegidas con protectores comerciales.

---

## Estrategia de análisis

Las estrategias más comunes al analizar aplicaciones protegidas con ASProtect incluyen:

- localizar el OEP y reconstruir el ejecutable original
- analizar las rutinas de validación del registro
- eliminar o modificar las comprobaciones de protección

Dependiendo del objetivo del análisis puede ser suficiente con localizar el punto donde el programa recupera su ejecución normal.

---

## Conclusión

En este tutorial se ha analizado un ejecutable protegido con ASProtect y se ha estudiado el proceso necesario para localizar el Original Entry Point.

Comprender este procedimiento resulta fundamental para el análisis de aplicaciones protegidas con protectores comerciales.

---

Autor: SyXe'05
