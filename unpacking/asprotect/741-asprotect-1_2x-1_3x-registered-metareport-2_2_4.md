# 741 — MetaReport 2.2.4 — ASProtect 1.2x–1.3x [Registered]

| Campo            | Detalle                                                                        |
|------------------|--------------------------------------------------------------------------------|
| **Programa**     | MetaReport 2.2.4                                                               |
| **Protección**   | ASProtect 1.2x – 1.3x [Registered]                                            |
| **Objetivos**    | Desempakar y conseguir que funke                                               |
| **Dificultad**   | Bastante sencillo                                                              |
| **Herramientas** | OllyDbg v1.10, PEiD v0.93, ImpREC v1.6, ConTEXT v0.98.3, RDG packer v0.6.3 Beta (opcional) |
| **Autor**        | SyXe'05 — [hAcK-c0d3d] — [CracksLatinoS]                                      |
| **Fecha**        | 05-02-2006                                                                     |
| **URL**          | http://www.metamatica.com                                                      |

> **Nota:** Este tute estudia ASProtect 1.2x–1.3x en versión **sin stolen code**,
> centrándose en la técnica de reparación de IAT mediante OllyScript.
> El archivo del título del PDF (`Estudio de ASProtect 2.xx`) es incorrecto —
> el contenido real corresponde a la versión 1.2x–1.3x.

---

## Identificación

PEiD v0.93 detecta:

```
ASProtect 1.2x - 1.3x [Registered] -> Alexey Solodovnikov
```

> RDG Packer en modo M-B detecta incorrectamente ASPack v2.12.

---

## Llegando al OEP

Se carga `MetaReport.exe` en OllyDbg con las excepciones desactivadas y se
aplica el **método de Ricardo** (superar excepciones sucesivas hasta la última).

Al llegar a la última excepción se pone un **BPM on access** en la primera
sección de código y se supera con `SHIFT+F9`. Olly para directamente en el
**OEP**:

```
OEP == 00631BF8
```

```asm
00631BF8  55            PUSH EBP       ; OEP!!!
00631BF9  8BEC          MOV EBP, ESP
00631BFB  83C4 F0       ADD ESP, -10
00631BFE  53            PUSH EBX
00631BFF  E8 F0126300   MOV EAX, 006312F0
```

Sin stolen bytes — esta versión no los usa.

---

## Análisis de la protección IAT

Esta versión de ASProtect usa una técnica compleja para proteger la IAT:

1. **Intercepta** el momento de rellenar la IAT.
2. **Crea una sección temporal** donde copia código inerte.
3. **Crea una segunda sección temporal**.
4. Al final de la primera sección introduce un **PUSH–RET** que salta a la segunda.
5. En la segunda sección copia **parte de la API interceptada** + salto a mitad de ella.
6. **Reemplaza** los `JMP DWORD PTR [POS_IAT]` por `CALL ASPROTECT`.

Hay APIs que **emula por completo** (GetCommandLineA, GetCurrentProcessId,
GetVersion...) y un caso especial: **GetProcAddress** — se intercepta de forma
diferente a las demás.

La JMP Table queda con saltos mezclados: algunos `JMP [POS_IAT]` normales y
otros `CALL ASPROTECT` que apuntan a secciones temporales que no existirán en
el dump.

---

## Los 5 puntos de escritura en la JMP Table

Se coloca un **BPM on Memory Write** en el byte `0x3C` de `00401328`
(primer salto de la tabla, evitando el opcode `FF25`). Se deshabilitan
excepciones marcando *"Ignore memory access violations in KERNEL32"*.

Tras varias paradas se identifican **5 zonas distintas** donde el packer
escribe en la tabla:

| Zona      | Dirección     | Tipo       | Registros clave                     |
|-----------|---------------|------------|-------------------------------------|
| `calls`   | `014F3AEE`    | CALL ASP   | EAX=bytes del CALL, EBP=API, ESI=dirección |
| `jmps`    | `014F5E4F`    | JMP normal | EAX=bytes del JMP, EBP=API, ESI=dirección |
| `jmps1`   | `014F5D53`    | JMP normal | igual que `jmps`                    |
| `push`    | `01730561`    | PUSH–RET   | EAX=bytes, EDI=API, ECX=dirección   |
| especial  | `014F5EA2`    | GetProcAddress | caso especial — se repara manualmente |

Punto de convergencia (posible gatillo): `014F5B0F` — todos los puntos
anteriores saltan allí al terminar de escribir.

---

## OllyScript para reparar la IAT

La IAT reparada se ubicará a partir de `0063F000` (zona libre del ejecutable).

El script intercepta cada uno de los 4 HBPs (el punto `014F5EA2` de
GetProcAddress se omite — se repara a mano), guarda la API en la nueva IAT
y corrige el JMP/CALL para que apunte allí.

> **Problema conocido:** el script falla en el segundo salto a GetProcAddress
> (`004079E4`). Solución: usar el comando `PAUSE` para pausar el script
> condicionalmente al llegar a esa dirección, reparar manualmente, y
> continuar con `RESUME`.

```
var flag             // bandera de primera pasada
var api              // api actual
var base             // imagebase de la DLL
var pos_iat          // puntero a la nueva IAT
var aux              // variable auxiliar 1
var aux1             // variable auxiliar 2
var ayu              // variable auxiliar 3
var otra             // variable auxiliar 4
var direccion        // variable auxiliar 5

mov pos_iat, 63f000  // ubicación de la nueva IAT
mov flag, 0

inicio:
dbh                          // ocultar debugger
bp 631BF8                    // BP en OEP
bphws 014f3AEE, "x"          // HBP 1: zona de CALLs
bphws 014f5E4F, "x"          // HBP 2: zona de JMPs
bphws 014f5D53, "x"          // HBP 3: zona de JMPs (variante)
bphws 01730561, "x"          // HBP 4: zona de PUSHes
eob vamos
run

vamos:
cmp eip, 014f3AEE
je calls
cmp eip, 014f5E4F
je jmps
cmp eip, 014f5D53
je jmps1
cmp eip, 01730561
je push
jmp termina

// --- Procedimiento CALLs ---
calls:
mov api, ebp
log api
cmp flag, 0
jne otra_vez
GMI api, MODULEBASE
mov base, $RESULT

iguales:
mov aux, ebx
mov direccion, ebx
cmp direccion, 4079dc       // ¿es el salto problemático?
je pausamos
log direccion
mov [pos_iat], api
mov [aux], #FF25#            // reparar el CALL → JMP [pos_iat]
add aux, 2
mov [aux], pos_iat
log pos_iat
add pos_iat, 4
mov flag, 1
mov eip, 014F3AF4
jmp inicio

otra_vez:
GMI api, MODULEBASE
cmp base, $RESULT
je iguales
mov base, $RESULT
add pos_iat, 4
jmp iguales

// --- Procedimiento JMPs ---
jmps:
mov direccion, esi
sub direccion, 2
cmp direccion, 4079dc
je pausamos
log direccion
mov api, ebp
log api
cmp flag, 0
jne sgute
GMI api, MODULEBASE
mov base, $RESULT

salvo:
mov otra, esi
mov [pos_iat], api
mov [otra], pos_iat
log pos_iat
add pos_iat, 4
mov flag, 1
mov eip, 014F5E51
jmp inicio

sgute:
GMI api, MODULEBASE
cmp base, $RESULT
je salvo
mov base, $RESULT
add pos_iat, 4
jmp salvo

// --- Procedimiento JMPs1 ---
jmps1:
mov direccion, esi
sub direccion, 2
cmp direccion, 4079dc
je pausamos
log direccion
mov api, ebp
log api
cmp flag, 0
jne sgute1
GMI api, MODULEBASE
mov base, $RESULT

salvo1:
mov aux1, esi
mov [pos_iat], api
mov [aux1], pos_iat
log pos_iat
add pos_iat, 4
mov flag, 1
mov eip, 014f5D55
jmp inicio

sgute1:
GMI api, MODULEBASE
cmp base, $RESULT
je salvo1
mov base, $RESULT
add pos_iat, 4
jmp salvo1

// --- Procedimiento PUSHes ---
push:
mov direccion, ecx
sub direccion, 2
cmp direccion, 4079dc
je pausamos
log direccion
mov api, edi
log api
cmp flag, 0
jne sigo
GMI api, MODULEBASE
mov base, $RESULT

salvar:
mov ayu, ecx
mov [pos_iat], api
mov [ayu], pos_iat
log pos_iat
add pos_iat, 4
mov flag, 1
jmp inicio

sigo:
GMI api, MODULEBASE
cmp base, $RESULT
je salvar
mov base, $RESULT
add pos_iat, 4
jmp salvar

pausamos:
pause                        // pausa condicional para reparar manualmente
add pos_iat, 4
jmp inicio

termina:
bc 631BF8
bphwc 014f3AEE
bphwc 014f5E4F
bphwc 014f5D53
bphwc 01730561
MSG "Dumpea ahora y repara la iat con el ImpRec :)"
ret
```

### Uso del script

1. Abrir el ejecutable **empacado** en Olly y llegar hasta que la JMP Table
   esté intacta.
2. Navegar a `00401328` en el DUMP y poner **BPM on Memory Write** en byte `0x3C`.
3. Pulsar F9 — a la tercera parada Olly está en `014F5E4F`.
4. Hacer **New Origin Here** una instrucción antes.
5. Lanzar el script: `Plugins → OllyScript → Run Script`.

### Pausa en `004079DC` (GetPrivateProfileStringA)

El script se pausa al llegar al salto problemático. En ese momento:

```
EBP = kernel32.GetPrivateProfileStringA
ESI = 004079DE  (dirección del salto)
```

Se salva la API manualmente en la siguiente posición libre de la IAT y se
ajusta el JMP para que apunte allí. Luego se avanza el EIP a `014F5D55` y
se reanuda el script con `Plugins → OllyScript → Resume`.

### Reparación manual de GetProcAddress

Al finalizar el script quedan dos saltos sin reparar:

```
004013F8  JMP [1518C74]   → GetProcAddress
004079E4  JMP [151910C]   → GetProcAddress
```

Se inserta la API en la IAT y ambos JMPs se redirigen a la misma entrada.

---

## Datos de IAT y dump

| Dato          | Valor      |
|---------------|------------|
| OEP (RVA)     | `00231BF8` |
| Inicio IAT    | `63F000`   |
| Final IAT     | `63F9A0`   |
| Longitud IAT  | `9A0`      |

Se dumpea con OllyDump: **Rebuild Import desactivado**, Entry Point → `231BF8`.

En ImpREC:

| Campo | Valor        |
|-------|--------------|
| OEP   | `00231BF8`   |
| RVA   | `0023F000`   |
| Size  | `000009A0`   |

Se pulsa **Get Imports** → todas las funciones resueltas. **Fix Dump** →
`dumpeado_.exe` arranca perfectamente.

---

## Registro del programa

Tras el desempacado el programa muestra una barra inferior:
*"Evaluation version - day 30 of 45. Click here to order..."*

### Flag de registro: `[637EEC]`

Al pulsar ABOUT, Olly para en una rutina verificadora. Se localiza la variable
de estado en `[637EEC]` (vacía en el dump).

El programa la usa como **puntero** a los datos de licencia. Se escribe en
`0063EBC` el siguiente contenido:

```
0063EBBC: 0A 0D 53 79 58 65 27 30 35 04 0D 43 72 61 63 6B  →  \n\rSyXe'05\nCrack
0063EBCC: 73 4C 61 74 69 6E 6F 53                           →  sLatinoS
```

(`0x0D0Ah` = salto de línea — el programa lo usa como delimitador de campos)

Se actualiza el puntero `[637EEC]` → `0063EBBC`.

El About muestra:

```
Licensed to
SyXe'05
CracksLatinoS
Single license
```

### Flag de modo debug: `[637EF4]`

Buscando referencias a la cadena `"****DEBUG BUILD****"` se localiza otra
variable en `[637EF4]` que cuando vale `0` activa el modo debug/trial.

La única zona donde se modifica:

```asm
0062B994  C705 F47E6300  MOV dword ptr [637EF4], -1   ; activa modo registrado
```

Se pone `[637EF4] = FFFFFFFF` directamente desde el dump antes de ejecutar.

Con ambas modificaciones el programa arranca sin cadenas EVALUATION ni TRIAL.

### Guardar los cambios

Se seleccionan todas las modificaciones en Olly y se hace
**Copy to Executable → All Modifications → Save File**.

---

## Resultado

- ✅ **Desempacado** limpio con IAT completamente reparada vía OllyScript.
- ✅ **GetProcAddress** reparado manualmente (2 entradas).
- ✅ **Registrado** — About muestra nombre y organización.
- ✅ Sin cadenas EVALUATION/TRIAL/DEBUG BUILD.
- ✅ Sin expiración — el contador de días lo llevaba el packer.

---

## Notas técnicas

- Esta versión de ASProtect **no tiene stolen bytes** — diferencia importante
  respecto a las versiones RC4.
- El packer usa **5 zonas distintas** para escribir en la JMP Table, con
  registros y comportamientos diferentes en cada una.
- `GetProcAddress` tiene su propia zona especial (`014F5EA2`) — no compatible
  con los 4 HBPs disponibles → reparación manual obligatoria.
- El comando `PAUSE` de OllyScript es clave para manejar el salto problemático
  en `004079DC` sin dividir el script en dos.
- La variable `[637EEC]` actúa como puntero a los datos de licencia — si apunta
  a NULL el programa entra en modo Trial; si apunta a datos válidos, registrado.

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (05-02-2006)
- Herramientas: OllyDbg 1.10, PEiD 0.93, ImpREC 1.6, ConTEXT 0.98.3
- Contacto original: syxe05@gmail.com
