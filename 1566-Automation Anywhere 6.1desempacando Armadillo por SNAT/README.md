# 1566 — Automation Anywhere 6.1 — Armadillo

| Campo            | Detalle                                                                              |
|------------------|--------------------------------------------------------------------------------------|
| **Programa**     | Automation Anywhere 6.1 (`Automation Anywhere.exe`)                                 |
| **Protección**   | Armadillo (proceso único, sin CopyMem-II ni Nanomites) + Import Table Elimination + Code Splicing |
| **Objetivos**    | Desempacar, reparar IAT, sortear limitaciones de la versión trial, resolver el misterio de `ArmAccess.dll` e inyectar una DLL permanente en el ejecutable |
| **Dificultad**   | Alta — VB6, anti-debug múltiple, hooks en APIs del sistema, inyección manual de código |
| **Herramientas** | OllyDbg 1.10, Hide OllyDbg v0.1, ODbgScript v1.67.0, Protection iD v0.6.6.7, Scylla x86 v0.9.6b, LordPE Deluxe, WinHex 17.8, Topo v1.2, VB Decompiler v10.0 |
| **Autor**        | Snat — [CrackSLatinoS]                                                              |
| **Fecha**        | Agosto 2015                                                                          |
| **URL**          | http://www.automationanywhere.com                                                    |

---

## Introducción

Automation Anywhere 6.1 es una herramienta de automatización de tareas con grabación de pantalla, workflows, automatización remota y más. La versión trial tiene numerosas limitaciones que bloquean funciones como la creación de EXEs, el Deploy Manager, el Workflow o el Schedule Manager. El tutorial cubre el proceso completo desde el desempacado hasta una solución permanente que no requiere ningún archivo externo.

---

## Identificación del packer

```
Protection iD → Armadillo
LordPE       → proceso único (single process)
               descarta: CopyMem-II, Nanomites
               posible: Import Table Elimination, Code Splicing
```

El ejecutable arranca con un `PUSHAD` — señal inequívoca de stub de packer.

---

## Desempacado

### Anti-debug: OutputDebugStringA

Armadillo llama a `OutputDebugStringA` con cadenas muy largas que provocan el cierre de OllyDbg. Se parcheará la API:

```asm
; Ir a OutputDebugStringA con Ctrl+G
; Parchear los primeros bytes por:
RET 4     ; retorna extrayendo el único parámetro (PUSH EAX previo)
; Bytes: C2 04 00
```

Colocar BP en el `RET 4` parcheado.

### Flujo de desempacado paso a paso

1. Añadir excepción `0xC000001E` (INVALID LOCK SEQUENCE) a la lista de excepciones de Olly.
2. BP en `VirtualProtect` → dar RUN → pasar el cartel inicial con Shift+F9.
3. Olly para en `VirtualProtect` — la llamada es para la dirección `0x3791000`.
4. Llegar al RET con `Ctrl+F9` → se sale a un loop → BP en el RET del loop → F9.
5. Tracear con F8 identificando los dos `OutputDebugStringA` → aplicar `New Origin Here` en la línea siguiente a cada uno, o usar el parche del paso anterior.
6. Al pasar el call en `0x0380C0D9` aparece un segundo cartel → pasar con Shift+F9.
7. Continuar con F8 hasta llegar al call que genera la nagscreen inicial → entrar con F7.
8. Tracear hasta `CALL EAX` → entrar con F7 → **OEP encontrado**:

```
OEP == 0x0044E388   (Visual Basic 6 — msvbvm60.ThunRTMain)
```

Colocar HBP en el OEP para regresar fácilmente.

---

## IAT — Reparación

### Delimitación

```
Inicio IAT: 0x00401000
Final IAT:  0x004015A0
Largo IAT:  0x15A0 bytes
```

### Puntero malo

Solo hay un puntero malo: `__vbaEnd` (de `MSVBVM60.DLL`). Se localiza su origen rastreando el loop de relleno de IAT de Armadillo:

```
Colocar HBP on Write en 0x00401078 (dos entradas antes del malo)
→ Olly para en la rutina de relleno
→ Localizar el salto que diferencia entradas buenas de malas
→ Cambiar ZeroFlag para que no salte → fuerza la escritura de __vbaEnd
```

La API correcta es `__vbaEnd` de `MSVBVM60.DLL`.

### Añadir GetProcAddress y GetModuleHandleA a la IAT

El ejecutable VB no tiene estas APIs directamente — se añaden manualmente:

```
GetProcAddress:   0x7C80AE40 → colocar en IAT
GetModuleHandleA: 0x7C80B741 → colocar en IAT
```

Longitud final de IAT ajustada: `0x15A8` (añadidos 2 punteros × 4 bytes).

### Dump con Scylla

```
Proceso:    Automation Anywhere.exe
OEP:        0x0044E388
IAT inicio: 0x00401000
IAT size:   0x15A8

→ Get Imports → Show Invalid → Cut Thunks (eliminar separadores de DLLs)
→ Dump  → Automation Anywhere_dump.exe
→ Fix Dump → Automation Anywhere_dump_SCY.exe
```

### Parche final — __vbaEnd

El dumpeado se cierra al llegar a un salto que no se toma y ejecuta `__vbaEnd`. Se nopea el salto y se fuerza el JMP:

```asm
; Localización: tracear desde 0x021FFA10 con F8
; Salto problemático: no se produce → llega a __vbaEnd → cierra el programa
; Solución: parchear con JMP incondicional hacia el código de continuación
```

Guardar como `dumpeado.exe`.

---

## Sorteando las limitaciones

Lista completa de funciones bloqueadas en la versión trial:

| Función              | Restricción                        |
|---------------------|------------------------------------|
| Create EXE          | Solo versión Premier o superior    |
| Deploy Manager      | Solo versión Premier o superior    |
| Report Designer     | Premier Only + `n uses left`       |
| Workflow            | Premier Only + `n uses left`       |
| Task Priority       | Solo versión Premier               |
| Auto Login          | Solo versión Premier               |
| Object Recorder     | Solo versión Premier               |
| Web Service         | Integration Pack                   |
| Application-XML     | Premier o superior                 |
| Error Handling      | Premier o superior                 |
| Image Recognition   | Premier o superior                 |
| Screen Capture      | Premier o superior                 |
| App Integration     | Integration Pack                   |
| OCR                 | Integration Pack                   |
| Email Automation    | Integration Pack                   |
| Terminal Emulator   | Integration Pack                   |
| Schedule Manager    | Premier o superior                 |
| Snap Points         | Premier o superior                 |
| System Logs         | Premier o superior                 |
| ROI Calculator      | Premier o superior                 |

### Técnica de bypass (ejemplo: Create EXE)

1. Cargar `dumpeado.exe` en Olly con el programa en ejecución.
2. Pulsar `Create EXE` → aparece nagscreen.
3. BP en `DestroyWindow` → pulsar Cancel → Olly para.
4. Tracear con F8 saliendo de `msvbvm60.dll` hasta llegar al código del dumpeado.
5. Localizar los saltos condicionales en `0x0229360B`, `0x02293616`, `0x02293621`.
6. Modificar el ZeroFlag para que el salto en `0x0229360B` NO se ejecute y que el de `0x02293621` SÍ → la función crea el EXE.

El mismo patrón (nagscreen → DestroyWindow → tracear hacia atrás → localizar salto) se aplica al resto de funciones restringidas.

---

## ilap.exe y Armadillo

El directorio de instalación contiene `ilap.exe`, también protegido con Armadillo. Gestiona las licencias del programa y se comunica con `Automation Anywhere.exe` mediante mecanismos IPC.

---

## En busca de la nag perdida

La nagscreen inicial ("Try It!") es generada por `ArmAccess.dll` a través de la función `ShowReminderMessage`:

```asm
; Ruta de llamada:
DllFunctionCall("ArmAccess.dll", "ShowReminderMessage", ...)
  → LoadLibraryA("ArmAccess.dll")   ← EAX == 0 si no existe la DLL
  → GetProcAddress("ShowReminderMessage")
  → JMP EAX                         ← salta a la función
```

Si `ArmAccess.dll` no está presente → EAX = 0 → la nag no aparece.

---

## El misterio de ArmAccess

### Por qué el empacado no necesita ArmAccess.dll pero el dumpeado sí

Armadillo instala **ganchos** en las APIs del sistema. Al desempacar, el código que instalaba esos ganchos ya no está, pero las llamadas a las APIs hookeadas permanecen. Una de ellas es el mecanismo por el que el original saltaba por encima de `ArmAccess.dll`.

### Cómo Armadillo instala los hooks

Tras cargar `MSVBVM60.DLL` via `LoadLibraryA`, Armadillo:

1. Guarda la base de la DLL encriptada.
2. Entra en un doble loop (`0x037DD26C` → `0x037DD79A`) que itera sobre las APIs a hookear.
3. Para cada API: `GetProcAddress` → encripta la dirección → la guarda.
4. Usa `VirtualProtect` (PAGE_READWRITE) → sobrescribe los primeros bytes de la API con un JMP a su stub → restaura permisos (PAGE_EXECUTE_READ).

```asm
; Detección del anti-BP en LoadLibraryA
; Armadillo comprueba si el primer byte de LoadLibraryA es 0xCC (INT3)
; Si hay BP → toma un camino alternativo para esquivarlo

; Solución: BP condicional en la 3ª instrucción de LoadLibraryA (tras el push ebp)
; Condición: [ESP+8] == "MSVBVM60.DLL"  (tipo: Pointer to ASCII string)
```

### Localización del gancho en MSVBVM60.DLL

```
1. BP condicional en LoadLibraryA para MSVBVM60.DLL
2. Tracear hasta RET → guardar EAX (base de la DLL)
3. BPM on Write en toda la sección .text de MSVBVM60.DLL
4. RUN → Olly para donde el packer sobrescribe la IAT de la DLL

; Resultado: el doble loop de Armadillo instala hooks en:
;   __vbaEnd   ← la API mala de la IAT
;   y otras APIs de MSVBVM60
```

---

## Inyectando la DLL

La solución definitiva es **incrustar `ArmAccess.dll` dentro del propio ejecutable** y generar un injerto que la cree en disco al iniciar y la elimine al cerrar el programa. Sin archivos externos, sin dependencias.

### Preparación del ejecutable

Se eliminan las secciones sobrantes del packer con LordPE (`wipe section header`):

```
Secciones a eliminar: .text1, .adata, .data1, .pdata
LordPE → Rebuild PE
Tamaño reducido: ~8 MB menos
```

Con **Topo v1.2** se crea una única sección nueva para albergar la DLL y el injerto:

```
Tamaño: 50.000 (DLL) + 20.000 (injerto) = 70.000 bytes
Nombre sección: .ArmAcc  (DLL) / .injerto (código)
Sección .SCY renombrada → .IAT
```

### Layout de la sección

| Dirección     | Contenido                          |
|---------------|-----------------------------------|
| `0x03009000`  | Bytes de `ArmAccess.dll` (49.152 B)|
| `0x03015100`  | Strings: nombres de DLLs y APIs   |
| `0x03015230`  | `\ArmAccess.dll` (path relativo)  |
| `0x03015290`  | Bytes del gancho a ExitProcess    |
| `0x03015300`  | Tabla de punteros a APIs          |
| `0x03015500`  | **Nuevo Entry Point (injerto)**   |
| `0x03015800`  | Rutina de inicialización          |
| `0x03015C00`  | Función gancho de ExitProcess     |

### Nuevo Entry Point

```
Offset EP = 0x03015500 - 0x400000 = 0x02C15500
→ cambiar AddressOfEntryPoint en cabecera PE
```

### Tabla de APIs del injerto

| Dirección    | API                               |
|--------------|-----------------------------------|
| `0x03015300` | `kernel32.GetCurrentDirectoryA`  |
| `0x03015304` | `kernel32.LocalAlloc`            |
| `0x03015308` | `kernel32.CreateFileA`           |
| `0x0301530C` | `kernel32.WriteFile`             |
| `0x03015310` | `kernel32.CloseHandle`           |
| `0x03015314` | `kernel32.LoadLibraryA`          |
| `0x03015318` | `kernel32.FreeLibrary`           |
| `0x0301531C` | `kernel32.VirtualProtect`        |
| `0x03015320` | `kernel32.Sleep`                 |
| `0x03015324` | `kernel32.DeleteFileA`           |
| `0x03015328` | `kernel32.LocalFree`             |
| `0x0301532C` | `kernel32.SetEnvironmentVariableA`|
| `0x03015330` | `kernel32.ExitProcess`           |
| `0x03015334` | `msvcrt.strcat`                  |
| `0x004015A4` | `kernel32.GetProcAddress` (IAT)  |
| `0x004015A8` | `kernel32.GetModuleHandleA` (IAT)|

### Variables del injerto

| Dirección    | Variable                          |
|--------------|-----------------------------------|
| `0x3015350`  | Retorno de LocalAlloc             |
| `0x3015360`  | Handle de la DLL (CreateFileA)    |
| `0x3015370`  | Bytes originales de ExitProcess (7 B)|
| `0x3015380`  | pSecurity para CreateFileA       |
| `0x3015390`  | Bytes escritos por WriteFile      |
| `0x30153A0`  | Base de ArmAccess.dll en memoria  |
| `0x30153A4`  | Contador función gancho           |
| `0x30153A8`  | Base de kernel32.dll              |
| `0x30153AC`  | Base de msvcrt.dll                |
| `0x30153B0`  | Bytes originales ExitProcess (backup)|

### Gancho en ExitProcess

Los 7 bytes del gancho:

```asm
; Parche instalado en kernel32.ExitProcess:
68 00 5C 01 03   push 0x03015C00   ; dirección de la función gancho
C3               ret
90               nop
; Bytes: 68 00 5C 01 03 C3 90
```

### Lógica del injerto

```
[Nuevo EP: 0x03015500]
  │
  ├─ Inicialización (0x03015800)
  │    └─ GetModuleHandleA(kernel32) → GetProcAddress para todas las APIs
  │
  ├─ Comprobar ArmAccess.dll
  │    ├─ LoadLibraryA("\ArmAccess.dll")
  │    ├─ Si EAX != 0 → ya existe → FreeLibrary → saltar al OEP
  │    └─ Si EAX == 0 → no existe → continuar
  │
  ├─ Crear ArmAccess.dll en disco
  │    ├─ GetCurrentDirectoryA → LocalAlloc → strcat → path completo
  │    ├─ CreateFileA (atributo oculto FILE_ATTRIBUTE_HIDDEN)
  │    └─ WriteFile (bytes de ArmAccess.dll desde 0x03009000)
  │
  ├─ SetEnvironmentVariableA("TYPE", "AAENTERPRISE")  → About muestra Enterprise
  │
  ├─ Instalar gancho en ExitProcess
  │    ├─ VirtualProtect(ExitProcess, PAGE_READWRITE)
  │    ├─ Guardar 7 bytes originales en 0x3015370
  │    ├─ Escribir parche: push 0x03015C00 + RET
  │    └─ VirtualProtect(ExitProcess, PAGE_EXECUTE_READ)
  │
  └─ POPAD → JMP OEP (0x0044E388)


[Función gancho: 0x03015C00]
  │  (llamada cuando el usuario cierra el programa)
  ├─ GetModuleHandleA("ArmAccess.dll") → FreeLibrary
  ├─ Sleep(500)                        → esperar cierre limpio
  ├─ DeleteFileA(path_ArmAccess)       → eliminar DLL del disco
  ├─ Restaurar bytes originales de ExitProcess
  ├─ LocalFree (liberar buffer)
  └─ ExitProcess(0)                    → cerrar el proceso
```

### Corrección del BaseOfCode en la cabecera PE

```
Nuevo BaseOfCode = 0x03009000 - 0x00400000 = 0x02C09000
→ editar en Olly (PE header view) en la dirección del campo BaseOfCode
→ evita el warning de Olly al abrir el ejecutable modificado
```

---

## Resultado

- ✅ Desempacado con IAT completamente reparada.
- ✅ Todas las limitaciones de la versión trial bypasseadas.
- ✅ Misterio de `ArmAccess.dll` resuelto: Armadillo installa hooks en MSVBVM60 para gestionar la nagscreen.
- ✅ `ArmAccess.dll` embebida en el propio ejecutable — sin dependencias externas.
- ✅ Injerto funcional: crea la DLL al inicio (oculta), la elimina al cerrar.
- ✅ Variable de entorno `TYPE=AAENTERPRISE` activa → versión Enterprise en el About.
- ✅ Probado en Windows XP SP3 y Windows 7. ✓

---

## Notas técnicas

- Armadillo detecta BPs en `LoadLibraryA` comprobando si el primer byte es `0xCC` → usar BP condicional a partir de la 3ª instrucción (después del `PUSH EBP`).
- Los separadores entre DLLs en la IAT son punteros tipo `0x037DDxxx` (no ceros) — Scylla los reporta como inválidos → eliminar con `Cut Thunks`.
- El doble loop de Armadillo (`0x037DD26C`–`0x037DD79A`) instala hooks en APIs del sistema sobrescribiendo sus primeros bytes con `JMP stub`.
- `VB6` no expone `GetProcAddress` en su IAT estándar — usa `msvbvm60.DllFunctionCall` como wrapper.
- Topo v1.2 tiene un límite de secciones — crear una única sección grande en lugar de dos pequeñas.
- El gancho a `ExitProcess` usa `push addr + ret` (7 bytes) para evitar un `JMP rel32` que requeriría calcular offsets relativos.

---

## Referencias

- Writeup original: Snat — CrackSLatinoS (Agosto 2015)
- Herramientas descargables en: http://www.ricardonarvaja.info/WEB/
- Archivos incluidos: `ArmAccess.dll`, `ganchos.osc` (script ODbgScript)
