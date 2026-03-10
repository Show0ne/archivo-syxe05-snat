# 612 — DVD Region+CSS Free 5.9.6.8 — ASProtect 1.2x–1.3x (2ª parte: Registro)

| Campo            | Detalle                                                        |
|------------------|----------------------------------------------------------------|
| **Programa**     | DVD Region+CSS Free 5.9.6.8 (`tute_.exe` — ya desempacado)    |
| **Protección**   | ASProtect 1.2x – 1.3x [Registered] + Nagscreen + Trial 30 días |
| **Objetivos**    | Registrarnos por el jeto, jeje..                               |
| **Dificultad**   | Súper fácil!                                                   |
| **Herramientas** | OllyDbg v1.10, PEiD 0.94, PEditor v1.7                        |
| **Autor**        | SyXe'05 — [hAcK-c0d3d] — [CracksLatinoS]                      |
| **Fecha**        | 26-01-2006                                                     |
| **URL**          | http://www.dvdidle.com                                         |

> **Requisito previo:** haber completado la 1ª parte (`611`) y trabajar sobre
> el ejecutable ya desempacado `tute_.exe`.

---

## Contexto

El desempacado de la parte 1 dejó el archivo `tute_.exe` limpio de ASProtect.
PEiD lo identifica como **Microsoft Visual C++ 6.0** — importante saberlo ya
que cada compilador tiene sus propias estructuras internas.

Las restricciones que quedan son exclusivamente del programa:

- **Nagscreen** de bienvenida con contador de días Trial.
- **Trial de 30 días**.

El vector de ataque no será el serial (el programa lo valida al arrancar desde
registro o archivo) sino localizar directamente dónde lee el nombre de usuario.

---

## Localización de la nagscreen

Se carga `tute_.exe` en OllyDbg y se pulsa **F9** hasta que aparece la nag.
Se pausa Olly con **F12** y se examina el stack.

En la pila aparecen dos llamadas sospechosas:

```
RETURN to tute_.00406A85 from tute_.0040F300
RETURN to tute_.00404148 from <JMP.&mfc42.#2514>
```

Se hace doble clic sobre cada una para ir a su código y se colocan **BPs** en
ambas direcciones (`00406A85` y `00404148`).

Se pulsa F9 y se hace clic en **"Evaluación gratuita"**. Olly para en
`00404148`. En los registros se observa **EAX==0**, que indica al programa qué
botón se pulsó.

Se pulsa **Ctrl+F9** para llegar al siguiente RETN y se supera para caer en:

```asm
00403593  8BC8          MOV ECX, EAX
00403695  E8 7BFBFFFF   CALL tute_.00403215    ; ojo a este call
0040369A  85C0          TEST EAX, EAX
0040369C  75 20         JNZ SHORT tute_.004036BE  ; bonito salto ;-)
...
004036AF  391D E005420  CMP DWORD PTR DS:[4205E0], EBX
004036B5  74 07         JE SHORT tute_.004036BE
004036B7  33F6          XOR ESI, ESI
...
004036AA  ...                                   ; aquí se llama a la nag
```

El `TEST EAX, EAX` seguido del `JNZ` es delator: si EAX fuera `1` se saltaría
la nag. El CALL en `00403215` decide ese valor.

---

## Análisis del CALL de protección (`00403215`)

Se coloca un **BP en `00403215`**, se reinicia y se entra con **F7**.

La rutina es muy pequeña:

```asm
00403215  E8 E6DDFFFF   CALL tute_.00401000
0040321A  05 04010000   ADD EAX, 104
0040321F  74 0F         JE SHORT tute_.00403230
00403221  50            PUSH EAX
00403222  E8 891B0100   CALL <JMP.&msvcrt.strlen>  ; strlen
00403227  85C0          TEST EAX, EAX
00403229  59            POP ECX
0040322A  76 04         JBE SHORT tute_.00403230
0040322C  33C0          XOR EAX, EAX
0040322E  40            INC EAX
0040322F  C3            RETN
00403230  33C0          XOR EAX, EAX
00403232  C3            RETN
```

El primer CALL (`00401000`) simplemente coloca `4233E0` en EAX y retorna:

```asm
00401000  B8 E0334200   MOV EAX, tute_.004233E0
00401005  C3            RETN
```

Después se le suma `104` → EAX apunta a `004234E4`. Se llama a `strlen` con
esa dirección como parámetro. Si la cadena en `[4234E4]` tiene longitud > 0,
EAX retorna `1` (registrado). Si está vacía, EAX retorna `0` (trial).

### La clave

Se hace **"Follow in dump → Memory Address"** sobre EAX (`004234E4`) y se
comprueba que está completamente vacío (todo ceros).

Se escribe un nombre directamente en esa dirección desde la ventana dump:

```
004234E4: 53 79 58 65 27 30 35  →  "SyXe'05"
```

Se pulsa **F9** — el programa arranca **sin la nag** y completamente registrado.
Confirmación en el About:

```
DVD Region+CSS Free 5.9.6.8 - Registrado a: SyXe'05
Derechos Reservados (C) 2001 - 2004 Fengtao Software Inc.
```

La protección se basaba enteramente en ASProtect — sin él no hay nada 😄

---

## Creación del parche (injerto de código)

Para que el registro sea permanente se inyecta código que escribe el nombre
en `[4234E4]` antes de que el programa lo lea.

### Zona libre para el injerto

Se localiza una zona de ceros en `00417EB0` y se ensamblan las siguientes
instrucciones:

```asm
00417EB0  C705 E4344200 65587953  MOV DWORD PTR DS:[4234E4], 53795865  ; "SyXe"
00417EBA  C705 E8344200 35302765  MOV DWORD PTR DS:[4234E8], 65273035  ; "'05"
00417EC4  68 464E4100             PUSH tute_.<ModuleEntryPoint>
00417EC9  C3                      RETN
```

El injerto escribe el nombre en `[4234E4]`, luego hace `PUSH` del EP original
(`00414E46`) y `RETN` para transferir el control al OEP normal.

### Aplicar el parche

1. Seleccionar los bytes modificados → **"Copy to executable → Selection"** →
   **"Save file"** → guardar como `tute_crk.exe`.

### Cambiar el EntryPoint con PEditor v1.7

Para que el injerto se ejecute al arrancar hay que apuntar el EP al injerto:

| Campo        | Valor original | Valor nuevo |
|--------------|---------------|-------------|
| Entry Point  | `00014E46`    | `00017EB0`  |
| Image Base   | `00400000`    | `00400000`  |

Se abre `tute_crk.exe` en PEditor, se cambia el EP a `00017EB0` y se guardan
los cambios.

---

## Resultado

Al ejecutar `tute_crk.exe` directamente:

- ✅ **Nag eliminada** — el programa arranca directamente sin ventana de trial.
- ✅ **Registrado** — el About muestra el nombre de usuario correcto.
- ✅ **Trial eliminado** — sin contador de días.
- ✅ Todas las funciones operan correctamente.

---

## Notas

- La protección real residía íntegramente en ASProtect — una vez desempacado
  el programa no tenía ninguna verificación adicional robusta.
- Técnica utilizada: **injerto de código** + modificación del EP con PEditor.
  Buena práctica introductoria para aprender a hacer patches permanentes.

---

## Referencias

- Writeup original: SyXe'05 — CracksLatinoS (26-01-2006)
- Parte 1 (desempacado): writeup `611-asprotect-1.2x-1.3x-dvd-region-css-free`
- Herramientas: OllyDbg 1.10, PEiD 0.94, PEditor v1.7
- Contacto original del autor: syxe00@yahoo.es / syxe05@gmail.com
