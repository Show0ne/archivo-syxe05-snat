# 742 — Magic Utilities 2006 v4.22 — PECompact 2.x

| Campo            | Detalle                                                        |
|------------------|----------------------------------------------------------------|
| **Programa**     | Magic Utilities 2006 v4.22 (`mgutil.exe`)                      |
| **Protección**   | PECompact 2.x + Nagscreen + Trial x días                       |
| **Objetivos**    | Desempacar y evitar las limitaciones                           |
| **Dificultad**   | Bastante sencilla                                              |
| **Herramientas** | OllyDbg v1.10, PEiD v0.92, ImpREC v1.6                        |
| **Autor**        | SyXe'05 — [hAcK-c0d3d] — [CracksLatinoS]                      |
| **Fecha**        | 17-02-2006                                                     |
| **URL**          | http://www.magictweak.com                                      |

---

## Identificación del packer

PEiD identifica el ejecutable `mgutil.exe` como empacado con **PECompact 2.x → Jeremy Collake**.

PECompact es un compresor puro: no modifica el EP (sin *stolen bytes*) ni redirige la IAT (la deja intacta). Su particularidad es que levanta una excepción SEH personalizada nada más arrancar para comenzar el proceso de descompresión.

Se abre OllyDbg con el plugin **IsDebuggerPresent** activo (parchea `[7FFDF002]` / `[EBX+2]` en WinXP). Se carga `mgutil.exe` y Olly para en el EP:

```asm
0045C168  B8 D4F85600   MOV EAX, mgutil.0056F8D4
0045C16E  50            PUSH EAX
0045C16F  64:FF35 00000 PUSH DWORD PTR FS:[0]
0045C176  64:8925 00000 MOV DWORD PTR FS:[0], ESP
0045C17D  33C0          XOR EAX, EAX
0045C17F  8908          MOV DWORD PTR DS:[EAX], ECX   ; ← Cuidado aquí!!
```

Las cuatro primeras instrucciones instalan un manejador SEH en `0056F8D4` y a continuación levantan una excepción intencionada en `0045C17F`.

---

## Análisis del SEH del packer

Se pone BP en el SEH (`0056F8D4`) antes de dejar que se genere la excepción. El handler no examina el tipo de excepción — simplemente **inserta un JMP** justo después del EP y reajusta el puntero:

```asm
0056F8D4  B8 7DE8CCAFF  MOV EAX, FFCAE87D
0056F8D9  8D88 7A108C00 LEA ECX, DWORD PTR DS:[EAX+8C107A]
0056F8DF  8941 01       MOV DWORD PTR DS:[ECX+1], EAX
...
0056F8EC  83C2 05       ADD EDX, 5
0056F8EF  2BCA          SUB ECX, EDX
0056F8F1  894A FC       MOV DWORD PTR DS:[EDX-4], ECX   ; ← Y lo reajusta
0056F8F4  33C0          XOR EAX, EAX
0056F8F6  C3            RETN
```

Tras el RETN se comprueba que efectivamente insertó un `JMP 0056F8F7` justo después del EP. Se retorna al módulo `ntdll`.

---

## Llegando al código del packer

Para evitar tracear hasta `ntdll.ZwContinue` se pone un **BPM on Memory Access** en la sección `.text` de `mgutil` (`00401000`). Se pulsa F9 y Olly para directamente en el JMP insertado:

```asm
0045C17F  E9 73371100   JMP mgutil.0056F8F7
```

Se intenta seguir el salto con F7 y Olly lanza un error:

> *"Debugged program set single step flag (bit T in EFL)..."*

El packer activó el **Trap Flag** (T=1) para impedir el trazado. Se desactiva haciendo doble clic sobre el flag T en el panel de registros (T=0) y se pulsa F7. Se cae en el stub del packer:

```asm
0056F8F7  B8 7DE8CCAFF  MOV EAX, FFCAE87D
0056F8FC  64:8FB5 00000 POP DWORD PTR FS:[0]
0056F903  83C4 04       ADD ESP, 4
0056F906  55            PUSH EBP
0056F907  53            PUSH EBX
0056F908  51            PUSH ECX
0056F909  57            PUSH EDI
0056F90A  56            PUSH ESI
...
0056F929  FFD0          CALL EAX              ; → VirtualAlloc
```

---

## Descompresión y localización del OEP

`CALL EAX` llama a **VirtualAlloc** — reserva el bloque `00DD0000` donde se descomprimirá el código original. Dentro de esa rutina se hace otra llamada a VirtualAlloc para el bloque `00DE0000`, que se libera al terminar.

Al salir del CALL, EAX apunta al OEP real. Aunque Olly muestra `<ModuleEntryPoint>`, en `0045C169` está el verdadero OEP descomprimido — el packer sobrescribió su propio stub con el código original:

```asm
0045C169  55            PUSH EBP
0045C16A  8BEC          MOV EBP, ESP
0045C16C  6A FF         PUSH -1
0045C16E  68 B8434900   PUSH mgutil.004943B8
0045C173  68 48254600   PUSH mgutil.00462548
0045C178  64:A1 0000000 MOV EAX, DWORD PTR FS:[0]
0045C17F  50            PUSH EAX
...
0045C18F  FF15 B0D24800 CALL DWORD PTR DS:[48D2B0]    ; kernel32.GetVersion
```

Un poco más adelante, `CALL DWORD PTR [ECX]` libera la sección `00DD0000` con **VirtualFree** y se produce el salto definitivo al OEP.

---

## Dump y reparación de la IAT

Estando en el OEP se dumpea con **OllyDump** → `tute.exe` (opciones por defecto).

Se abre **ImpREC**, se attachea el proceso `mgutil.exe`:

| Campo     | Valor   |
|-----------|---------|
| OEP (RVA) | `5C169` |

Se pulsa **IAT AutoSearch** → **Get Imports**. Todas las entradas aparecen correctas. Se pulsa **Fix Dump** → ImpREC genera `tute_.exe`:

```
Fixing a dumped file...
10 (decimal:16) module(s)
1CA (decimal:458) imported function(s).
*** New section added successfully. RVA:00201000 SIZE:00003000
Image Import Descriptor size: 140; Total length: 20DE
C:\Archivos de programa\Mgutil 2006 4.22\tute_.exe saved successfully.
```

`tute_.exe` arranca correctamente — **PECompact eliminado**.

---

## Superando las limitaciones

Se abre `tute_.exe` en Olly. Aparece la **NagScreen de registro** con campos Nombre y Código. Se introducen datos de prueba (`SyXe'05` / `121212`) y se pulsa Registro — el programa pide reiniciar.

### Localización de los datos de registro

Se buscan strings y se detecta la referencia a `mgutil_reg.ini`. Se ponen BP en las APIs de lectura de `.ini`:

```
bp GetPrivateProfileStringA
bp GetPrivateProfileIntA
```

En el directorio de instalación se encuentran dos archivos `.ini`:

- `mgutil_reg.ini` — configuración general (lenguaje, skin)
- `mgutil_win.ini` — **datos de registro**

Contenido de `mgutil_win.ini` tras el primer intento:

```ini
[REG]
Times=4
1=1140162652
2=1140162876
3=1140163275
4=1140163375
UserName=SyXe'05
RegCode=121212
```

### Rutina de validación

Con los BPs activos, Olly para primero en la lectura de `UserName` (buffer `00127A08`) y después en `RegCode` (buffer `00127968`). Con `Ctrl+F9` se retorna a la zona de código que llama a las APIs:

```asm
00421496  68 04ACED4A00  PUSH 004ACED4             ; "UserName"
0042149B  68 906A4A00    PUSH 004A6A90             ; "REG"
004214A0  C68424 74860A0 MOV BYTE PTR [ESP+8674],0F
004214A8  FFD7           CALL EDI                  ; GetPrivateProfileStringA
...
004214BB  68 04ACED4A00  PUSH 004ACED4             ; "RegCode"
004214C0  68 906A4A00    PUSH 004A6A90             ; "REG"
004214C5  FFD7           CALL EDI                  ; GetPrivateProfileStringA
```

Poco después se pasan nombre y serial al CALL `004229C0`:

```asm
004214F9  8D8C24 54010   LEA ECX, DWORD PTR [ESP+154]
00421500  50             PUSH EAX           ; Arg2 = 00127968 "121212"
00421501  51             PUSH ECX           ; Arg1 = 00127A08 "SyXe'05"
00421503  8BCD           MOV ECX, EBP
00421504  E8 B7140000    CALL 004229C0
00421509  85C0           TEST EAX, EAX
0042150B  74 0F          JE SHORT 0042151C
```

### Algoritmo de generación del serial

Dentro de `004229C0` hay un loop que **convierte el nombre a dígitos numéricos**. Para `SyXe'05` el resultado es `2229780` (7 dígitos). Este valor se compara con el serial introducido — pero es una **trampa**: aunque la comparación actualiza la variable global `[4ADBE4]`, este serial generado no es el válido.

### Seriales hardcoded

En la llamada siguiente (`00422D20`) el programa compara el serial contra una tabla de **seriales hardcoded** ofuscados almacenados en `004A6CD8`:

```
004A6CD8  2FCZCCB2,BZKFZG1
004A6CE8  2,ZZMEC23G,G52EE
004A6CF8  2FU,GC3M3UFF,2EZ
004A6D08  ECH2K,B4ZZZH5Z,2
004A6D18  BBUFF3M,CFGCFEFE
...
```

Hay **5 bucles** de comparación. Se prueba uno de ellos (`LXULGXKU` para el nombre `SyXe'05`) y el programa acepta el registro:

```asm
00422E8B  33C0   XOR EAX, EAX
00422E8D  JMP SHORT 00422E94   ; serial VÁLIDO ;)
```

Tras reiniciar el programa arranca **sin nagscreen** y el About muestra:

> *Esta copia tiene Licencia para: SyXe'05*

---

## Resultado

- ✅ **Desempacado** — PECompact 2.x eliminado, IAT reparada (458 funciones, 16 módulos).
- ✅ **Trap Flag neutralizado** — desactivado manualmente en el panel de registros.
- ✅ **Registrado** — serial hardcoded localizado, nagscreen y Trial eliminados.

---

## Notas técnicas

- PECompact 2.x no roba bytes del EP ni redirige la IAT — el dump con OllyDump es directo y la reparación con ImpREC no requiere ajustes manuales.
- El algoritmo de generación de serial (nombre → dígitos numéricos) es un **señuelo**: el programa no lo valida realmente, sino que compara contra una tabla de ~50 seriales hardcoded ofuscados en la sección de datos.
- El contador de arranques (`Times=N`) en `mgutil_win.ini` registra cada ejecución — la protección Trial se basa en este valor junto con timestamps UNIX.
- La variable global `[4ADBE4]` se actualiza en función del resultado del serial generado pero **no determina el estado de registro** — es otro señuelo.

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (17-02-2006)
- Herramientas: OllyDbg 1.10, PEiD 0.92, ImpREC 1.6
- Contacto original del autor: syxe05@gmail.com
