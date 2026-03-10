# 550 — DVD Region+CSS Free 5.9.6.8 — ASProtect 1.2x–1.3x [Registered]

| Campo            | Detalle                                                        |
|------------------|----------------------------------------------------------------|
| **Programa**     | DVD Region+CSS Free 5.9.6.8 (`DVDRegionFree.exe`)             |
| **Protección**   | ASProtect 1.2x – 1.3x [Registered] + Nagscreen + Trial 30 días |
| **Objetivos**    | Desempacar ASProtect (1ª parte)                                |
| **Dificultad**   | Su fortaleza está en la IAT                                    |
| **Herramientas** | OllyDbg v1.10, PEiD 0.94, ImpRec 1.6                          |
| **Autor**        | SyXe'05 — [hAcK-c0d3d] — [CracksLatinoS]                      |
| **Fecha**        | 25-01-2006                                                     |
| **URL**          | http://www.dvdidle.com                                         |

---

## Contexto

Writeup solicitado por **th_hunter_fox**, quien pedía ayuda para desempacar un
programa protegido con ASProtect 1.2x–1.3x. La versión original era la
`v5.9.6.5` pero al momento de escribirse el tute ya estaba actualizada a
`v5.9.6.8`; el proceso es prácticamente idéntico.

Writeups relacionados con versiones superiores del mismo packer:

```
467 – ASProtect v2.0x [Registered] by +NCR
471 – ASProtect v2.0x [Registered] parte II by +NCR
473 – ASProtect v2.0x [Registered] III by +NCR
495 – Asprotect 2.X Parte I por ZettK
542 – ASProtect 2.0x [Registered] by SyXe'05
```

La carpeta de instalación contiene también `DVD43.exe`, igualmente empacado
con la misma versión de ASProtect.

---

## Identificación del packer

PEiD 0.93 confirma:

```
ASProtect 1.2x - 1.3x [Registered] -> Alexey Solodevnikov
```

El EntryPoint presenta la estructura habitual de ASProtect:

```asm
00401000  68 01D04500  PUSH DVDRegio.0045D001
00401005  E8 01000000  CALL DVDRegio.0040100B
0040100A  C3           RETN
0040100B  C3           RETN
```

---

## Localización del OEP

Se utiliza el **método de Narvaja (excepciones)**:

1. Destildar todas las excepciones en `Options → Debugging options → Exceptions`.
2. Pulsar **Shift+F9** sucesivamente hasta que el programa cargue.
3. Anotar la última excepción producida.
4. Reiniciar con **Ctrl+F2** y repetir el proceso, pero al llegar a esa
   excepción colocar un **BPM en la primera sección de código** (Memory Map).
5. Superar la excepción con Shift+F9 → Olly para en el OEP.

```
OEP: 414E46
```

El OEP presenta la estructura típica de inicio de aplicación Win32:

```asm
00414E46  55            PUSH EBP
00414E47  8BEC          MOV EBP,ESP
00414E49  6A FF         PUSH -1
00414E4B  68 80BA4100   PUSH DVDRegio.0041BA80
00414E50  68 F44D4100   PUSH DVDRegio.00414DFA    ; JMP to MSVCRT._except_handler3
...
00414E73  FF15 64874100 CALL DWORD PTR DS:[418764] ; MSVCRT.__set_app_type
```

---

## Delimitación de la IAT

Desde el primer `CALL DWORD PTR` visible en el OEP se hace
**"Follow in Dump → Memory Address"** para aterrizar en la IAT.
Se navega hasta el inicio de la sección `.rdata` (ASProtect borra el nombre).

| | Dirección |
|---|---|
| Inicio IAT | `41800` |
| Final IAT  | `418930` |
| Longitud   | `930`    |

```
418930 - 41800 = 930
```

---

## El problema: redirección de CALLs a la IAT

ASProtect 1.2x–1.3x [Registered] reemplaza todos los `CALL DWORD PTR [addr_api]`
del código original por llamadas a una rutina del packer:

```asm
CALL DWORD PTR [dirección_api]   →   CALL 00E20000
```

Hay **148 CALLs** de este tipo dispersos por toda la sección de código.
Éste es el punto fuerte de esta versión del packer (compartido con ASProtect
2.0x [Registered]), a diferencia de las versiones 2.1 SKE y superiores donde
además aparece *Stolen Code*.

### Obtención de la lista de CALLs a reparar

1. Botón derecho en la sección de código → **"Search for → All commands"**.
2. Buscar la instrucción `CALL 00E20000`.
3. En la ventana de resultados, botón derecho → **"Copy to clipboard → Whole table"**.
4. Pegar en Word, eliminar líneas que no sean un CALL y reemplazar la cadena
   `CALL 00E20000` por vacío → quedan solo las 148 direcciones.
5. Guardar como `calls.doc` (ver archivo adjunto `calls_a_reparar.doc`).

Las primeras direcciones de la tabla son:

```
0040159C  0040AFFD  0040B70B
004015AC  0040B02A  0040B7A1
004015BF  0040B083  0040B811
00401BCE  0040B0F7  ...
```

---

## Análisis del mecanismo de redirección

### Cómo funciona 00E20000

Cuando el programa ejecuta `CALL 00E20000`, la rutina del packer:

1. Toma la **dirección del CALL** que lo invocó (en `:0BF5E83`, valor en EAX).
2. Busca la **API correspondiente** a ese CALL (en `:0BF6258`, valor en EAX).
3. Crea una **zona temporal 1** (`VirtualAlloc`) donde copia parte del código
   de la API.
4. Crea una **zona temporal 2** donde inserta una instrucción basura
   (`INC DWORD PTR SS:[ESP]`) seguida de un `PUSH+RETN` hacia zona 1.
5. **Reparchea** el `CALL 00E20000` original para que apunte a zona 2.

Resultado final para el ejemplo de `GlobalMemoryStatus`:

```
Antes:  004030A6  E8 55CFA100  CALL 00E20000
Ahora:  004030A6  E8 254A0000  CALL 00F70004

; Zona 2 (00F70004):
FF0424        INC DWORD PTR SS:[ESP]
68 0000F600   PUSH 0F60000
C3            RETN

; Zona 1 (00F60000):  ← parte inicial de la API
55            PUSH EBP
8BEC          MOV EBP,ESP
83EC 2C       SUB ESP,2C
...
68 2224DA77   PUSH 77DA2422
C3            RETN              ; Salto a mitad de la API real
```

Este mecanismo es idéntico al de ASProtect 2.0x [Registered].

### Puntos clave para el script

| Dirección  | Contenido en EAX                     |
|------------|--------------------------------------|
| `0BF5E83`  | Dirección del CALL a reparar         |
| `0BF6258`  | Dirección de la API correspondiente  |
| `0BF6273`  | Donde sobrescribe la API con zona 1  |
| `0BF6290`  | Donde sobrescribe zona 1 con zona 2  |

Si se impide la sobreescritura en `0BF6273` y `0BF6290` ("New origin here"
en la instrucción siguiente), el CALL queda reparado directamente a la API:

```asm
004030A6  E8 0254A577  CALL kernel32.GlobalMemoryStatus
```

---

## Preparación de la tabla de direcciones

Para que el script pueda iterar sobre los 148 CALLs se inserta la tabla en
una zona libre del ejecutable:

1. Abrir las 148 direcciones del `calls.doc` en un editor hexadecimal
   (Hex Workshop 3.1):
   - `File → New`
   - `Edit → Paste Special` (marcar "Interpret as a hexadecimal string")
   - `Tools → Operations → Byte Flip` → 32-bit Little Endian
2. Guardar el archivo resultante.
3. En Olly, localizar zona libre en el ejecutable. Se encontró espacio en
   `41F400` (zona de ceros).
4. Copiar allí la tabla con `Edit → Binary paste`.
5. Añadir **4 bytes a cero** al final como condición de parada del script.

```
Tabla en: 41F400
```

---

## Script OllyScript

Colocar los siguientes HBPs antes de lanzar el script:

| # | Dirección | Tipo    | Función                              |
|---|-----------|---------|--------------------------------------|
| 1 | `00414E46`| Execute | OEP (opcional, para reiniciar cómodo)|
| 2 | `00BF5E83`| Execute | Obtiene dirección del CALL a reparar |
| 3 | `00BF6258`| Execute | Obtiene la API correspondiente       |

```asm
; ─────────────────────────────────────────────────
; Script para reparar los 148 CALLs de ASProtect
; 1.2x–1.3x [Registered] — DVD Region+CSS Free
; Autor: SyXe'05 — CracksLatinoS
; ─────────────────────────────────────────────────

var direc       ; dirección del call a reparar
var api         ; API válida encontrada
var pos         ; posición actual en la tabla

mov pos, 41f400 ; inicio de la tabla de CALLs

inicio:
  mov ebx, pos
  mov ebx, [ebx]
  cmp ebx, 0          ; fin de tabla?
  je termina
  mov eip, ebx        ; ejecutar el CALL
  bphws [pos], "x"    ; HBP en el CALL actual
  eob empiezo
  run

empiezo:
  cmp eip, [pos]      ; paró por el HBP del CALL?
  jne vamos
  run                 ; si es así, dejarlo correr

vamos:
  cmp eip, 0BF5E83    ; tenemos la dirección del CALL?
  jne no_direc
  mov direc, eax      ; guardar dirección del CALL
  eob no_direc
  run

no_direc:
  cmp eip, 0BF6258    ; tenemos la API?
  jne revisa
  mov api, eax        ; guardar la API
  mov ebx, 418000     ; inicio IAT

loop:
  mov ecx, [ebx]
  cmp ecx, api        ; ¿es nuestra API?
  je tengo
  add ebx, 4
  cmp ebx, 418930     ; ¿fin de IAT?
  je termina
  jmp loop

tengo:
  mov eax, direc
  mov [eax], #FF15#   ; CALL DWORD PTR ...
  add eax, 2
  mov [eax], ebx      ; apunta a la entrada IAT
  mov eip, 0BF62B4    ; saltar reparcheo del packer
  eob otro
  run

otro:
  bphwc [pos]         ; liberar HBP
  add pos, 4          ; siguiente CALL
  jmp inicio

revisa:
  cmp eip, [pos]
  jne termina
  jmp otro

termina:
  ret
```

Guardar como `script.osc` y ejecutar desde `Plugins → OllyScript → Run script`.
Tarda aproximadamente **1 minuto** en un P4 a 1.7 GHz.

Al terminar aparece el diálogo *"Script finished"*.

---

## Resultado del script

Los CALLs quedan reparados de la forma correcta:

```asm
; Antes:
0040159C  E8 5FEAA100  CALL 00E20000
004015AC  E8 4FEAA100  CALL 00E20000
004015BF  E8 3CEAA100  CALL 00E20000

; Después:
0040159C  FF15 1C824100  CALL DWORD PTR DS:[41821C]  ; kernel32.WaitForSingleObject
004015AC  FF15 20824100  CALL DWORD PTR DS:[418220]  ; kernel32.GetExitCodeThread
004015BF  FF15 24824100  CALL DWORD PTR DS:[418224]  ; kernel32.TerminateThread
```

Limpiar la tabla en `41F400` con **"Undo selection"** (seleccionar toda la
zona y Alt+BkSp).

Corregir el EIP al OEP antes de dumpear (`4164C4` → `414E46` con
"New origin here").

---

## Dump con OllyDump

Opciones en OllyDump:

| Campo          | Valor     |
|----------------|-----------|
| Start Address  | `400000`  |
| Size           | `80000`   |
| Entry Point    | `14E46`   |
| Base of Code   | `1000`    |
| Base of Data   | `18000`   |

- Marcar **"Fix Raw Size & Offset of Dump Image"**.
- **Desmarcar** "Rebuild Import".
- Guardar como `tute.exe`.

---

## Reconstrucción de la IAT con ImpRec 1.6

```
OEP : 00014E46
RVA : 00018000
Size: 00000930
```

Pulsar **"Get Imports"**. Queda **una sola entrada sin resolver**:
`GetProcAddress` de kernel32 (ASProtect la trata de forma especial).

La entrada mala apunta a una rutina del packer en `00BE7758`. Ver su código
con botón derecho → "Disassemble/HexView":

```asm
00BE7758  push ebp
00BE7759  mov ebp,esp
00BE775B  mov edx,[ebp+C]
00BE775E  mov eax,[ebp+8]
00BE7761  cmp eax,[BFA458]   ; DWORD value: FFFFFFFF
00BE7767  jnz short 00BE7772
00BE7769  mov eax,[edx*4+BFA458]
00BE7770  jmp short 00BE7779
00BE7772  push edx
00BE7773  push eax
00BE7774  call 00BD577C       ; = kernel32.dll/0191/GetProcAddress
00BE7779  pop ebp
00BE777A  retn 8
```

ImpRec la detecta correctamente como `kernel32.GetProcAddress`. El log
confirma:

```
23 F (decimal:575) imported function(s).
0 (decimal:0) unresolved pointer(s).
Congratulations! There is no more invalid pointer, now the question is: Will it work? :-)
```

Pulsar **"Fix Dump"** sobre `tute.exe` → genera `tute_.exe`.

---

## Verificación

Al cargar `tute_.exe` en Olly todas las llamadas aparecen correctamente
anotadas con sus parámetros. Ejecutando directamente el binario:

- Aparece la **nag** de bienvenida (Trial pendiente para la 2ª parte).
- Pulsando "Evaluación gratuita" se abre la aplicación completa y funcional.
- Todas las funciones de la interfaz operan correctamente.

---

## Notas

- El **Time-Trial** queda pendiente para una segunda parte del writeup.
- `DVD43.exe` (también en la carpeta de instalación) está empacado con la
  misma versión de ASProtect; el proceso sería análogo.
- ASProtect posee un **CRC check** robusto que impide parchear el ejecutable
  en disco antes del desempacado; de ahí la necesidad del script en memoria.

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (25-01-2006)
- Archivo auxiliar: `calls_a_reparar.doc` — lista de las 148 direcciones
- Herramientas: OllyDbg 1.10, PEiD 0.94, ImpRec 1.6, OllyScript 0.92,
  OllyDump 2.21.108, Hex Workshop 3.1
- Contacto original del autor: syxe00@yahoo.es / syxe05@gmail.com
