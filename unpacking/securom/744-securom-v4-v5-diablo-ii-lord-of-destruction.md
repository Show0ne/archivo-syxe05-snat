# 744 --- SecuROM v4.x.x.x -- 5.x.x.x --- Diablo II: Lord of Destruction

  -----------------------------------------------------------------------
  Campo                               Valor
  ----------------------------------- -----------------------------------
  Programa                            Diablo II -- Lord of Destruction

  Protección                          SecuROM v4.x.x.x -- 5.x.x.x

  Autor                               SyXe'05

  Grupo                               CracksLatinoS

  Fecha                               05‑02‑2006

  Herramientas                        OllyDbg 1.10, PEiD 0.92, ImpREC
                                      1.6, DAEMON Tools 3.44, ConTEXT
                                      0.98, Hex Workshop 4.23, PEditor
                                      1.7, LordPE Deluxe
  -----------------------------------------------------------------------

PDF original: **Diablo II_Lord of Destruction.pdf**

------------------------------------------------------------------------

# Introducción

En este tutorial se analiza la protección **SecuROM v4 / v5**, muy
utilizada en juegos comerciales distribuidos en CD. El estudio se
realiza sobre el ejecutable del juego:

Diablo II --- expansión *Lord of Destruction*.

El objetivo es:

-   analizar la protección
-   localizar el OEP
-   reconstruir el ejecutable
-   eliminar la dependencia del CD original.

------------------------------------------------------------------------

# Identificación de la protección

Usando **PEiD** se detecta la protección:

SecuROM v4.x.x.x -- 5.x.x.x (Sony DADC).

Este sistema introduce varias técnicas de protección:

-   CD‑check
-   uso intensivo de excepciones
-   manipulación del SEH
-   redirección de llamadas API

Cuando el programa se ejecuta sin el CD original aparece el típico
mensaje de error solicitando el disco.

------------------------------------------------------------------------

# Comprobación de CD

SecuROM utiliza una verificación del disco en la unidad óptica.

Si el CD original no está presente el programa no se ejecuta.

Una forma de evitar temporalmente esta comprobación es utilizando
**DAEMON Tools** con emulación SecuROM.

Esto permite ejecutar el programa y continuar el análisis.

------------------------------------------------------------------------

# Análisis en OllyDbg

Al cargar el ejecutable en OllyDbg se observa un comportamiento basado
en excepciones.

El packer provoca:

-   **INTEGER_DIVISION_BY_ZERO**
-   **ACCESS_VIOLATION**

Estas excepciones se repiten dentro de loops y dificultan el uso de
breakpoints.

También se detecta manipulación de los registros de depuración:

DR0 -- DR3

lo que impide el uso de hardware breakpoints.

------------------------------------------------------------------------

# Búsqueda del OEP

Debido a la protección no es posible usar métodos tradicionales como:

-   breakpoints
-   hardware breakpoints
-   memory breakpoints

Una estrategia alternativa consiste en poner breakpoints en APIs comunes
invocadas poco después del OEP.

Por ejemplo:

-   GetVersion
-   GetCommandLineA
-   GetModuleHandleA

Colocando un breakpoint en **GetVersion** se consigue finalmente
localizar el retorno hacia el código del programa original.

El OEP real se encuentra en:

00402330

------------------------------------------------------------------------

# Análisis de la tabla de llamadas

Tras localizar el OEP se detecta una tabla de llamadas redirigidas por
SecuROM.

Las instrucciones tienen forma similar a:

CALL \[XXXXXX\]

Estas llamadas no apuntan directamente a APIs sino a rutinas internas
del packer.

Dentro de estas rutinas se accede a una sección de memoria:

013B0000

que contiene los valores necesarios para resolver la API real.

------------------------------------------------------------------------

# Reconstrucción de llamadas

Se detectan aproximadamente:

193 llamadas

que deben ser reparadas.

Para automatizar el proceso se crea una tabla con todas las direcciones
de los CALL a reparar.

Esta tabla se inserta posteriormente dentro del ejecutable en memoria.

------------------------------------------------------------------------

# Script de reparación

Se implementa un script (por ejemplo con **OllyScript**) que realiza:

1.  recorrer la tabla de calls
2.  ejecutar cada call
3.  obtener la API real
4.  localizarla en la IAT
5.  reconstruir la llamada correctamente

De esta forma las llamadas dejan de apuntar a código del packer y pasan
a apuntar directamente a la API original.

------------------------------------------------------------------------

# Dump del ejecutable

Una vez reparadas las llamadas:

1.  situarse en el OEP
2.  usar el dumper de OllyDbg
3.  guardar el ejecutable (ej: tute.exe)

Posteriormente se utiliza **Import Reconstructor** para reconstruir la
IAT.

El ejecutable resultante queda totalmente funcional.

------------------------------------------------------------------------

# Eliminación de secciones innecesarias

Después del dump se observan varias secciones creadas por el packer:

.cms_s\
.cms_d\
.idata

Estas secciones pueden eliminarse.

Posteriormente se reconstruye el ejecutable con **LordPE** para reducir
su tamaño.

------------------------------------------------------------------------

# Resultado final

El ejecutable final:

-   funciona sin SecuROM
-   no requiere el CD original
-   tiene un tamaño mucho menor

El tamaño pasa aproximadamente de:

414 KB → 78 KB

lo que representa una reducción de más del 80%.

------------------------------------------------------------------------

# Conclusión

Este estudio muestra cómo desempacar una protección **SecuROM v4/v5**
utilizando técnicas de:

-   análisis de excepciones
-   localización manual del OEP
-   reconstrucción automática de llamadas API
-   reconstrucción de la IAT

El resultado es un ejecutable completamente funcional sin la protección.

------------------------------------------------------------------------

Autor: **SyXe'05**\
Grupo: **CracksLatinoS**\
Contacto: syxe05@gmail.com
