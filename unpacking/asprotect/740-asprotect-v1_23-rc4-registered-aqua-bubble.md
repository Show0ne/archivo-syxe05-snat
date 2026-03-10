# 740 — Aqua Bubble — ASProtect v1.23 RC4 Registered

| Campo            | Detalle                                                                        |
|------------------|--------------------------------------------------------------------------------|
| **Programa**     | Aqua Bubble                                                                    |
| **Protección**   | ASProtect v1.23 RC4 Registered + limitaciones varias                           |
| **Objetivos**    | Desempakar y lograr que funcione                                               |
| **Dificultad**   | Sencilla                                                                       |
| **Herramientas** | OllyDbg v1.10, PEiD v0.93, ImpREC v1.6, ConTEXT v0.98, Hex WorkShop 4.23, PEditor v1.7, LordPE Deluxe |
| **Autor**        | SyXe'05 — [hAcK-c0d3d] — [CracksLatinoS]                                      |
| **Fecha**        | 01-08-2006                                                                     |
| **URL**          | http://arcade.reflexive.com                                                    |

> **Nota:** Este tute estudia las diferencias entre ASProtect v1.23 RC4 normal
> (sin registrar) y la versión **Registered**, usando `AquaBubble.exe` como
> objetivo.

---

## Identificación

PEiD v0.93 detecta:

```
ASProtect 1.23 RC4 Registered -> Alexey Solodovnikov
```

Plugins usados en OllyDbg: CommandBar v3.10.109c, Hide Debugger v1.2.3f,
IsDebuggerPresent v1.4, OllyDump v2.21.108, OllyScript v0.92.

La protección antidebug se basa únicamente en el byte `IsDebuggerPresent`
en `[EBX+2]` → `[7FFDF002]` que debe valer `0`.

---

## Llegando al OEP

Se carga `AquaBubble.exe` en Olly y se van superando excepciones con el
**método de Ricardo** hasta llegar a la última:

```asm
01288D03  3100          XOR [EAX], EAX
01288D05  64:8F05 ...   POP dword ptr fs:[0]
01288D0C  58            POP EAX
01288D0D  833D BC7E2801 CMP dword ptr [1287EBC], 0
01288D14  74 14         JE SHORT 01288D2A
```

Se pone un **BPM on access** en la primera sección de código (`ALT+M`) y se
supera con `SHIFT+F9`. Olly para mostrando ceros antes del primer CALL — son
los **Stolen Bytes**:

```asm
00437431  0000  ADD [EAX], AL   ; Stolen bytes!
...
00437445  FF15 68914500  CALL [4591683]
0043744B  33D2            XOR EDX, EDX
```

---

## Buscando los Stolen Bytes

Se reinicia Olly con `CTRL+F2`, se llega a la última excepción y se localiza
el **SEH handler** en la pila:

```
0012FF84  01283CB0   Pointer to next SEH record
0012FF88  01283CE6   SE handler   ← sección activa del packer
```

Se pone un **BPM on Memory Access** en todo el bloque que contiene `01283CE6`.
Se pasa la excepción con `CTRL+F9`. Olly para en la sección del packer.

Se tracea hasta el RET que cae en NTDLL. Con el BPM activo se pulsa F9 y Olly
vuelve a parar un poco más adelante. Se pasa la zona con F8 hasta el siguiente
RET. Desde aquí se tracea con **F7** con cuidado, deshaciendo bucles con BP al
final + F9:

```asm
01295E07  75 21000000   JNZ 01295E2E   ; bucle — poner BP después y F9
```

Al llegar a la zona de stolen bytes, el inicio está en `01295EE0`:

```asm
01295EE0  65:EB 01      JMP short 01295EF0   ; Superfluous prefix
01295EEF  F2:           prefix repne
01295EF0  F2:           prefix repne
...
01295F92  896C24 04     MOV [ESP+4], EBP     ; PUSH EBP (inicio real)
```

La zona es **automodificable** (XORs en medio de la rutina). Se tracea con F7
hasta recopilar todos los stolen bytes:

```asm
01295F92  896C24 04   MOV [ESP+4], EBP    ; PUSH EBP
01295FFE  895C24 04   MOV [ESP+4], EBX    ; PUSH EBX
01296025  897424 04   MOV [ESP+4], ESI    ; PUSH ESI
0129604C  897C24 04   MOV [ESP+4], EDI    ; PUSH EDI
0129605B  8965 E8     MOV [EBP-18], ESP   ; MOV [EBP-18], ESP
```

Se pegan en el **verdadero OEP** (`00437441F`) justo encima del primer CALL.
Se hace **New Origin Here** al inicio de los stolen bytes y se dumpea con
OllyDump → `tute.exe` (Rebuild Import **desactivado**).

---

## Reparación de la IAT

| Dato         | Valor    |
|--------------|----------|
| Inicio IAT   | `459000` |
| Final IAT    | `459480` |
| Longitud IAT | `480`    |
| OEP (RVA)    | `3741F`  |

Se cierra el Olly con el dump y se abre otro con el **ejecutable original
empacado**. Se pone un **BPM on Memory Write** en `[459000]`, se deshabilitan
excepciones (`ALT+O`), se pulsa F9.

Olly para en un `REP MOVS` — no vale. Se pulsa F9 otra vez y para en el
bucle de relleno donde se ve el **CALL mágico** en `012835D1`:

```asm
012835CC  E8 43FCFFFF   CALL 01283214
012835D1  E8 7EFEFFFF   CALL 01283454   ; call mágico
012835D6  8B17          MOV EDX, [EDI]
```

Se reinicia Olly, se reactivan las excepciones, se pone BP en el call mágico,
se pasan las excepciones con `SHIFT+F9` y se **nopea**:

```asm
012835D1  90 90 90 90 90  NOP x5
```

Se pulsa `CTRL+F9` para retornar y se pone un **BP en el POPAD** al final del
loop (`01288857`). Se pulsa F9 y para allí. Se hace **Undo Selection** para
restaurar el call nopeado. Se reac­tivan las excepciones y se llega al OEP.

En ImpREC se selecciona el proceso `AQUABUBBLE.EXE`:

| Campo | Valor      |
|-------|------------|
| OEP   | `0003741F` |
| RVA   | `00059000` |
| Size  | `00000484` |

Entradas manuales pendientes:

| # | IAT rva | Apunta a | API correcta        |
|---|---------|----------|---------------------|
| 1 | 59168   | 01281528 | GetVersion          |
| 2 | 591B4   | 01281554 | GetCurrentProcess   |
| 3 | 59220   | 01281574 | GetCurrentProcess   |
| 4 | 59284   | 0128155C | GetCurrentProcessId |
| 5 | 592A8   | 012810AC | GetProcAddress      |
| 6 | 592AC   | 01281500 | GetModuleHandleA    |

Se pulsa **Fix Dump** → genera `tute_.exe`.

---

## Antidumps y correcciones

### Error 1: "Crypt API not found"

`tute_.exe` lanza un MessageBox con texto *"Crypt API not found. Please
re-install application..."*.

El fallo ocurre en `00420D10` — hay una llamada a `GetProcAddress` con
`hModule = FFFFFFFF` (inusual). En el ejecutable original el packer intercepta
esta API y devuelve un valor de una tabla interna en `012810C1` sin ejecutar la
API real.

**Solución en `tute_.exe`:** modificar el call para que simplemente ponga un
valor distinto de cero en EAX y retorne:

```asm
00420CF0  90            NOP       ; (NOPs donde estaba el CALL)
...
00420CF5  B8 01000000   MOV EAX, 1
00420CFA  33C0          XOR EAX, EAX  ; → EAX = 1 (distinto de 0)
00420CFC  C3            RET
...
00420D19  B8 01000000   MOV EAX, 1
0042001E  C3            RET
```

Se guarda con **Copy to Executable → Save File**.

### Error 2: ACCESS_VIOLATION en `[4623B0]`

El segundo crash ocurre porque el programa intenta leer desde `[01290BB0]`
(zona que solo existe en el proceso del empacado, no en el dump).

El puntero en `[4623B0]` apunta a `01290BB0` que en el original contiene la
cadena `"3RptLw&gaJM=..."` relacionada con el estado Trial/Registered.

**Solución:** redirigir el puntero en `[4623B0]` hacia la cadena
`"9mFUeAAAI1e="` que ya existe en el dump justo después:

```
004623B0: B8 23 46 00   →   (dirección de "9mFUeAAAI1e=" en el dump)
```

Se seleccionan los 4 bytes y se hace **Copy to Executable → Save File**.

Con estos dos cambios `tute_.exe` arranca correctamente.

---

## Registrando el programa

Al ejecutar aparece una **NagScreen** sin botones de sistema (banner con tres
botones: MAYBE LATER / BUY NOW / ALREADY PAID).

### Localización del flag de registro

En el código se localiza la variable de estado en `[46DE80]`. Se buscan todas
las referencias con **Find References → To Address Constant** y se localiza:

```asm
004251F0  A1 80DE4600   MOV EAX, [46DE80]   ; lee el flag
004251F5  8B5424 04     MOV EDX, [ESP+4]
004251F9  2BC2          SUB EAX, EDX
004251FB  85C0          TEST EAX, EAX
004251FD  A3 80DE4600   MOV [46DE80], EAX   ; salva el resultado
00425202  7F 13         JG SHORT 00425217
00425204  E8 57FBFFFF   CALL 00424D60       ; interesante llamada
00425209  85C0          TEST EAX, EAX
0042520B  7E 13         JLE SHORT 00425217  ; Salta si Trial
0042520D  C705 80DE4600 MOV dword ptr [46DE80], 36EE80h  ; hmmm..
```

Se entra en el CALL previo (`00435C80`) que lleva a
`Reflexiv.radll_HasTheProductBeenPurchased` vía `JMP [46FF64]`.

### Dentro de ReflexiveArcade.dll

La función clave está en `10008124` y debe retornar `AL==1`:

**Primera salida** (`1000B729`–`1000B74B`):

```asm
1000B745  0F94C1   SETE CL          ; ← cuidado aquí!
```

Parche:

```asm
1000B745  B0 01    MOV AL, 1        ; forzar AL=1
1000B747  90       NOP
```

**Segunda salida** (`1000B7A4`–`1000B7BB`):

```asm
1000B7B7  8AC3     MOV AL, BL       ; ← debe quedar AL==1
```

Parche:

```asm
1000B7B7  B0 01    MOV AL, 1
```

Ambos cambios se aplican en **ReflexiveArcade.dll** →
**Copy to Executable Selection → Save File**.

### Error 3: CryptVerifySignatureA

Con la DLL modificada, el programa crashea. La causa es un `JNZ` que salta a
`[47068C]` donde hay `0x00000000` (memoria protegida). En la DLL original este
valor se escribe correctamente pero en la modificada no, porque dentro del
CALL verificador ocurre esto:

```asm
00435518  E8 8BF9FFFF   CALL 00434E80    ; call verificador
00435520  83C4 04       ADD ESP, 4
00435524  84C0          TEST AL, AL
00435526  JNZ 00435551                   ; ← saltamos si OK
```

Dentro del CALL se llama a:

```asm
004350BE  FF15 18904500  CALL [<&advapi32.CryptVerifySignatureA>]
```

La DLL verifica su propia firma digital. Si la firma no coincide (DLL
modificada) retorna `AL==0` y el JNZ no salta → crash.

**Solución en `tute_.exe`:** convertir el JNZ en JMP incondicional:

```asm
00435526  EB 28   JMP short 00435551   ; era JNZ — salta siempre
```

Se guarda el cambio en `tute_.exe` sobrescribiendo el archivo.

---

## Limpieza final

Se restaura `ReflexiveArcade.dll` modificada y se ejecuta el programa.
Arranca sin limitaciones — el juego es completamente funcional.

Para reducir el tamaño del ejecutable:

1. Se elimina la sección `.adata` con **PEditor v1.7** (no es necesaria).
2. La sección `.data` se deja (al eliminarla pierde el icono).
3. Se arrastra el EXE sobre **LordPE** para hacer un **Rebuild**.
4. Tamaño final: de 616 KB → 611 KB.

---

## Resultado

- ✅ **Desempacado** con IAT reparada.
- ✅ **Antidumps neutralizados** (GetProcAddress fake, puntero a zona del packer).
- ✅ **CryptVerifySignatureA bypaseado** (JNZ → JMP).
- ✅ **Registrado** — sin nag, sin restricciones, sin referencias a TRIAL.
- ✅ Tamaño reducido con LordPE Rebuild.

---

## Notas técnicas

- La versión **Registered** de ASProtect añade verificación de firma digital de
  la DLL auxiliar mediante `CryptVerifySignatureA` — diferencia principal
  respecto a la versión RC4 normal.
- El puntero en `[4623B0]` apunta a una zona de memoria del packer que no
  existe en el dump — hay que redirigirlo a una cadena válida dentro del
  ejecutable.
- Seguir el **flag de estado** (`[46DE80]`) es la estrategia clave para
  localizar la verificación de registro.

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (01-08-2006)
- Herramientas: OllyDbg 1.10, PEiD 0.93, ImpREC 1.6, PEditor 1.7, LordPE Deluxe
- Contacto original: syxe05@gmail.com
