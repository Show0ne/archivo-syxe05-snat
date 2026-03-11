# SVKP v1.3x - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Software Protection

## PDF original

SVKP v1.3x_con_Trucos__por_SyXe'05.pdf

---

## Introducción

En este tutorial se analiza la protección **SVKP v1.3x**, un protector shareware bastante utilizado en aplicaciones de la época.

SVKP implementa diferentes mecanismos destinados a dificultar el análisis del ejecutable, incluyendo técnicas de ofuscación y verificación interna del flujo de ejecución.

El objetivo del análisis es estudiar el comportamiento del protector y comprender cómo interactúa con el ejecutable protegido.

---

## Herramientas utilizadas

- OllyDbg
- PE Tools
- Editor hexadecimal

---

## Análisis de la protección

Durante el análisis del ejecutable se observan varios comportamientos característicos del protector **SVKP**:

- código inicial del protector antes del OEP
- múltiples saltos condicionales
- modificaciones del flujo de ejecución
- rutinas internas de verificación

Estas técnicas están destinadas a dificultar la localización del **Original Entry Point (OEP)** y complicar el análisis estático del programa.

---

## Flujo de ejecución

Mediante el análisis dinámico con un debugger es posible seguir la ejecución del programa y observar cómo el protector transfiere finalmente el control al código real de la aplicación.

Durante este proceso se identifican:

- rutinas de inicialización del protector
- verificaciones internas
- redirecciones del flujo de ejecución

---

## Observaciones

SVKP utiliza técnicas simples pero efectivas para entorpecer el análisis del ejecutable.

Aunque no introduce virtualización de código como protectores más modernos, sí emplea ofuscación y modificaciones del flujo de ejecución que pueden dificultar el reversing inicial.

---

## Resultado

Tras analizar el comportamiento del protector es posible comprender la estructura general del ejecutable protegido y localizar el punto donde el control es transferido al programa original.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
