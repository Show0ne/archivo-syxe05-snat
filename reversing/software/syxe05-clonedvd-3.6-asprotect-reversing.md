# Reversing CloneDVD 3.6 (ASProtect 1.2x–1.3x)
Tutorial original por **SyXe'05**

Protección analizada: **ASProtect 1.2x – 1.3x**

---

## Introducción

En este tutorial se analiza el programa **CloneDVD 3.6**, protegido con **ASProtect 1.2x–1.3x**.

ASProtect fue una de las protecciones comerciales más utilizadas en aplicaciones shareware de los años 2000.  
Su objetivo principal es dificultar el análisis del ejecutable mediante:

- empaquetado del ejecutable
- cifrado de código
- control de registro y licencias

El objetivo del tutorial es comprender cómo localizar la rutina de validación del registro.

---

## Herramientas utilizadas

Para el análisis utilizaremos:

- **OllyDbg**
- **W32Dasm**
- **PE Tools**
- **Import Reconstructor**

Estas herramientas permiten seguir el flujo del programa y analizar las rutinas protegidas.

---

## Análisis inicial

Al ejecutar el programa observamos que funciona en **modo trial**.

El software solicita un **número de serie** para activar la versión completa.

Las protecciones de este tipo normalmente incluyen:

- comprobación del serial
- control de ejecución del programa
- verificación interna del estado de registro

---

## Identificación de cadenas relevantes

Una técnica común consiste en buscar cadenas relacionadas con el registro:

Register
Registration
Invalid serial
Wrong key
Thank you for registering

Estas referencias suelen conducir a la rutina encargada de validar el serial.

---

## Localización de la rutina de validación

Siguiendo estas referencias encontramos una secuencia similar a:

CALL ValidateSerial
TEST EAX,EAX
JE InvalidSerial

Si el serial introducido es incorrecto, el programa ejecuta la rama que muestra el mensaje de error.

---

## Modificación del flujo del programa

Podemos modificar el salto condicional para evitar la validación.

Código original:

JE InvalidSerial

Parche posible:

JNE InvalidSerial

Otra alternativa es reemplazar el salto por instrucciones **NOP** para que el programa continúe la ejecución normalmente.

---

## Aplicación del parche

Procedimiento:

1. Localizar la instrucción de salto en OllyDbg.
2. Editar la instrucción.
3. Guardar el ejecutable modificado.

Después de aplicar el parche el programa se comportará como si estuviera registrado.

---

## Resultado

Tras aplicar la modificación:

- el programa acepta cualquier serial
- se eliminan las limitaciones del modo trial
- todas las funcionalidades quedan habilitadas

---

## Conclusión

Las protecciones basadas en validación de serial suelen depender de comprobaciones relativamente simples.

Una vez localizada la rutina de validación es posible modificar el flujo de ejecución para evitar la comprobación.

Este tutorial muestra un ejemplo clásico de análisis de software protegido con **ASProtect**.

---

Autor original: **SyXe'05**  
Formato adaptado: Markdown
