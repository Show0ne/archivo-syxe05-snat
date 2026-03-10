# 550 — Armadillo 2.x — Free Registry Fix 3.0

| Campo          | Detalle                                              |
|----------------|------------------------------------------------------|
| **Programa**   | Free Registry Fix 3.0                                |
| **Protección** | Armadillo 2.x + limitación a 50 reparaciones         |
| **Objetivos**  | Desempacar y eliminar la limitación                  |
| **Dificultad** | Muy sencilla                                         |
| **Herramientas** | OllyDbg v1.10, PEiD 0.94, ImpRec 1.6, LordPE      |
| **Autor**      | SyXe'05 — [hAcK-c0d3d] — [CracksLatinoS]            |
| **Fecha**      | 17-11-2005                                           |
| **URL**        | http://www.freeregistryfix.com                       |

---

## Identificación del packer

PEiD detecta **Armadillo 1.xx–2.xx** (Silicon Realms Toolworks). RDG Packer
confirma en modo M-A **Armadillo v2.5x–v2.6x** (compilador Visual C++ v6.0) y
en modo M-B **Armadillo v2.60 b2** con detección heurística de EXECryptor.

Para confirmar la variante se usa **LordPE**: si hay dos procesos corriendo es
Armadillo con CopyMem-II/Nanomites; si hay uno solo, no lo usa. En este caso
hay un único proceso — sin padre/hijo — lo que simplifica bastante el
desempacado.

### Plugins de OllyDbg recomendados

- IsDebuggerPresent 1.3
- CommandBar 3.00.108
- HideDebugger 1.2.3f (configurado al máximo: IsDebuggerPresent, FindWindow/EnumWindows, TerminateProcess, Unhandled exception tricks, OutputDebugString exploit)
- OllyDump 2.21.108
- OllyScript 0.92

Con HideDebugger activo, el byte de IsDebuggerPresent queda a 0 en
`[EBX+2]` / `[7FFDF002]` — verificable desde el EP.

Se tildan también **todas las excepciones** para que Olly no maneje ninguna.

---

## Localización del OEP

Desde el EP del packer se coloca un **BPM en la primera sección** (la que
sigue al PE header en el Memory Map) y se pulsa F9. Olly para directamente en
el OEP sin excepciones adicionales gracias a los plugins:

```
OEP: 004C8FF8
```

Compilador Delphi confirmado por la estructura del código y las secciones
`CODE`, `DATA`, `BSS`, `.idata`, `.tls`, `.rdata`, `.reloc`.

Se pone de inmediato un **HBP en ejecución en el OEP** para facilitar
reinicios posteriores.

---

## Delimitación de la IAT

El primer CALL desde el OEP lleva a `GetModuleHandleA` (típico en Delphi).
Siguiendo los JMPs con "Follow in dump → Memory address":

| | Dirección |
|---|---|
| Inicio IAT | `4D01CC` |
| Final IAT  | `4D09C8` |
| Size       | `7FC`    |

```
4D09C8 - 4D01CC = 7FC
```

---

## IAT Scrambled — salto mágico

Se elige la primera entrada mala `[4D01EC] == C8E6CD` y se coloca un **HBPWD**.
Con dos HBPs activos (OEP en ejecución + entrada mala en escritura) se reinicia
Olly y se pulsa F9.

El HBP de escritura para dos veces: la primera en zona de msvcrt sin los bytes
finales — se ignora. La segunda para en el bucle real de relleno de IAT
(`CA561D`–`CA594A`). Traceando con F8 se localiza el salto mágico:

```
Salto mágico: CA57EB   (JNZ SHORT 00CA582F)
```

Cuando salta, no pasa por el CALL `GetProcAddress` en `CA5821` y guarda en
la IAT el valor de ECX (valor incorrecto) en lugar del de EAX (API real).

### Script OllyDbg

HBPs necesarios: OEP (`4C8FF8`) en ejecución + mágico (`CA57EB`) en
ejecución. Todas las excepciones desactivadas. Script lanzado desde el EP:

```asm
inicio:
eob vamos
run

vamos:
cmp eip, 0ca57eb
jne termina
mov eip, 0ca57ed
jmp inicio

termina:
ret
```

Al terminar el script OllyScript muestra "Script finished" y queda detenido en
el OEP. La IAT ahora resuelve correctamente — `GetModuleHandleA` aparece al
lado del primer JMP.

---

## Reparación del PE header (trastadas de Armadillo)

Armadillo corrompe dos campos del header. Ambos se reparan desde la ventana de
dump antes de volcar.

### 1 — PE Signature

En `[40003C]` Armadillo deja el valor `1651F8` en lugar del offset correcto
hacia la cadena `"PE"`. La cadena `"PE"` se encuentra en `400100`:

```
400100 - 400000 = 100h
```

Se modifica `[40003C]` → `00000100`. En el Memory Map la sección recupera el
indicador "PE header".

### 2 — Número de secciones

El archivo real tiene **13 secciones** (verificado con un editor PE). Armadillo
ha escrito **14** en el campo `NumberOfSections` del COFF header en `400106`.
Se hace doble clic sobre la sección del header en el Memory Map → "Modify
integer" → se cambia `0E` (14) por `0D` (13).

---

## Dump y reconstrucción IAT

**OllyDump:**
- Start: `400000`, Size: `29D000`
- "Get EIP as OEP" → OEP queda `C8FF8`
- **Desmarcar** "Rebuild Import" y "Fix Raw Size & Offset of Dump Image"
- Guardar como `tute.exe`

**ImpRec 1.6:**

```
OEP : 000C8FF8
RVA : 000D01CC    (= 4D01CC - 400000)
Size: 000007FC
```

"Get Imports" devuelve 21 entradas sin resolver — son separadores entre DLLs,
no entradas reales. Se aplica **"Cut Thunks"** a las 21 → ninguna queda por
resolver. "Fix Dump" sobre `tute.exe` → genera `tute_.exe`.

---

## Eliminación de la limitación (50 reparaciones)

El programa limita las reparaciones a **50 por ejecución**. Hay varios puntos
que gestionar.

### Punto 1 — Salto de expiración (`4B420D`)

En `4B420D` hay un `JB` que, tras agotar las 50 reparaciones, redirige a una
zona que muestra el aviso de "upgrade" y bloquea futuras reparaciones. Se
**nopea**.

### Punto 2 — MessageBoxA de advertencia (`4B424C`)

El CALL en `4B424C` lanza el `MessageBoxA` con el aviso. Recibe 4 parámetros
(hOwner, Text, Title, Style). Se sustituye por:

```asm
ADD ESP, 10      ; limpia los 4 parámetros de la pila (4 × DWORD = 10h)
MOV EAX, 1      ; simula pulsación de "Aceptar"
```

Y se fuerza el `JMP SHORT` en `4B4254` para que siempre ejecute la reparación.

### Punto 3 — Contador de 50 (`4B4364`)

La instrucción `MOV EDX, 32` en `4B4364` inicializa el contador a 50 (0x32).
Se cambia por:

```asm
MOV EDX, C350   ; 50.000 decimal
```

Esto amplía el límite de reparaciones por ejecución a 50.000.

### Punto 4 — MessageBeep (`40D39C`)

La llamada a `MessageBeep` en `40D39C` se **nopea** para eliminar el sonido de
aviso.

### Punto 5 — Segundo MessageBox residual (`4B6405`)

En `4B6405` hay un `MOV EAX, 1` + zona que lanza un segundo aviso cuando
quedan errores pendientes. Se aplica `MOV EAX, 1` forzado y se nopea el CALL
al mensaje para que no aparezca.

---

## Resultado

Todos los cambios se guardan como `tute1.exe`:

- ✅ Armadillo desempacado (IAT reparada, PE header corregido).
- ✅ Sin límite práctico de reparaciones por ejecución.
- ✅ Sin mensajes de advertencia ni sonidos.

> ⚠️ El autor reconoce que el ejecutable final no cierra la ventana de progreso
> al terminar y deja ocasionalmente una entrada sin reparar — comportamiento
> residual sin impacto funcional relevante.

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (2005)
- Herramientas: OllyDbg 1.10, PEiD 0.94, ImpRec 1.6, LordPE
- Contacto original del autor: syxe00@yahoo.es
