# 542 --- ASProtect 2.0 --- 1st Startup Manager 1.0

  Campo          Detalle
  -------------- ----------------------------------------------
  Programa       1st Startup Manager 1.0
  Protección     ASProtect 2.0 \[Registered\] + Trial 30 días
  Autor          SyXe'05
  Grupo          CracksLatinoS
  Fecha          06-11-2005
  Herramientas   OllyDbg 1.10, ImpRec 1.6, PEiD 0.93

------------------------------------------------------------------------

## Introducción

En este tutorial se analiza cómo desempacar un ejecutable protegido con
**ASProtect 2.0 \[Registered\]** utilizando como ejemplo el programa
**1st Startup Manager 1.0**.

El objetivo es:

-   Obtener el **OEP**
-   Analizar el mecanismo de redirección de **APIs**
-   Reparar los **CALL redirigidos**
-   Realizar el **dump del ejecutable**
-   Reconstruir la **IAT**
-   Eliminar la limitación del **Trial**

------------------------------------------------------------------------

## Identificación de la protección

Con **PEiD** comprobamos que el ejecutable está empaquetado con:

ASProtect 2.0 \[Registered\]

Abrimos el programa en **OllyDbg** y ocultamos el debugger mediante el
plugin `IsDebuggerPresent` o parcheando el chequeo correspondiente.

------------------------------------------------------------------------

## Obtención del OEP

Usamos el método clásico de **excepciones** para localizar el OEP.

Después de superar la última excepción llegamos a:

OEP = 00401240

En el código aparece una llamada importante:

CALL 00F40004

Esta llamada será clave para entender cómo **ASProtect redirige las
APIs**.

------------------------------------------------------------------------

## Análisis del mecanismo de redirección

ASProtect intercepta llamadas a APIs y las redirige hacia código del
packer.

Para detectar dónde se generan:

1.  Seguimos los bytes del CALL.
2.  Colocamos un **Hardware Breakpoint on Write**.
3.  Reiniciamos el programa.

Esto permite localizar la rutina que parchea dichas llamadas.

Durante el análisis se observa un loop que procesa todas las llamadas
redirigidas.

------------------------------------------------------------------------

## Resolución de APIs

El packer:

1.  Localiza la DLL correspondiente
2.  Resuelve la API
3.  Copia parte de su código
4.  Crea trampolines en memoria

Ejemplo observado:

CreateSemaphoreA

ASProtect copia parte del código de la API mediante:

REP MOVS

y crea una zona ejecutable con:

VirtualAlloc

donde se ejecutará el código copiado.

------------------------------------------------------------------------

## Reparación de CALLs

Cada CALL redirigido debe sustituirse por una llamada directa a la
**IAT**.

Ejemplo:

Original:

CALL 00F20004

Reparado:

CALL DWORD PTR \[465634\]

donde `465634` corresponde a la dirección de la API en la IAT.

------------------------------------------------------------------------

## CALL vs JMP

No todas las entradas deben repararse como CALL.

Regla:

-   **CALL** cuando la API es invocada directamente
-   **JMP** cuando forma parte de una **Jump Table**

Ejemplo:

CALL 401210 401210 JMP DWORD PTR \[IAT\]

El CALL previo mantiene la dirección de retorno en la pila.

------------------------------------------------------------------------

## Dump del ejecutable

Una vez reparadas las llamadas se realiza el dump con **OllyDump**.

Antes de hacerlo debemos pulsar:

Get EIP as OEP

para que el OEP sea correcto.

------------------------------------------------------------------------

## Reconstrucción de la IAT

Utilizamos **Import Reconstructor (ImpRec)**.

Parámetros utilizados:

OEP = 1240 IAT RVA = 654C8 Size = 3B8

Después:

Get Imports Fix Dump

ImpRec genera el ejecutable final con la IAT reconstruida.

------------------------------------------------------------------------

## Resultado

El ejecutable resultante funciona correctamente y el **Trial
desaparece**, ya que la limitación temporal estaba gestionada por
ASProtect.

------------------------------------------------------------------------

## Eliminación del Time Trial

El control del Trial depende de la variable:

\[EBP-9\]

Su valor inicial es:

0

Si se cambia a:

1

la comparación posterior no activará la rutina de expiración.

------------------------------------------------------------------------

## Conclusión

Se ha demostrado cómo:

-   Analizar el funcionamiento interno de **ASProtect 2.0**
-   Obtener el **OEP**
-   Reparar manualmente los CALL redirigidos
-   Reconstruir la **IAT**
-   Eliminar la limitación de **Trial**

Aunque existen métodos automatizados mediante scripts, el enfoque manual
permite comprender en profundidad el funcionamiento del packer.

------------------------------------------------------------------------

**Autor:** SyXe'05\
**Grupo:** CracksLatinoS\
**Contacto:** syxe00@yahoo.es
