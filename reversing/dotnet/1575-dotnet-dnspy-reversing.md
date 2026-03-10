# 1575 — Jugando con un .NET en dnSpy

| Campo | Valor |
|------|------|
| Plataforma | .NET |
| Herramienta | dnSpy |
| Autor | SNAT |
| Grupo | CracksLatinoS |

PDF original: **Jugando con un .NET en dnSpy.pdf**

---

## Introducción

Este tutorial muestra cómo analizar aplicaciones **.NET** utilizando la herramienta **dnSpy**.
A diferencia de los binarios nativos, los programas .NET contienen código intermedio
(CIL/IL) que puede decompilarse con relativa facilidad a un lenguaje de alto nivel
como C#.

El objetivo del documento es explicar cómo explorar ensamblados .NET,
analizar su lógica interna y modificar el comportamiento del programa.

---

## Herramientas utilizadas

Durante el análisis se utilizan herramientas como:

- **dnSpy**
- **PEiD**
- **Debugger integrado de dnSpy**

dnSpy es una herramienta muy potente para reversing de aplicaciones .NET,
ya que permite:

- decompilar assemblies
- navegar por clases y métodos
- depurar el programa
- editar y recompilar métodos directamente

---

## Explorando el ensamblado

Al abrir el ejecutable en **dnSpy** se puede observar la estructura del assembly:

- namespaces
- clases
- métodos
- recursos

Esto permite localizar rápidamente funciones relevantes del programa.

---

## Análisis del código

Una vez identificado el método que nos interesa, dnSpy permite visualizar
el código en distintos formatos:

- C#
- IL (Intermediate Language)

Esto facilita entender la lógica interna del programa.

---

## Depuración

dnSpy incluye un debugger integrado que permite:

- colocar breakpoints
- inspeccionar variables
- seguir el flujo de ejecución

Esto resulta muy útil para comprender cómo se ejecuta el programa en tiempo real.

---

## Modificación del código

Una de las características más interesantes de dnSpy es la posibilidad de
**editar métodos directamente**.

El proceso consiste en:

1. localizar el método a modificar
2. editar el código C#
3. recompilar el método
4. guardar el ejecutable modificado

---

## Conclusión

dnSpy es una herramienta extremadamente útil para el reversing de aplicaciones
.NET.

Permite combinar:

- análisis estático
- depuración dinámica
- modificación del código

todo dentro de una misma interfaz.

---

Autor: **SNAT**  
Grupo: **CracksLatinoS**
