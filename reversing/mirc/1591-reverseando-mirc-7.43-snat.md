# 1591 — Reverseando mIRC 7.43

| Campo | Valor |
|------|------|
| Aplicación | mIRC 7.43 |
| Tipo | Reverse Engineering |
| Autor | SNAT |
| Grupo | CracksLatinoS |
| Año | ~2016 |

PDF original: **Reverseando mIRC 7.43.pdf**

---

## Introducción

Este tutorial describe el proceso de análisis y reversing de la aplicación **mIRC 7.43**.
A diferencia de otros documentos del repositorio, este trabajo no se centra en
un packer concreto sino en el análisis directo de una aplicación real.

mIRC es uno de los clientes IRC más populares para Windows y ha sido utilizado
durante décadas. El objetivo del tutorial es estudiar su funcionamiento interno
y comprender determinados mecanismos de registro y protección del software.

---

## Herramientas utilizadas

Durante el proceso de análisis se emplean herramientas clásicas de reversing:

- **OllyDbg**
- **IDA Pro**
- **PEiD**
- **Import Reconstructor (ImpREC)**

Estas herramientas permiten analizar el flujo de ejecución del programa,
localizar funciones relevantes y estudiar la lógica interna del binario.

---

## Análisis inicial

El primer paso consiste en analizar el ejecutable para determinar:

- compilador utilizado
- estructura del binario
- presencia de protecciones

Tras el análisis preliminar se procede a ejecutar el programa bajo debugger
para observar su comportamiento en tiempo de ejecución.

---

## Seguimiento del flujo de ejecución

Utilizando el debugger se siguen las funciones relacionadas con:

- verificación de licencia
- inicialización del programa
- manejo de cadenas y claves

Esto permite identificar los puntos críticos donde el programa valida
su estado de registro.

---

## Localización de la rutina de verificación

Durante el análisis se identifica la función encargada de comprobar
la validez del registro.

Analizando esta rutina es posible comprender:

- cómo se validan los datos del usuario
- qué condiciones determinan si el programa está registrado

---

## Modificación del flujo

Una vez localizada la rutina de verificación, el tutorial explica
cómo modificar el flujo de ejecución para evitar la comprobación
de licencia.

Esto se consigue mediante:

- modificación de saltos condicionales
- parcheo del binario

---

## Resultado

Tras aplicar las modificaciones necesarias el programa puede ejecutarse
sin las restricciones impuestas por el sistema de registro.

Este proceso demuestra cómo el análisis del flujo de ejecución permite
comprender y modificar el comportamiento de una aplicación.

---

## Conclusión

El tutorial muestra un ejemplo práctico de **reversing aplicado a software real**.

Las técnicas utilizadas incluyen:

- análisis estático
- debugging dinámico
- localización de rutinas críticas
- parcheo del ejecutable

---

Autor: **SNAT**  
Grupo: **CracksLatinoS**
