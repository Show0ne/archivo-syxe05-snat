# Armadillo 3.xx — CubisGold

Autor: SyXe'05
Tipo: Reversing tutorial
Protección: Armadillo 3.xx
Herramientas: SoftICE, W32Dasm, editor hexadecimal

---

## Introducción

En este tutorial se analiza la protección Armadillo 3.xx aplicada al programa CubisGold.

Armadillo fue durante muchos años uno de los sistemas de protección comercial más utilizados para proteger aplicaciones shareware.

El objetivo de este tutorial es estudiar el funcionamiento de esta protección y comprender cómo localizar el punto donde el programa recupera su ejecución normal.

---

## Información del programa

Programa: CubisGold  
Protección: Armadillo 3.xx  
Tipo de protección: Compresión + control de registro

La protección Armadillo introduce múltiples mecanismos de defensa:

- compresión del ejecutable
- verificación de integridad
- detección de depuradores
- control del flujo de ejecución

---

## Primer análisis

Al ejecutar el programa bajo un depurador observamos que el ejecutable se encuentra protegido por Armadillo.

El código inicial del programa no pertenece a la aplicación original sino al **loader de la protección**.

Esto significa que primero debemos seguir el flujo de ejecución hasta encontrar el punto donde el programa real comienza a ejecutarse.

---

## Localización del OEP

Uno de los objetivos principales al analizar ejecutables protegidos con Armadillo consiste en localizar el **Original Entry Point (OEP)**.

El OEP corresponde al punto donde comienza el código original de la aplicación.

Para localizarlo utilizamos SoftICE y seguimos el flujo de ejecución paso a paso.

Durante el proceso es habitual observar múltiples rutinas relacionadas con:

- desempaquetado del código
- comprobaciones de integridad
- detección de depuradores

Una vez finalizado el proceso de desempaquetado la ejecución saltará finalmente al código original del programa.

---

## Análisis del flujo

Siguiendo la ejecución del programa podremos observar cómo la protección transfiere el control al código real de la aplicación.

En este punto ya es posible analizar el comportamiento normal del programa.

El OEP suele identificarse por la aparición de código más estructurado y llamadas a funciones del sistema o bibliotecas habituales.

---

## Estrategia de reversing

Existen varias estrategias posibles para analizar aplicaciones protegidas con Armadillo.

Las más comunes son:

- localizar el OEP y reconstruir el ejecutable original
- analizar las rutinas de verificación de registro
- parchear el ejecutable para eliminar las comprobaciones

Dependiendo del objetivo del análisis puede ser suficiente con identificar el punto donde el programa recupera su ejecución normal.

---

## Conclusión

En este tutorial se ha estudiado la protección Armadillo 3.xx aplicada al programa CubisGold.

Utilizando herramientas clásicas de reversing como SoftICE y W32Dasm es posible seguir el flujo de ejecución hasta localizar el punto donde el programa original comienza a ejecutarse.

Comprender este proceso resulta fundamental para analizar aplicaciones protegidas con sistemas de protección comerciales.

---

Autor: SyXe'05
