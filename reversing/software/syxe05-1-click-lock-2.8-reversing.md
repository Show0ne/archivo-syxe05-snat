# Reversing 1 Click & Lock 2.8
Tutorial original por **SyXe'05**

---

## Información del objetivo

**Programa:** 1 Click & Lock 2.8  
**Tipo:** Shareware  
**Protección:** Serial / Registration check

1 Click & Lock es una utilidad diseñada para bloquear rápidamente el escritorio o ciertas funciones del sistema mediante contraseña.

Como en muchos programas shareware de la época, la versión no registrada presenta limitaciones y muestra avisos de registro.

---

## Análisis inicial

Abrimos el ejecutable en **OllyDbg**.

El primer paso consiste en localizar las cadenas relacionadas con el sistema de registro.

Buscamos referencias como:

Registration
Registered
Unregistered
Please register

En este tipo de programas normalmente existe una comparación que determina si el usuario introdujo un serial válido.

---

## Localización del chequeo

Tras rastrear las referencias a texto relacionadas con el registro encontramos un bloque similar a:

CMP EAX,1
JNE short not_registered

El flujo del programa funciona así:

serial_valid → continuar  
serial_invalid → mensaje de registro

El salto condicional determina si el programa considera el serial válido.

---

## Patch del salto

Podemos modificar la lógica cambiando el salto condicional.

Original:

JNE not_registered

Patch:

JE not_registered

o alternativamente reemplazar el salto por **NOPs**.

---

## Aplicación del patch

En OllyDbg:

1. Localizar la instrucción `JNE`.
2. Editar la instrucción.
3. Cambiarla por `JE` o eliminarla.

Esto provoca que el programa siempre continúe por la rama **registrada**.

---

## Guardar el ejecutable parcheado

Una vez modificado el salto:

Copy to executable → Save file

Guardamos el binario modificado.

---

## Resultado

Al ejecutar el programa parcheado:

- El mensaje de registro desaparece.
- Todas las funciones quedan habilitadas.
- El programa se comporta como versión registrada.

---

## Conclusión

Este tipo de protecciones basadas en comparaciones simples eran comunes en aplicaciones shareware.

El procedimiento general suele ser:

1. Localizar referencias de registro.
2. Encontrar el chequeo lógico.
3. Alterar el flujo de ejecución.

Este ejercicio ilustra un ejemplo básico de bypass de verificación de registro mediante modificación de un salto condicional.

---

**Autor original:** SyXe'05  
**Formato adaptado:** Markdown
