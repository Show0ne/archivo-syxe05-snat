# 739 — TagRename v2.1.7.4 — ASProtect v1.23 RC4 – v1.3.08.24

| Campo            | Detalle                                                                        |
|------------------|--------------------------------------------------------------------------------|
| **Programa**     | TagRename v2.1.7.4                                                             |
| **Protección**   | ASProtect v1.23 RC4 – v1.3.08.24 + Trial 30 días                              |
| **Objetivos**    | Desempakar y evitar el trial                                                   |
| **Dificultad**   | Facilón                                                                        |
| **Herramientas** | OllyDbg v1.10, PEiD v0.94, ImpREC v1.6, ConTEXT v0.98, Hex WorkShop 4.23, PEditor v1.7, LordPE Deluxe |
| **Autor**        | SyXe'05 — [CracksLatinoS]                                                     |
| **Fecha**        | 17-06-2006                                                                     |
| **URL**          | http://DondeSea.com                                                            |

---

## Identificación

PEiD 0.94 detecta:

```
ASProtect 1.23 RC4 - 1.3.08.24 -> Alexey Solodovnikov
```

Se usa **OllyICE** (build de hacnho) que incluye plugins antidebug integrados.
Se carga `TagRename.exe` y se van superando excepciones hasta llegar a la última.

---

## Localización del OEP (Stolen Bytes)

Desde la última excepción se abre el Memory Map (`ALT+M`) y se coloca un
**BPM on access** en la primera sección de código. Se supera la excepción con
`SHIFT+F9` y Olly para en:

```asm
00407E8C  FF25 D8C25F00   JMP [5FC2D8]   ; JMP a la IAT — no es el OEP
00407E92  8BC0            MOV EAX, EAX
00407E94  FF25 D4C25F00   JMP [5FC2D4]
...
```

No es el OEP — hay **Stolen Bytes**. Se analiza el Call Stack (`ALT+K`) para
ver las llamadas previas. Se selecciona la entrada inferior de la pila y se
entra con Enter para llegar a la rutina donde al final hay un `RETN`. Se pone
un BP allí, se pulsa F9 y se supera el RETN con F8.

Se aterriza en código con instrucciones sospechosas (`psraw mm7,mm7`, `???`)
que indican código corrupto. Haciendo scroll hacia arriba se encuentran los
stolen bytes representados como ceros. El **falso OEP** queda en `005F6FBE`
(provisional).

---

## Reparación de la IAT

Desde el JMP a la IAT se hace **Follow in dump → Memory Address** para
localizar el inicio de la tabla.

| Dato          | Valor    |
|---------------|----------|
| Inicio IAT    | `5FC1CC` |
| Final IAT     | `5FCA7C` |
| Longitud IAT  | `8B0`    |

### Localizar y nopear el CALL mágico

Se toma una **entrada mala** de la IAT (valor `0154034C`) y se pone un
**BP Memory on Write** en esa dirección. Se reinicia y se pulsa F9.

Olly para en `014D32C0`. En los registros se confirma que el packer está
rellenando la IAT. El responsable de redirigir las APIs es el CALL en
`014D32B9`:

```asm
014D32B4  E8 47FCFFFF   CALL 014D2F00
014D32B9  E8 7EFEFFFF   CALL 014D3180   ; <-- CALL mágico
014D32BE  8B17          MOV EDX, [EDI]
```

Se reinicia Olly, se navega al CALL mágico y se **nopea**:

```asm
014D32B9  90  NOP
014D32BA  90  NOP
014D32BB  90  NOP
014D32BC  90  NOP
014D32BD  90  NOP
```

Se desactivan las excepciones (`ALT+O`) para ir más rápido, se pone un
**BPM on Write** en la **última entrada** de la IAT (`005FCA78`) y se pulsa F9.

Alternativa: poner BP con F2 en el `POPAD` al final del loop de relleno
(`014D3550`).

Cuando Olly para en la última entrada se restaura el CALL nopeado con
**Undo Selection** (`ALT+BkSp`). Se reactiván las excepciones y se continúa
hasta el OEP.

### Entradas manuales pendientes

| # | IAT rva | Apunta a   | API correcta        |
|---|---------|------------|---------------------|
| 1 | 1FC21C  | 014D17A4   | GetProcAddress      |
| 2 | 1FC220  | 014D1C64   | GetModuleHandleA    |
| 3 | 1FC230  | 014D1CD8   | GetCommandLineA     |
| 4 | 1FC2D8  | 014D1C64   | GetModuleHandleA    |
| 5 | 1FC378  | 014D1CC8   | LockResource        |
| 6 | 1FC3B8  | 014D1C8C   | GetVersion          |
| 7 | 1FC3DC  | 014D17A4   | GetProcAddress      |
| 8 | 1FC3E0  | 014D1C64   | GetModuleHandleA    |
| 9 | 1FC414  | 014D1CC0   | GetCurrentProcessId |
|12 | 1FC420  | 014D1CF0   | FreeResource        |

Se guardan en ImpREC con **Save Tree** → `iat.txt`. OEP provisional: `0x1000`.

---

## Localización de los Stolen Bytes

Se llega de nuevo a la última excepción y se localiza el **SEH handler** en
la pila:

```
0012FF68  014D39CF   SE handler   ; bloque [014C0000 – 014DE000]
```

Se pone **BPM on Memory Access** en ese bloque, se supera la excepción con
`SHIFT+F9`. Olly para en `014D39CF`. Se tracea hasta el RET (cae en NTDLL),
se vuelve a pulsar F9 y Olly para en `014D39EE`. Desde allí se tracea con F8
hasta otro RET que lleva a otra sección del packer (`01546B4`).

Se continúa con **F7** para no saltar ningún CALL. Se deshacen los bucles
poniendo BP al final y pulsando F9. Tras el POPAD en `01546B45` la pila queda
limpia:

```
0012FFC4  77E614C7   RETURN to kernel32.77E614C7   ; aún no hay stolen bytes
```

Al llegar a `01546BCE` empieza la ejecución de los stolen bytes:

```asm
01546BCE  896C24 00   MOV [ESP], EBP   ; especie de PUSH EBP
01546BD2  8BEC         MOV EBP, ESP
01546BD4  83C4 FC      ADD ESP, -0C
...
```

Tras su ejecución, la pila muestra 7 DWORDs empujados — los stolen bytes son:

```asm
PUSH EBP
MOV EBP, ESP
ADD ESP, -0C
PUSH EDX
PUSH EBX
PUSH EBX
PUSH ESI
PUSH EDI
MOV EAX, 5F6998
```

**Bytes:** `55 8B EC 83 C4 FC 52 53 53 56 57 B8 98 69 5F 00`

Se pegan antes del falso OEP → el **OEP provisional** queda en `005F6FAE`.

---

## Dump y reparación del ejecutable

Se dumpea con OllyDump con **Rebuild Import desactivado** → `tute.exe`.

En ImpREC se selecciona el proceso `TagRename`, se carga `iat.txt` y se pone:

| Campo | Valor      |
|-------|------------|
| OEP   | `001F6FAE` |
| RVA   | `001FC1CC` |
| Size  | `000008B4` |

Se pulsa **Fix Dump** → genera `tute_.exe`.

### Problema: Initialization Error

`tute_.exe` lanza error al ejecutarse. El fallo ocurre en una llamada interna
(`CALL EAX` → `005FA704`) donde un POP intenta escribir en `77E93F25`
(FatalExit de kernel32) — dirección protegida.

**Causa:** los stolen bytes sobreescriben `005F6FAC`–`005F6FAE` que contiene
el valor `0x005F6970` necesario para la **deinit table**. El primer DWORD
queda como `0x8B556970` en lugar de `0x005F6970`.

### Solución: JMP a zona secundaria

1. Se recuperan los bytes originales del ejecutable empacado y se pegan en
   `005F6FAC`:

   ```
   005F6FAC: 70 69 5F 00   (valor original)
   ```

2. Se inserta un `JMP` antes del CALL problemático apuntando a una zona libre
   (`005F70E4`) donde se colocan los stolen bytes:

   ```asm
   005F6FB9  E9 26010000   JMP 005F70E4   ; salto al injerto
   ...
   005F70E4  55            PUSH EBP
   005F70E5  8BEC          MOV EBP, ESP
   005F70E7  83C4 FC       ADD ESP, -4
   005F70EA  52            PUSH EDX
   005F70EB  53            PUSH EBX
   005F70EC  53            PUSH EBX
   005F70ED  56            PUSH ESI
   005F70EE  57            PUSH EDI
   005F70EF  B8 98695F00   MOV EAX, 005F6998
   005F70F4  68 BE6F5F00   PUSH 005F6FBE
   005F70F9  C3            RET
   ```

3. El **OEP definitivo** queda en `005F6FB9`. Se modifica con PEditor:

   | Campo       | Valor      |
   |-------------|------------|
   | Entry Point | `001F6FB9` |
   | Image Base  | `00400000` |

4. Se pulsa **Apply Changes**.

### Neutralizar bucle de encriptación en OEP

En la zona del OEP hay un bucle que encripta/desencripta datos al iniciar y
al cerrar. Si no se neutraliza, el programa crashea al cerrarse.

Bucle de encriptación (`005F6FE4`–`005F6FF3`):

```asm
005F6FE4  BA 0D000000   MOV EDX, 0D
005F6FE9  B8 04A75F00   MOV EAX, 005FA704
005F6FEE  8028 02       SUB BYTE PTR [EAX], 2   ; InicioLoop
005F6FF1  40            INC EAX
005F6FF2  4A            DEC EDX
005F6FF3  75 F9         JNZ SHORT 005F6FEE       ; FinLoop
```

Se **nopean** todas las instrucciones del bucle + el `MOV EDX,0D` previo.

También se nopean el PUSH y POP problemáticos en `005FA70B`–`005FA70E`.

Se salvan los cambios con **Copy to Executable File → All Modifications →
Save File** (en dos pasadas si Olly no permite hacerlo todo a la vez).

El ejecutable arranca correctamente. ✅

---

## Eliminando el Trial y el registro

El packer era el responsable del conteo de días — en el dumpeado ya no hay
chequeo de tiempo. Sin embargo siguen apareciendo la **nag** y cadenas
`UNREGISTERED`.

Se carga el dumpeado en Olly, se analiza el módulo (`CTRL+A`) y se buscan
cadenas. Se localiza:

```asm
005F6706  E8 0122E7FF   CALL 00468890C    ; hmmm..
005F670B  84C0          TEST AL, AL
005F670D  75 74         JNZ SHORT 005F6783
005F670F  A1 68A85F00   MOV EAX, [5FA868]
...
005F6714  BA F0675F00   MOV EDX, 005F67F0
005F6719  E8 7810E4FF   CALL 00437798
005F671E  8B0D 00A85F00 MOV ECX, [5FA800]  ; ASCII "Tag&Rename 2.1.7.4 UNREGISTERED"
```

Dentro del CALL de verificación (`00468890C`) se comprueba el serial guardado
en el registro:

```
[HKEY_CURRENT_USER\Software\Softpointer\Tag&Rename\Config]
"cbVQFFtoTagReplaseUnde" = "12121212"
"Name"                  = "SyXe'05"
```

El algoritmo es tipo **HASH** — se verifican 4 DWORDs resultantes. La
comparación ocurre en `00468771`–`004687A0`:

```asm
00468771  3B4424 14   CMP EAX, [ESP+14]
00468775  75 28       JNZ SHORT 0046879F   ; salto de fallo 1
00468777  3B4424 04   CMP EAX, [ESP+4]
...
00468789  75 14       JNZ SHORT 0046879F   ; salto de fallo 2
...
0046878F  75 0E       JNZ SHORT 0046879F   ; salto de fallo 3
...
00468793  75 00       JNZ SHORT 0046879F   ; salto de fallo 4
0046879D  EB 04       JMP short 004687A3   ; flag de error
004687A3  B0 01       MOV AL, 1            ; flag de éxito
```

**Parche:** nopear los 4 primeros JNZ y convertir el JMP de error en JMP a
la zona buena:

```asm
00468775  90 90  NOP NOP     ; era JNZ 0046879F
0046877F  90 90  NOP NOP     ; era JNZ 0046879F
00468789  90 90  NOP NOP     ; era JNZ 0046879F
00468793  90 90  NOP NOP     ; era JNZ 0046879F
0046879D  EB 04  JMP 004687A3 ; redirige siempre al flag de éxito
```

Se guarda como `tute_1.exe` → **Copy to Executable → Selection → Save File**.

---

## Resultado

- ✅ **Desempacado** limpio con IAT reparada.
- ✅ **Trial eliminado** — el packer ya no está presente para contar días.
- ✅ **Registrado** — About muestra "Registered to: SyXe'05".
- ✅ El reloj del sistema puede adelantarse/retrasarse sin efecto.
- ✅ Desaparecen todas las cadenas UNREGISTERED/TRIAL.

---

## Notas técnicas

- **Stolen Bytes** en este ASProtect se ejecutan en zona del packer antes del
  OEP — se recuperan observando la pila limpia justo antes.
- El **CALL mágico** (`014D32B9`) intercambia APIs buenas por APIs encriptadas
  durante el relleno de la IAT — nopear y restaurar es la técnica estándar.
- La **deinit table** comparte zona con los stolen bytes — hay que preservar
  los valores originales y redirigir con JMP a zona libre.
- El bucle de encriptación al inicio/cierre usa XOR/SUB sobre el propio código
  — nopear previene el crash al cerrar.

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (17-06-2006)
- Herramientas: OllyICE (hacnho), PEiD 0.94, ImpREC 1.6, PEditor 1.7, LordPE Deluxe
- Contacto original: syxe05@gmail.com
