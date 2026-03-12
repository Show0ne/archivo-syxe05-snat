# GoLive CS – ASProtect Unpacking

Autor: SyXe'05
Tipo: Unpacking tutorial
Protección: ASProtect
Herramientas: SoftICE, W32Dasm

---

## Introducción

En este tutorial se analizará un ejecutable protegido con APSProtect utilizando como ejemplo el programa Adobe GoLive CS.

ASProtect es uno de los protectores comerciales más utilizados en aplicaciones shareware y comerciales. Su funcionamiento consiste en proteger el ejecutable original mediante una capa de control que introduce diferentes mecanismos de protección.

El objetivo del análisis será localizar el Original Entry Point (OEP) del ejecutable protegido para poder estudiar el programa original.

---

## Preparación
Ejecutamos el programa protegido y cargamos SoftICE para comenzar el análisis dinámico.

En aplicaciones protegidas con APSProtect es habitual comenzar colocando breakpoints en funciones relacionadas con la carga de módulos o la transferencia de control al código real del programa.

---

## Breakpoints iniciales

Por ejemplo:

bpx GetProcAddress
bpx LoadLibraryA

Estas funciones suelen utilizarse durante el proceso de inicialización del protector y pueden ayudar identificar el momento en el que la ejecución pasa al código real del programa.

---

## Conclusión

En este tutorial se ha analizado un ejecutable protegido con ASProtect y se ha estudiado el proceso necesario para localizar el Original Entry Point.

Comprender este procedimiento resulta fundamental para el análisis de aplicaciones protegidas con protectores comerciales.

---

Tutorial original: SyXe'05
