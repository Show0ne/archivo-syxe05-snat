# Reversing DVD Region+CSS Free 5.9.6.8 (Part 2)
Tutorial original por **SyXe'05**

Protección analizada: **ASProtect 1.2x – 1.3x (TimeTrial)**

---

## Introducción

En este tutorial continuamos el análisis del programa **DVD Region+CSS Free 5.9.6.8**, protegido mediante **ASProtect**.

El objetivo es comprender cómo funciona el sistema **TimeTrial** implementado por ASProtect y cómo el programa controla el periodo de evaluación.

Este tipo de protección fue muy común en aplicaciones shareware de principios de los 2000.

---

## Herramientas utilizadas

Para el análisis utilizamos:

- OllyDbg
- W32Dasm
- Import Reconstructor
- PE tools

Estas herramientas permiten analizar el flujo del programa y localizar los chequeos relacionados con el periodo de prueba.

---

## Análisis inicial

Al ejecutar el programa observamos que funciona en **modo trial**.

El sistema de protección muestra información sobre:

- número de ejecuciones
- tiempo restante del trial
- restricciones en funcionalidades

ASProtect suele implementar estas limitaciones mediante:

- almacenamiento de datos en el registro
- chequeos internos en el ejecutable
- validación del estado del trial durante la ejecución

---

## Localización del chequeo TimeTrial

Usando el debugger buscamos referencias a cadenas relacionadas con el modo trial:

Trial
Evaluation
Time limit
Trial expired

Siguiendo estas referencias llegamos a la rutina que controla el estado del trial.

Normalmente el programa realiza algo similar a:

CALL CheckTrialStatus
TEST EAX,EAX
JE TrialExpired

Si el chequeo indica que el periodo de prueba ha expirado, el programa muestra el aviso correspondiente.

---

## Modificación del flujo de ejecución

Para evitar la limitación del trial podemos modificar el salto condicional.

Código original:

JE TrialExpired

Modificación posible:

JNE TrialExpired

o bien eliminar la condición para que el programa siempre continúe como si el trial fuese válido.

---

## Aplicación del parche

Procedimiento en OllyDbg:

1. Localizar la instrucción que controla el salto al estado "TrialExpired".
2. Editar la instrucción.
3. Cambiar el salto condicional o neutralizarlo con NOPs.

Tras aplicar el parche guardamos el ejecutable modificado.

---

## Resultado

Después de aplicar el parche:

- El programa deja de mostrar el aviso de expiración.
- Las restricciones del modo trial desaparecen.
- El software funciona sin limitaciones.

---

## Conclusión

Las protecciones basadas en **TimeTrial** suelen depender de verificaciones simples que determinan si el periodo de prueba sigue activo.

Una vez localizada la rutina de control, modificar el flujo de ejecución suele ser suficiente para evitar la limitación.

Este ejercicio muestra cómo identificar y modificar estas comprobaciones en aplicaciones protegidas con **ASProtect**.

---

Autor original: **SyXe'05**  
Formato adaptado: Markdown
