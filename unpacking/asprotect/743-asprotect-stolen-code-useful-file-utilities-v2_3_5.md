# 743 --- ASProtect 1.2x--1.3x --- Stolen Code --- Useful File Utilities v2.3.5

  -----------------------------------------------------------------------
  Campo                               Valor
  ----------------------------------- -----------------------------------
  Programa                            Useful File Utilities v2.3.5

  Protección                          ASProtect v1.2x -- 1.3x
                                      \[Registered\]

  Técnica                             Stolen Code

  Autor                               SyXe'05

  Grupo                               CracksLatinoS

  Fecha                               20-08-2006

  Herramientas                        OllyDbg 1.10, PEiD 0.93, ImpREC
                                      1.6, ConTEXT 0.98, Hex Workshop
                                      4.23, PEditor 1.7, LordPE Deluxe,
                                      ToPo 1.2
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Introducción

Este tutorial muestra cómo desempacar una aplicación protegida con
**ASProtect 1.2x--1.3x** utilizando la técnica conocida como **Stolen
Code**.

El programa utilizado como ejemplo es:

Useful File Utilities v2.3.5

El objetivo es recuperar el ejecutable original completamente funcional.

------------------------------------------------------------------------

## ¿Qué es Stolen Code?

El **Stolen Code (SCode)** es una técnica utilizada por algunos packers
en la que parte del código original del programa es eliminado del
ejecutable y ejecutado desde memoria en tiempo de ejecución.

En lugar de comenzar con instrucciones típicas como:

PUSH EBP\
MOV EBP, ESP\
CALL GetModuleHandleA

el packer ejecuta bloques completos del código fuera del ejecutable.

Esto complica:

-   la localización del OEP
-   la reconstrucción del flujo de ejecución
-   la reparación de la IAT

------------------------------------------------------------------------

## Identificación de la protección

PEiD identifica el ejecutable como:

ASProtect 1.2x -- 1.3x \[Registered\]

El programa contiene varios archivos:

BatchReplacer.exe\
Useful File Utilities.exe\
BatchReplacer.plgn

El ejecutable protegido es **Useful File Utilities.exe**.

------------------------------------------------------------------------

## Anti‑debug

El programa utiliza la comprobación:

IsDebuggerPresent

ubicada en:

\[ebx+2\] → 7FFDF002

Puede bypassarse modificando el byte correspondiente o utilizando un
plugin anti‑anti‑debug en OllyDbg.

------------------------------------------------------------------------

## Localización del Stolen Code

Durante el análisis se observa que parte del código se ejecuta fuera del
ejecutable en la región de memoria:

014C0000

Esto confirma el uso de Stolen Code.

El flujo contiene llamadas como:

CALL 019C0000

que posteriormente ejecutan APIs del sistema y regresan al flujo
principal.

------------------------------------------------------------------------

## Secciones implicadas

El SCode utiliza varias regiones de memoria:

01290000 tamaño 2C000h\
012C0000 tamaño 4000h\
012D8000 tamaño 4000h\
014C0000 tamaño 16000h\
0012C000 stack

Estas secciones deben ser copiadas posteriormente al ejecutable
desempaquetado.

------------------------------------------------------------------------

## Restauración de la IAT

ASProtect modifica la IAT para impedir el dumpeado directo del
ejecutable.

Los saltos típicos tienen la forma:

FF25

Para capturar las APIs correctas se colocan breakpoints en escritura
sobre la sección de código.

De esta forma se obtiene:

-   API real
-   posición del salto
-   dirección de la entrada en la IAT

------------------------------------------------------------------------

## Dump del ejecutable

Una vez reconstruidas las tablas:

1.  detener en el OEP
2.  usar Import Reconstructor
3.  reconstruir la IAT

El ejecutable dumpeado se guarda como:

tute.exe

------------------------------------------------------------------------

## Inyección del Stolen Code

Después del dump es necesario copiar al ejecutable varias regiones de
memoria que contienen el código robado.

Ejemplo:

02F20000 → 004DC000\
02F30000 → 004DE000

Posteriormente se copian otras secciones adicionales desde el ejecutable
original.

------------------------------------------------------------------------

## Creación de nueva sección

Con **ToPo v1.2** se crea una nueva sección en el ejecutable para alojar
el código robado y las tablas auxiliares.

Esto permite almacenar:

-   Stolen Code
-   stack necesario
-   Init Table
-   Deinit Table

------------------------------------------------------------------------

## Init Table

El programa contiene una tabla de inicialización con múltiples
funciones.

Durante el análisis se extraen todas las direcciones de estas funciones
y se reconstruye una nueva tabla dentro del ejecutable desempaquetado.

El contador del loop se ajusta para ejecutar:

105 funciones.

------------------------------------------------------------------------

## Deinit Table

También existe una tabla de desinicialización que se ejecuta cuando el
programa termina.

Se aplica el mismo procedimiento:

-   capturar direcciones
-   reconstruir la tabla
-   redirigir la ejecución hacia la nueva tabla

------------------------------------------------------------------------

## Resultado

Después de:

-   reparar la IAT
-   reconstruir la JMP Table
-   inyectar el Stolen Code
-   reconstruir Init y Deinit Tables

el ejecutable funciona correctamente sin el packer.

El programa inicia normalmente y todas sus funciones operan sin errores.

------------------------------------------------------------------------

Autor: SyXe'05\
Grupo: CracksLatinoS\
Contacto: syxe05@gmail.com
