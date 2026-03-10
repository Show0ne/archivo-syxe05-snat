# 545 — Visual Protect — Web Boomerang 3.0

| Campo          | Detalle                                        |
|----------------|------------------------------------------------|
| **Programa**   | Web Boomerang 3.0 (wbb.exe + wbmerang.exe)     |
| **Protección** | Visual Protect + Trial 30 días (vía vp.dll)    |
| **Objetivos**  | Desempacar ambos ejecutables y eliminar el Trial |
| **Dificultad** | Muy fácil                                      |
| **Herramientas** | OllyDbg v1.10, ImpRec 1.6, PEiD 0.94        |
| **Autor**      | SyXe'05 — [hAcK-c0d3d] — [CracksLatinoS]      |
| **Fecha**      | 09-11-2005                                     |
| **URL**        | http://www.filestream.com                      |

---

## Identificación del packer

PEiD y RDG identifican la protección como **Visual Protect** aunque sin indicar
versión exacta. Protección antigua, sin antidebug ni PE header roto.

La gestión del Trial la realiza completamente **vp.dll**, librería que acompaña
al ejecutable. El dumpeado final no la importa, por lo que el Trial desaparece
automáticamente.

---

## Parte 1 — wbb.exe

### Localización del OEP

Se aplica el método de excepciones (Narvaja): se van superando todas las
excepciones con **Shift+F9** anotando la última. Entre excepción y excepción
aparece la nag del programa — se elige "Try" y se continúa.

Tras la última excepción se coloca un **BPM en la primera sección** y se
supera con Shift+F9. OllyDbg para por escritura (no ejecución) en un bucle
interno. Se tracean los bucles hasta alcanzar el OEP:

```
OEP: 004A326B
```

### Dump

Se vuelca con **OllyDump**:
- Pulsar **"Get EIP as OEP"** antes de Dump.
- **Desmarcar** "Rebuild IAT".
- Guardar como `tute.exe`.

### Localización de la IAT

Desde el primer CALL inválido tras el OEP:
```
004A3291  FF15 60445000  CALL DWORD PTR DS:[504460]
```
Se hace **"Follow in dump → Memory address"** para aterrizar en la IAT.

| | Dirección |
|---|---|
| Inicio IAT | `504000` |
| Final IAT  | `504A14` |
| Size       | `A14`    |

```
504A14 - 504000 = A14
```

### IAT Scrambled — salto mágico

Algunos punteros apuntan a zonas del tipo `:F1Cxxx` creadas por el packer en
tiempo de ejecución. Para encontrar el salto mágico:

1. Se elige una entrada mala, p.ej. `[504268] == F1C0E8`.
2. Se coloca un **HBPWD** en esa dirección.
3. Se reinicia Olly con todas las excepciones tildadas y se pulsa F9.
4. Tras varios REP MOVS el HBP para justo donde se escriben los bytes finales.

Se localiza el bucle de tratamiento de la IAT y dentro de él el call a
`GetProcAddress`. Entrando en el subcall se encuentran **dos saltos mágicos**
consecutivos que comprueban si la DLL es kernel32 o user32 para redirigir la
entrada.

Las DLLs problemáticas son:

| DLL      | Rango IAT           |
|----------|---------------------|
| kernel32 | `504268` – `504548` |
| user32   | `504600` – `504944` |
| ntdll    | Tratada como kernel |

Para estas DLLs el valor correcto de la API queda en **ECX** en lugar de EAX.

### Script OllyDbg

Se colocan HBPs en:
- `880038` — primer salto mágico
- `880049` — instrucción `MOV EBX, EAX` donde se hace el cambio

```asm
inicio:
eob vamos
run

vamos:
CMP eip, 880038
jne no_cambio
MOV eip, 880042
jmp inicio

no_cambio:
CMP eip, 880049
JNE termina
CMP esi, 77e40000
JE cambio
CMP esi, 77d10000
JE cambio
JMP inicio

cambio:
MOV ebx, ecx
MOV eax, ecx
jmp inicio

termina:
ret
```

Al terminar el script se queda detenido en el OEP con la IAT correctamente
reparada.

### Reconstrucción IAT con ImpRec 1.6

```
OEP : A326B       (= 4A326B - 400000)
RVA : 104000      (= 504000 - 400000)
Size: A14
```

Quedó una entrada sin resolver — se repara con **"Trace Level1 (Disasm)"** o
siguiendo la entrada mala con "Follow DWORD in Disassembler" para localizar la
API (`GetProcAddress`). Se aplica **Fix Dump** sobre `tute.exe` → genera
`tute_.exe`.

---

## Parte 2 — wbmerang.exe

Mismo packer, misma vp.dll. Proceso análogo con diferencias menores.

### OEP

Se desactivan todas las excepciones, se pulsa F9, aparece la nag. Con la nag
en pantalla se abre el **Memory Map** (Alt+M) y se pone un BPM en la primera
sección. Se acepta la nag y Olly para por lectura (no ejecución). Se quita el
BPM, se tracean los bucles hasta el salto al OEP mediante
`JMP DWORD PTR [ESP-4]`:

```
OEP: 00416F5B
```

### IAT

Entradas malas apuntan a zonas `:BFFxxx`. El packer trata `GetProcAddress` de
forma especial: la redirige a `:6600E0` dentro de vp.dll en lugar de a la API
real.

### Script OllyDbg

HBPs necesarios: OEP (`416F5B`), primer mágico (`660038`), cambio de
registros (`660049`).

```asm
inicio:
eob vamos
run

vamos:
CMP eip, 660038
jne no_cambio
MOV eip, 660042
jmp inicio

no_cambio:
CMP eip, 660049
JNE termina
CMP esi, 77e40000
JE cambio
CMP esi, 77d10000
JE cambio
JMP inicio

cambio:
MOV ebx, ecx
MOV eax, ecx
jmp inicio

termina:
ret
```

### Reconstrucción IAT con ImpRec 1.6

`GetProcAddress` queda sin resolver tras el script — se repara manualmente
desde ImpRec. Se aplica **Fix Dump** → genera `tute1_.exe`.

> ⚠️ Renombrar `tute1_.exe` como `wbmerang.exe` para que funcione la
> integración con el menú de `wbb.exe` (Copy Wizard).

---

## Resultado

- ✅ `wbb.exe` desempacado y funcional (`tute_.exe`).
- ✅ `wbmerang.exe` desempacado y funcional (`tute1_.exe`).
- ✅ Trial eliminado — vp.dll no aparece en la IAT del dumpeado y puede
  borrarse de la carpeta sin efecto alguno.

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (2005)
- Herramientas: OllyDbg 1.10, ImpRec 1.6, PEiD 0.94
- Contacto original del autor: syxe00@yahoo.es
