# 743 — Primer acercamiento al Stolen Code (Parte 1)

| Campo | Valor |
|------|------|
| Programa | Useful File Utilities v2.3.5 |
| Protección | ASProtect 1.2x–1.3x [Registered] + Stolen Code |
| Autor | SyXe'05 |
| Grupo | CracksLatinoS |
| Fecha | 20‑08‑2006 |

PDF original: **Primer_acercamiento_al_Stolen_Code_parte_1 - [por SyXe'05].pdf**

---

# Introducción

Este tutorial describe una técnica para desempacar ejecutables protegidos con **ASProtect 1.2x–1.3x** que utilizan la técnica conocida como **Stolen Code (SCode)**.

El ejemplo utilizado en el estudio es el programa:

```
Useful File Utilities v2.3.5
```

El objetivo es:

- analizar el comportamiento de la protección
- localizar el OEP real
- reconstruir la IAT
- reparar la tabla de saltos
- recuperar el código robado por el packer.

Herramientas utilizadas:

- OllyDbg 1.10
- PEiD 0.93
- Import Reconstructor (ImpREC)
- ConTEXT
- Hex Workshop
- PEditor
- LordPE
- ToPo

---

# ¿Qué es Stolen Code?

En algunas protecciones modernas, el packer elimina partes del código original del ejecutable y las ejecuta desde memoria o desde secciones temporales.

En lugar de comenzar con un código típico como:

```
PUSH EBP
MOV EBP,ESP
CALL GetModuleHandleA
```

ASProtect elimina bloques de código completos y los ejecuta fuera del ejecutable.

Esto se conoce como **Stolen Code**.

En algunos casos se eliminan más de **1000h bytes** del programa original.

---

# Análisis inicial

Al analizar el ejecutable con **PEiD** se detecta:

```
ASProtect 1.2x – 1.3x [Registered]
```

Dentro de esta protección pueden encontrarse varias variantes:

- redirección simple de IAT
- destrucción de la tabla de saltos
- inserción de Stolen Code
- inserción de basura en la IAT

---

# Antidebug inicial

Al ejecutar el programa en OllyDbg aparece un chequeo usando:

```
IsDebuggerPresent
```

La comprobación se realiza en la dirección:

```
[7FFDF002]
```

Para evitar el antidebug basta con poner ese byte a **0** o usar un plugin de OllyDbg.

---

# Uso de excepciones para encontrar el OEP

Para continuar el análisis se utilizan excepciones controladas.

Pasos:

1. abrir el ejecutable en OllyDbg
2. desactivar la mayoría de excepciones
3. dejar activa la excepción de kernel32
4. ejecutar el programa con F9
5. saltar excepciones con CTRL+F9.

Finalmente se alcanza lo que aparenta ser el OEP.

Sin embargo el código ya ha sido ejecutado parcialmente.

Esto indica la presencia de **Stolen Code**.

---

# Localización del código robado

El código robado se ejecuta desde secciones externas al ejecutable, por ejemplo:

```
014C0000
019C0000
019B0000
```

Estas secciones contienen fragmentos del código original que han sido movidos fuera del ejecutable.

El packer ejecuta estas secciones mediante múltiples llamadas indirectas.

---

# Análisis de llamadas indirectas

Muchas instrucciones del código original son reemplazadas por llamadas como:

```
CALL 02F20000
```

Estas llamadas:

- analizan los flags
- calculan la dirección de destino
- redirigen la ejecución.

En algunos casos se simulan saltos condicionales como:

```
JE
JNE
JG
JL
```

---

# Laberinto de llamadas

El flujo de ejecución se convierte en una cadena de llamadas encadenadas que saltan continuamente entre:

- el ejecutable original
- secciones temporales
- código del packer.

Esto dificulta el análisis manual.

---

# Secciones necesarias

Durante el análisis se identifican varias secciones que deben recuperarse para reconstruir el ejecutable:

```
01290000 size 2C000h
012C0000 size 4000h
012D8000 size 4000h
014C0000 size 16000h
```

Además se utiliza la zona de pila.

---

# Reparación de la IAT

ASProtect modifica la tabla de importación para evitar que un dump funcione.

También sustituye saltos del tipo:

```
FF25
```

por llamadas indirectas que apuntan a secciones virtuales creadas con **VirtualAlloc**.

Para reparar esto se utiliza un script de **OllyScript** que:

1. detecta las modificaciones
2. captura la API real
3. reconstruye la entrada en la IAT
4. restaura el salto original.

---

# Problema con GetProcAddress

Durante la reconstrucción aparece un problema con la API:

```
GetProcAddress
```

El packer utiliza una técnica especial para ocultarla, por lo que debe repararse manualmente.

Los saltos corregidos son:

```
00401338 - jmp [GetProcAddress]
00406FDC - jmp [GetProcAddress]
```

---

# Redirección de secciones

Dos secciones de código robado se redirigen dentro del ejecutable:

```
02F20000 -> 004DC000
02F30000 -> 004DE000
```

Estas secciones contienen partes del código original que el packer ejecutaba fuera del ejecutable.

---

# Estado final (Parte 1)

Después de estas modificaciones se consigue:

- IAT completamente reparada
- tabla de saltos restaurada
- secciones de Stolen Code redirigidas
- ejecución estable hasta el OEP.

El ejecutable se puede dumpear con **OllyDump**.

La reconstrucción final continuará en la **Parte 2 del tutorial**.

---

Autor: **SyXe'05**  
Grupo: **CracksLatinoS**
