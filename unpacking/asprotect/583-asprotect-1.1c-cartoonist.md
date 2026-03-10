# 583 — ASProtect 1.1c — Cartoonist 1.1 (1ª parte: Desempacado)

| Campo          | Detalle                                                          |
|----------------|------------------------------------------------------------------|
| **Programa**   | Cartoonist 1.1                                                   |
| **Protección** | ASProtect 1.1c + nags + watermark en imágenes creadas            |
| **Objetivos**  | Desempacado de ASProtect 1.1c (1ª parte)                         |
| **Dificultad** | La IAT casi agota la paciencia del cracker ;-)                   |
| **Herramientas** | OllyDbg v1.10, PEiD 0.94, ImpRec 1.6                          |
| **Autor**      | SyXe'05 — [hAcK-c0d3d] — [CracksLatinoS]                        |
| **Fecha**      | 04-01-2006                                                       |
| **URL**        | http://www.helpandmanual.com                                     |

---

## Identificación del packer

PEiD detecta **ASProtect 1.1c → Alexey Solodovnikov**. Una de las versiones más
antiguas del packer. A diferencia de versiones modernas, no usa el método
PUSHAD/POPAD. El único antidebug presente es la detección vía `IsDebuggerPresent`
— no hace falta un HideDebugger sofisticado.

EP típico de ASProtect, sin cambios en múltiples versiones.

---

## Localización del OEP

Se usa el **método de las excepciones** (método de Ricardo): se destildan todas
las excepciones en `Options → Debugging options → Exceptions` para que Olly
pare en cada una. Se supera cada excepción con Shift+F9 anotando la última.

La última excepción en la máquina del autor es una instrucción ilegal
(`Illegal use of register`) en `00DC0506`. Conocida la última excepción:

1. Reiniciar con Ctrl+F2.
2. Llegar hasta esa excepción.
3. En lugar de superarla, abrir Memory Map (Alt+M).
4. Colocar **BPM on access** en la primera sección de código (inmediatamente
   después del PE header).
5. Superar la excepción con Shift+F9 → aterrizaje en el OEP.

```
OEP: 00401000
```

Compilador **MASM/TASM** (inicio en `401000` con un `JMP`, sin stolen bytes).

---

## Delimitación de la IAT

Entrando en el primer CALL del OEP (`401022`) se llega a la Jump Table — está
completamente cascada, ningún nombre de API visible, todo redirigido.

Se hace "Follow in dump → Memory Address" sobre cualquier JMP de la tabla y se
navega hacia arriba para encontrar el inicio. La IAT está muy agujereada
(abundantes ceros entre DLL y DLL).

| | Dirección / RVA |
|---|---|
| Inicio IAT | `0062F124` (RVA `22F124`) |
| Final IAT  | `00630084` (RVA `230084`) |
| Size       | `F64`                     |

**Datos para ImpRec:**
```
OEP : 00001000
RVA : 0022F124
Size: 00000F64
```

> No hay Stolen Bytes — se puede dumpear directamente desde el OEP.

---

## Dump inicial

OllyDump con las opciones habituales:
- `Fix Raw Size & Offset of Dump Image` ✓
- `Rebuild Import` ☐ (destildado)
- Entry Point: `Get EIP as OEP`

Se guarda como `tute.exe`.

---

## Estructura interna del packer — tres zonas de relleno de IAT

ASProtect 1.1c tiene **tres zonas distintas** de relleno de IAT según el tipo
de librería, discriminadas por el **Identificador de DLL** que retorna en `BL`
a la salida del `CALL 00DB2768`:

```asm
00DBF038  E8 2B37FFFF  CALL 00DB2768    ; obtiene Id. DLL en BL
00DBF03D  80EB 02      SUB BL, 2
00DBF040  74 0E        JE SHORT 00DBF050  ; → Zona 1 (kernel, user…)
00DBF042  80EB 02      SUB BL, 2
00DBF045  0F84 990000  JE 00DBF0E4        ; → Zona 2 (version, commdlg32, shell32)
00DBF04B  E9 36010000  JMP 00DBF186       ; → Zona 3 (gdi32…)
```

**Zona 1** (`DBF050`) — kernel32, user32, etc.: usa el call semi-mágico.  
**Zona 2** (`DBF0E4`) — version.dll, commdlg32.dll, shell32.dll: **sin call
mágico**, desencripción distinta, IAT rota irremediablemente.  
**Zona 3** (`DBF186`) — gdi32, etc.: llama directamente a `GetProcAddress` y
guarda el resultado.

### Tabla de la IAT interna del packer

El packer mantiene una tabla en memoria con el siguiente formato:

| Byte(s) | Significado |
|---------|-------------|
| nombre + `\0` | Nombre de la DLL (en claro) |
| `01`/`02`/`04`... | Identificador de DLL |
| `4A` | Identificador de api (delimita cada entrada) |
| longitud | Tamaño del nombre de la api |
| nombre | Nombre de la api **encriptado** |
| `5A` | Separador de DLL (indica fin de bloque) |

Cada api se desencripta con una **llave distinta** (sin patrón fijo), lo que
hace imposible recuperar las de la Zona 2 desde fuera.

---

## Localización del call semi-mágico

Se coloca un **BPM on Write** en la primera entrada redirigida de la Jump Table
(`[62F350]`, valor final `DD0334`). Se hace correr el programa hasta que EAX
contiene ese valor. Subiendo en el código se llega al par de CALLs
característicos de ASProtect donde opera el semi-mágico:

```
call semi_mágico: 00DBF0D6
```

Al pasarlo con F8 la API válida que estaba en EAX se reemplaza por un valor
"malo" de ASProtect — confirma que este CALL es el responsable de la
redirección.

---

## Script OllyScript para recuperar la IAT (solución al CRC)

ASProtect 1.1c detecta nopeos directos mediante un chequeo CRC de la zona.
La solución es un **nopeo virtual vía script** que redirige EIP sin modificar
bytes en memoria:

```
; script.txt
inicio:
  eob vamos           ; si hay excepción salta a "vamos"
  run                 ; deja correr el programa

vamos:
  cmp eip, 0DBF0D6    ; ¿estamos en el mágico?
  jne no_es
  mov eip, 0DBF0DB    ; sí → redirigir EIP (nopeo simulado)
  jmp inicio

no_es:
  cmp eip, 0DBF439    ; ¿POPAD? (freno = fin del trabajo de IAT)
  je termina
  jmp inicio

termina:
  ret
```

### Procedimiento de ejecución

1. Reiniciar Olly — excepciones **destildadas** (queremos que pare).
2. Dar RUN → para en primera excepción.
3. Tildar excepciones (para que no pare en ellas).
4. `Ctrl+G` → `0DBF0D6` — poner BP.
5. Superar excepción con Shift+F9 → cae en el mágico.
6. Quitar el BP y poner **HE (Hardware Execute)** en `00DBF0D6`.
7. Poner otro **HE** en `00DBF439` (POPAD = freno).
8. `Plugins → OllyScript → Run script...` → cargar `script.txt`.

> ⚠️ Los dos HE son obligatorios. Si falta alguno el script no funciona.

Al terminar el script aparece "Script finished" y Olly queda parado en
`0DBF439` (el POPAD).

### Regreso al OEP tras el script

1. Activar excepciones (quitar tildes).
2. F9 → ir superando excepciones con Shift+F9.
3. En la última: Alt+M → BPM en sección de código → Shift+F9 → OEP.

---

## Reconstrucción IAT con ImpRec 1.6

Tras el script, ImpRec muestra **14h (20 decimal) entradas sin resolver**.
Sin el script habrían sido más de 300.

### Entradas reparables con herramientas

| RVA      | Apunta a   | API correcta          | Método de reparación        |
|----------|------------|-----------------------|-----------------------------|
| `22F350` | `0DD0334`  | `CloseHandle`         | Trace Level1 (Disasm)       |
| `22F3F8` | `0DBC208`  | `GetProcAddress`      | Plugin ASProtect 1.22 / Disassemble+HexView |

### Entradas de las 3 DLLs problemáticas (18 entradas manuales)

Las 18 entradas restantes pertenecen a **version.dll**, **commdlg32.dll** y
**shell32.dll** (Zona 2 del packer). No pueden resolverse desde ImpRec
automáticamente.

**Método de recuperación por traceo con BP en JMPs:**

1. Buscar referencias a las entradas redirigidas con Ctrl+R sobre los bytes
   de la IAT.
2. Seleccionar todos los JMPs encontrados → botón derecho → "Set breakpoint
   on every command".
3. Dejar correr el programa desde el OEP con F9.
4. Cuando Olly para en un BP: activar el Log (botón `...`) → "Log to file"
   → tracear con F7 entrando en el código del packer.
5. En el Log se ve el nombre completo de la API y su DLL.
6. Retirar el BP del JMP ya identificado, repetir para el siguiente.
7. En ImpRec: doble clic sobre la entrada → seleccionar módulo y API → OK.

**Ejemplo — entrada `[62F544]`:**
```
JMP: 005D4B0E - FF25 44F56200  JMP DWORD PTR DS:[62F544]
RVA en ImpRec: 22F544
API encontrada en Log: GetFileVersionInfoSizeA  (version.dll)
```

### Entrada no detectable por BP (API no llamada en runtime)

La entrada `RVA 22F660` (apunta a `DD46B0`) corresponde a una API que el
programa **nunca ejecuta**, por lo que el método de BP no la hace saltar.

**Método alternativo — forzar ejecución:**
1. Pausar Olly con F12.
2. Ir a `005D4BD6` (`JMP DWORD PTR DS:[62F660]`).
3. Colocar EIP allí con "New origin here".
4. Entrar con F7 al código del packer y tracear.
5. El packer desencripta el nombre de la API — se ve en la ventana dump.

**API encontrada:** `PrintDlgA` (commdlg32.dll) — función de imprimir no
utilizada en el programa.

### Tabla completa de entradas manuales

| RVA      | DLL           | API                        |
|----------|---------------|----------------------------|
| `22F540` | version.dll   | —                          |
| `22F544` | version.dll   | GetFileVersionInfoSizeA    |
| `22F548` | version.dll   | —                          |
| `22F654` | comdlg32.dll  | (grupo de 4 entradas)      |
| `22F658` | comdlg32.dll  | GetOpenFileNameA           |
| `22F65C` | comdlg32.dll  | GetSaveFileNameA           |
| `22F660` | comdlg32.dll  | PrintDlgA                  |
| `22F998` | shell32.dll   | DragAcceptFiles            |
| `22F99C` | shell32.dll   | DragQueryFileA             |
| `22F9A0` | shell32.dll   | DragQueryPoint             |
| `22F9A4` | shell32.dll   | ShellExecuteA              |
| `22F9A8` | shell32.dll   | Shell_NotifyIconA          |

> ⚠️ ImpRec puede asignar automáticamente `AdjustWindowRectExA` (user32) a
> todas estas entradas si se usa "Trace Level1 (Disasm)" sin discriminación —
> son en realidad de commdlg32 y shell32. No confiar en esa reparación
> automática.

---

## Fix Dump y resultado

Con todas las entradas resueltas en ImpRec se aplica **"Fix Dump"** sobre
`tute.exe` → genera `tute_.exe`.

- ✅ ASProtect 1.1c desempacado correctamente.
- ✅ IAT completamente reparada (481 funciones importadas, 13 módulos).
- ✅ `tute_.exe` arranca y muestra la interfaz de Cartoonist 1.1.
- ⏳ Eliminación de nags y watermark → **2ª parte** (writeup `cartoonist_parte2`).

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (2006)
- Herramientas: OllyDbg 1.10, PEiD 0.94, ImpRec 1.6
- Script: OllyScript 0.92
- Contacto original del autor: syxe00@yahoo.es
