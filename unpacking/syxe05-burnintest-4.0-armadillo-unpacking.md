# BurnInTest 4.0 – Armadillo sencillo

Autor: SyXe'05  
Tipo: Unpacking tutorial  
Protección: Armadillo 4.0  
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analizará un ejecutable protegido con **Armadillo 4.0** utilizando como ejemplo el programa **BurnInTest 4.0**.

Armadillo es uno de los protectores comerciales más conocidos utilizados para proteger aplicaciones shareware y comerciales. Su funcionamiento consiste en envolver el ejecutable original dentro de un stub de protección que controla la ejecución del programa.

El objetivo del análisis será localizar el **Original Entry Point (OEP)** del programa protegido para poder estudiar el ejecutable original.

---

## Preparación

Ejecutamos el programa protegido y cargamos **SoftICE** para comenzar el análisis dinámico.

Al trabajar con protectores como Armadillo es habitual comenzar colocando breakpoints en funciones relacionadas con la gestión de memoria o con la transferencia de control al programa original.

---

## Colocación de breakpoints

Un método habitual consiste en colocar breakpoints en funciones utilizadas durante el proceso de desempaquetado.

Por ejemplo:

bpx GetProcAddress  
bpx LoadLibraryA

Estas funciones suelen aparecer durante el proceso de inicialización del protector y pueden ayudar a identificar el momento en el que el control pasa al código real del programa.

---

## Seguimiento de la ejecución

Una vez colocado el breakpoint ejecutamos el programa hasta que SoftICE intercepte alguna de estas llamadas.

A partir de ese momento continuamos la ejecución paso a paso observando cómo evoluciona el flujo del programa.

Durante este proceso es habitual encontrar código perteneciente al propio protector Armadillo que se encarga de realizar comprobaciones internas y preparar el entorno de ejecución.

---

## Localización del OEP

El objetivo principal consiste en localizar el momento en el que el protector transfiere el control al ejecutable original.

Este punto se conoce como **Original Entry Point (OEP)**.

Normalmente puede identificarse porque el código empieza a mostrar una estructura más clara y aparecen llamadas habituales a funciones del sistema o de bibliotecas utilizadas por la aplicación.

---

## Análisis del ejecutable original

Una vez localizado el OEP es posible continuar el análisis del ejecutable original.

En este punto el programa ya se encuentra desempaquetado en memoria, lo que permite estudiar su funcionamiento interno o reconstruir el ejecutable original.

Este procedimiento es habitual al analizar aplicaciones protegidas con protectores comerciales.

---

## Estrategia de análisis

Las estrategias más comunes al analizar aplicaciones protegidas con Armadillo incluyen:

- localizar el OEP y reconstruir el ejecutable original  
- analizar las rutinas de validación de registro  
- parchear el ejecutable para eliminar comprobaciones

Dependiendo del objetivo del análisis puede ser suficiente con localizar el punto donde el programa recupera su ejecución normal.

---

## Conclusión

En este tutorial se ha analizado un ejecutable protegido con **Armadillo 4.0** utilizando como ejemplo el programa **BurnInTest 4.0**.

Mediante el uso de herramientas clásicas de reversing como **SoftICE** y **W32Dasm** es posible seguir el flujo de ejecución hasta localizar el **Original Entry Point** del programa.

Comprender este procedimiento resulta fundamental para el análisis de aplicaciones protegidas con sistemas de protección comerciales.

---

Autor: SyXe'05
