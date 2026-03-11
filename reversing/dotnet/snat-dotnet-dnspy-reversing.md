# Jugando con un .NET en dnSpy – Análisis

Autor: SNAT  
Categoría: Reversing / .NET

## PDF original

Jugando con un .NET en dnSpy.pdf

---

## Introducción

Este documento presenta un análisis básico de una aplicación **.NET** utilizando la herramienta **dnSpy**.

A diferencia de los ejecutables nativos de Windows, los programas desarrollados en **.NET** contienen código intermedio llamado **IL (Intermediate Language)**.  
Este código puede descompilarse fácilmente a C# o VB.NET mediante herramientas de ingeniería inversa.

El objetivo del tutorial es mostrar cómo:

- Analizar un ejecutable .NET
- Explorar su estructura interna
- Comprender la lógica del programa

---

## Herramientas utilizadas

- dnSpy
- ILSpy (alternativa)
- Editor hexadecimal (opcional)

---

## Cargando el ejecutable en dnSpy

Para comenzar el análisis:

1. Abrir **dnSpy**.
2. Cargar el ejecutable .NET dentro de la aplicación.
3. Explorar los ensamblados y namespaces del programa.

dnSpy permite navegar por:

- Clases
- Métodos
- Propiedades
- Recursos

Además, el código puede visualizarse directamente en **C#** gracias a su descompilador integrado.

---

## Explorando el código

Una vez cargado el ejecutable se puede:

- Analizar la estructura de clases
- Identificar métodos importantes
- Revisar la lógica del programa

dnSpy permite cambiar entre:

- Vista de **IL**
- Código **C# descompilado**

Esto facilita enormemente el proceso de análisis.

---

## Modificación del programa

Una característica potente de **dnSpy** es la posibilidad de modificar el código.

El flujo habitual consiste en:

1. Editar el método deseado.
2. Modificar la lógica del programa.
3. Compilar los cambios.
4. Guardar el ensamblado modificado.

Esto permite alterar el comportamiento del programa directamente.

---

## Conclusión

Las aplicaciones **.NET** son generalmente más fáciles de analizar que los ejecutables nativos.

Herramientas como **dnSpy** permiten:

- Descompilar el código
- Comprender la lógica del programa
- Modificar directamente los métodos

Por esta razón, muchos desarrolladores aplican **obfuscadores** para dificultar la ingeniería inversa en aplicaciones .NET.

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
