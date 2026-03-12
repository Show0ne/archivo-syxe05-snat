# 3D FotoStudio 1.2

Autor: SyXe'05
Tipo: Reversing tutorial
Protección: Cinderella (Trial 30 días)
Herramientas: SoftIce, W32Dasm, UltraEdit32

---

## Introducción

El programa 3D FotoStudio 1.2 es una aplicación orientada al manejo y edición de imágenes.
La versión analizada posee una limitación TimeTrial de 30 días, tras la cual el programa deja de funcionar si no se registra.

El objetivo de este tutorial es analizar el mecanismo de registro del programa y obtener un serial válido.

En este tipo de protecciones existen diferentes estrategias posibles:

1. Generar un serial válido.
2. Parchear la rutina de validación.
3. Modificar la lógica de control de registro.

En este tutorial se opta por analizar directamente la rutina de validación del serial.

---

## Preparación

Ejecutamos el programa y abrimos el cuadro de registro.

Introducimos cualquier nombre y cualquier serial para provocar que el programa ejecute la rutina de validación.

Antes de aceptar el registro abrimos SoftIce.

---

## Breakpoints iniciales

Colocamos los siguientes breakpoints:

bpx GetWindowTextA
bpx hmemcpy

Estas funciones suelen utilizarse para:

- Obtener el texto introducido en los campos
- Copiar datos en memoria

Al activarse podremos observar cómo el programa procesa el nombre y el serial.

---

## Captura del serial

Introducimos un nombre y un serial cualquiera y pulsamos Aceptar.

SoftIce se activará al interceptar una de las funciones monitorizadas.

Cuando aparezca el breakpoint ejecutamos:

F5

para continuar la ejecución hasta el siguiente punto de interés.

Si el programa utiliza múltiples campos (nombre y serial), el breakpoint puede activarse varias veces.

---

## Análisis de la rutina de validación

Continuamos la ejecución hasta regresar al código del programa.

Utilizamos:

F11

para salir de las llamadas a funciones del sistema.

Una vez dentro del código del programa utilizamos:

F12

para ejecutar instrucciones hasta el siguiente RET.

En este punto llegamos a una zona de código donde el programa compara el serial introducido con el serial esperado.

Un fragmento típico puede ser:

mov eax,[ebp-10]
mov edx,[ebp-08]
call 00494FA7
test eax,eax
jne 00495000

Si la comparación falla el programa ejecutará un salto hacia la rutina de error.

---

## Localización de la comparación

Analizando el flujo observamos que el programa compara:

- el serial introducido
- el serial calculado internamente

Si ambos coinciden, el registro es aceptado.

Si no coinciden, aparece el mensaje de serial incorrecto.

---

## Estrategias de solución

En este punto tenemos varias opciones.

### Parchear el salto

Podemos modificar el salto condicional para que el programa acepte siempre el serial.

Por ejemplo:

jne bad_serial

puede convertirse en:

je bad_serial

o directamente eliminar el salto.

---

### Generar un serial válido

Otra opción es analizar el algoritmo que genera el serial esperado.

Esto permitiría construir un keygen que genere seriales válidos para cualquier nombre.

---

## Conclusión

En este tutorial hemos analizado el mecanismo de registro del programa 3D FotoStudio 1.2.

Mediante el uso de herramientas clásicas de reversing como SoftIce y W32Dasm se ha identificado la rutina de validación del serial.

A partir de este punto es posible:

- Parchear la aplicación para aceptar cualquier serial
- Analizar el algoritmo de generación de claves
- Desarrollar un generador de seriales

Este tipo de análisis es habitual en protecciones TimeTrial + Serial muy comunes en software de principios de los años 2000.

---

Autor: SyXe'05
