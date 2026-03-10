# 551 — ASProtect 1.23 RC4 — Clip Plus 3.3

| Campo          | Detalle                                              |
|----------------|------------------------------------------------------|
| **Programa**   | Clip Plus 3.3                                        |
| **Protección** | ASProtect 1.23 RC4 [Registered] + Trial 30 días      |
| **Objetivos**  | Desempacar y eliminar la nag/Trial                   |
| **Dificultad** | No es difícil                                        |
| **Herramientas** | OllyDbg v1.10, PEiD 0.94, ResHacker 3.4            |
| **Autor**      | SyXe'05 — [hAcK-c0d3d] — [CracksLatinoS]            |
| **Fecha**      | 13-11-2005                                           |
| **URL**        | http://www.hotdownloads.com                          |

---

## Identificación del packer

PEiD detecta **ASProtect 1.23 RC4 Registered → Alexey Solodovnikov**.
RDG Packer indica **ASProtect v1.23–v2.0** (sin concretar compilador).

A diferencia de ASProtect 2.0x [Registered], cuyo fuerte es la redirección de
IAT, la rama 1.23 RC4 también redirige la IAT agresivamente y puede presentar
**stolen bytes** al inicio del código. La librería `riched20.dll` incluida en
la carpeta de instalación tiene su EP fuera de la sección de código — síntoma
de que también está empacada.

**Plugins de OllyDbg usados:**
- HideDebugger 1.2.3f (IsDebuggerPresent, FindWindow/EnumWindows,
  TerminateProcess, Unhandled exception tricks, OutputDebugString exploit)
- IsDebuggerPresent 1.3
- OllyScript 0.92
- CommandBar 3.00.108
- OllyDump

Excepciones: **no tildadas** (Olly maneja todas excepto las de la lista custom).

---

## Localización del OEP

Se usa el **método de excepciones**: se van superando con Shift+F9 anotando la
última. Tras la última excepción se abre el Memory Map (Alt+M) y se coloca un
**BPM en la primera sección** (sección de código). Se supera con Shift+F9 y se
aterriza directamente en el OEP:

```
OEP: 00401000
```

Compilador **MASM/TASM** — inicio en `401000` con un `JMP`, sin stolen bytes
visibles.

---

## Delimitación de la IAT

Entrando en el primer CALL desde el OEP (`401022`) se llega a la Jump Table,
completamente destrozada. La mayoría de entradas apuntan a zonas inválidas
porque ASProtect 1.23 RC4 redirige casi todos los punteros del kernel.

Para localizar el inicio con precisión se usa **"Find References" (Ctrl+R)**:
se selecciona un bloque sospechoso en la zona de datos y se buscan referencias
hasta encontrar el primer puntero válido de la IAT.

| | RVA / Dirección |
|---|---|
| Inicio IAT | `63915C` (RVA `23915C`) |
| Final IAT  | `63A42C` (RVA `23A42C`) ⚠️ *ver nota* |
| Size       | `12E0` (aproximado, contiene mucha basura) |

> ⚠️ En el writeup original se calculó erróneamente `63A43C` como final — el
> valor correcto es `63A42C`. El error causó un fallo de acceso al poner el
> BPM en la última entrada, pero no afectó al proceso de reparación.

**Datos para ImpRec:**
```
OEP : 00001000
RVA : 0023915C
Size: 000012E4
```

---

## Localización del call semi-mágico

Se elige el primer puntero redirigido de la Jump Table — `[63941C] == DA8DC0`
— y se coloca un **BPM on Write** en esa dirección. Con las excepciones
deshabilitadas se pulsa F9. El HBP para en la zona de relleno de IAT con los
dos CALLs característicos de esta versión de ASProtect:

```
call_mágico: D935D1
```

Para llegar a él hay que dejar que el packer solicite primero el bloque de
memoria vía `VirtualAlloc`. Procedimiento:

1. Reiniciar Olly con excepciones habilitadas.
2. Cuando pare en la primera excepción, deshabilitar excepciones.
3. Hacer GO a `D935D1` y **nopear** el CALL.
4. Poner BPM en la última entrada de la IAT y pulsar F9.

---

## Reconstrucción IAT con ImpRec 1.6

"Get Imports" devuelve un único thunk marcado como `Valid:NO`. Con "Show
Invalid" se muestran las entradas malas — son valores inofensivos (basura
entre entradas válidas). Se seleccionan por bloques con Shift+clic y se
aplica **"Cut Thunks"** bloque a bloque. Quedan **7 entradas sin resolver**,
todas del kernel32.

### Entradas manuales — kernel32

| IAT RVA  | Apunta a | API correcta         |
|----------|----------|----------------------|
| `23947C` | `D9158C` | `FreeResource`       |
| `239488` | `D91574` | `GetCommandLineA`    |
| `239490` | `D9155C` | `GetCurrentProcessId`|
| `2394DC` | `D91500` | `GetModuleHandleA`   |
| `2394E8` | `D910AC` | `GetProcAddress`     |
| `23951C` | `D91528` | `GetVersion`         |
| `239590` | `D91564` | `LockResource`       |

Cada entrada se verifica siguiendo la dirección destino en el Disassembler —
el stub del packer llama internamente a `GetProcAddress` o retorna el valor
directamente desde estructuras internas. Se corrigen manualmente en ImpRec.

Se guarda la IAT con **"Save Tree"** → `tute_iat.txt` por precaución.

---

## Dump y Fix Dump

Con un segundo OllyDbg detenido en el OEP se vuelca con **OllyDump** (opciones
estándar, sin Rebuild Import). Se guarda como `tute.exe`. Desde ImpRec se
aplica **"Fix Dump"** → genera `tute_.exe`.

---

## Eliminación de la nag y fix del AccessViolation

### Problema 1 — AccessViolation al ejecutar fuera de Olly

`tute_.exe` lanza un `EAccessViolation` al ejecutarse directamente. Se localiza
mediante **bisección por bucles infinitos**: se inserta un `JMP` sobre sí mismo
en distintos puntos del código, se guarda y se ejecuta. Si no falla el error
está después; si falla, antes. Intervalo final:

```
40631F – 406339
```

El CALL culpable está en `406334`:

```asm
00406334  E8 53780000  CALL clipplus.0040DB8C
```

Dentro de él, el subcall `0040DBA4 → CALL clipplus.005D9574` es el responsable
del crash. Se **nopean** los 5 bytes del subcall en `40DBA4`:

```asm
; Antes:
0040DBA4  E8 CBB91C00  CALL clipplus.005D9574

; Después:
0040DBA4  90 90 90 90 90  NOP × 5
```

### Problema 2 — Nag de evaluación

La nag se muestra desde `406365`. El salto que la evita está en `40633C`,
controlado por el byte en `[EDX+72D]`. Si ese byte vale `0` se muestra la nag;
si vale `1` el programa arranca en modo licenciado.

**Parche aplicado:**

```asm
; Antes:
0040633C  80BA 2D070000  CMP BYTE PTR DS:[EDX+72D], 0
00406343  0F85 80000000  JNZ tute_.004063C9

; Después:
0040633C  C682 2D070000  MOV BYTE PTR DS:[EDX+72D], 1
00406343  E9 81000000    JMP tute_.004063C9
00406348  90             NOP
```

---

## Resultado

Guardando todos los cambios como `tute_ok.exe`:

- ✅ ASProtect 1.23 RC4 desempacado, IAT completamente reparada.
- ✅ Nag eliminada — programa arranca directamente en modo licenciado.
- ✅ AccessViolation resuelto mediante nopeo del subcall problemático.
- ✅ About muestra "Licensed to:" confirmando el estado registrado.

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (2005)
- Herramientas: OllyDbg 1.10, PEiD 0.94, ImpRec 1.6, ResHacker 3.4
- Contacto original del autor: syxe00@yahoo.es
