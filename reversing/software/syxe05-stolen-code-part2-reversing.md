# Primer acercamiento al Stolen Code (Parte 2) - Reversing Tutorial

Autor: SyXe'05  
Categoría: Reversing / Protectores / Técnicas

## PDF original

Primer_acercamiento_al_Stolen_Code_parte_2 - [por SyXe'05].pdf

---

## Introducción

Este documento continúa el análisis iniciado en **Primer acercamiento al Stolen Code (Parte 1)**.

En esta segunda parte se estudia cómo esta técnica afecta al proceso de **unpacking** y cómo identificar el flujo de ejecución real del programa cuando el código original ha sido desplazado o modificado por el protector.

---

## Problema del Stolen Code

Cuando un protector utiliza esta técnica:

- Las primeras instrucciones del programa pueden no corresponder al código original.
- Parte del código original puede ejecutarse desde otra región de memoria.
- El flujo del programa aparenta ser distinto al real.

Esto complica tareas habituales del reverser como:

- localizar el **OEP**
- reconstruir el binario original
- seguir el flujo lógico del programa

---

## Análisis en el debugger

Durante el debugging se deben observar:

- saltos hacia zonas inesperadas de memoria
- instrucciones que parecen pertenecer al código original pero ejecutadas fuera de contexto
- cambios en el flujo inmediatamente antes de llegar al OEP

Herramientas utilizadas:

- **OllyDbg**
- **PE Tools**
- **Editor hexadecimal**

---

## Estrategia de análisis

Para tratar con código robado se recomienda:

1. Seguir el flujo del stub del protector.
2. Identificar las instrucciones que pertenecen al código original.
3. Localizar los saltos que redirigen la ejecución.
4. Reconstruir mentalmente el flujo original del programa.

En muchos casos el protector ejecuta:

- código del stub
- fragmentos del código original
- restauración del contexto
- salto final al OEP

---

## Reconstrucción del flujo original

Una vez identificados los fragmentos desplazados del programa:

- se puede reconstruir el flujo lógico original
- se identifica el punto donde el protector transfiere el control al código real

Ese punto corresponde al **Original Entry Point (OEP)**.

---

## Conclusión

La técnica **Stolen Code** es una forma sencilla pero efectiva de dificultar el análisis de un ejecutable protegido.

Comprender cómo funciona permite al reverser:

- identificar código desplazado
- reconstruir el flujo real del programa
- localizar el OEP con mayor facilidad

Este tipo de técnicas son habituales en protectores clásicos como:

- Armadillo
- ASProtect
- protectores personalizados

---

Repositorio:

https://github.com/Show0ne/archivo-syxe05-snat
