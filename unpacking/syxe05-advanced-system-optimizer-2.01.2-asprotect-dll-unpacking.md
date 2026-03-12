# Advanced System Optimizer 2.01.2 – ASProtect en una DLL

Autor: SyXe'05  
Tipo: Unpacking tutorial  
Protección: ASProtect  
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analizará un caso particular de protección mediante **ASProtect**, aplicado no al ejecutable principal sino a una **DLL**.

El ejemplo utilizado será **Advanced System Optimizer 2.01.2**, donde una de las bibliotecas del programa se encuentra protegida mediante ASProtect.

El objetivo del análisis será comprender el proceso de carga de la DLL protegida y localizar el **Original Entry Point (OEP)** para poder estudiar el código original.

---

## Preparación

Ejecutamos el programa y cargamos **SoftICE** para comenzar el análisis dinámico.

Cuando una DLL protegida es cargada por el programa principal, el sistema utiliza funciones del sistema como:

LoadLibraryA  
GetProcAddress  

Estas funciones suelen ser buenos puntos de partida para comenzar el análisis.

---

## Breakpoints iniciales

Colocamos breakpoints en funciones relacionadas con la carga de bibliotecas dinámicas:

bpx LoadLibraryA  
bpx GetProcAddress

Cuando el programa cargue la DLL protegida podremos interceptar el proceso de inicialización de la biblioteca.

---

## Seguimiento de la ejecución

Una vez que SoftICE intercepte la llamada correspondiente continuamos la ejecución paso a paso.

Durante esta fase se ejecutará el código perteneciente al **stub de ASProtect**, que se encarga de preparar el entorno antes de transferir el control al código original.

Este código suele incluir diferentes comprobaciones internas del protector.

---

## Localización del OEP

El objetivo consiste en localizar el momento en el que el protector transfiere el control al código real de la DLL.

Este punto se conoce como **Original Entry Point (OEP)**.

El OEP suele identificarse porque el código empieza a mostrar una estructura más clara y aparecen llamadas habituales a funciones del sistema.

---

## Análisis del código original

Una vez localizado el OEP es posible continuar el análisis de la DLL original.

En este punto el código ya se encuentra desempaquetado en memoria y puede estudiarse con herramientas de análisis estático o dinámico.

Este procedimiento permite comprender el funcionamiento interno de la biblioteca protegida.

---

## Estrategia de análisis

Al analizar protecciones como ASProtect aplicadas a DLLs pueden utilizarse varias estrategias:

- localizar el OEP y reconstruir la DLL original  
- analizar las rutinas de protección implementadas por el protector  
- estudiar las funciones exportadas por la biblioteca

Dependiendo del objetivo del análisis puede ser suficiente con localizar el punto donde la DLL comienza a ejecutar su código original.

---

## Conclusión

En este tutorial se ha analizado una DLL protegida con **ASProtect** utilizando como ejemplo **Advanced System Optimizer 2.01.2**.

Mediante el uso de herramientas clásicas de reversing como **SoftICE** y **W32Dasm** es posible seguir el flujo de ejecución hasta localizar el **Original Entry Point** del código protegido.

Comprender este proceso resulta fundamental para analizar aplicaciones protegidas mediante sistemas de protección comerciales.

---

Autor: SyXe'05
