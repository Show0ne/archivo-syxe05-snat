# 1562 — Servicios de Windows

| Campo            | Detalle                                                                 |
|------------------|-------------------------------------------------------------------------|
| **Programa**     | Alchemy Eye 11.5.0 (`eyesrv.exe` + `eyecli.exe`)                       |
| **Protección**   | ASProtect 1.2x (sobre el servicio `eyesrv.exe`)                         |
| **Objetivos**    | Comprender el funcionamiento de los Servicios de Windows y practicar desempacando uno |
| **Dificultad**   | Media — requiere conocimientos previos de servicios y debugging         |
| **Herramientas** | OllyIce 1.10, ImpREC 1.7e, RDG Packer Detector v0.7.2                  |
| **Autor**        | Snat — [CracksLatinoS]                                                  |
| **Fecha**        | Julio 2015                                                              |
| **URL**          | http://www.alchemy-eyes.com                                             |

---

## Introducción

Guía práctica sobre el funcionamiento de los Servicios de Windows: construcción, ejecución, depuración y desempacado. Se programa un servicio propio en Visual C++ para practicar con él y después se aplican los conocimientos sobre un servicio comercial real (`eyesrv.exe`) protegido con ASProtect.

Sistema operativo de referencia: **Windows XP SP3 (32 bit)**. El funcionamiento en Windows 7 es similar.

---

## 1. Descripción — ¿Qué es un servicio?

Un servicio es un programa que corre en **segundo plano** (background), normalmente invisible para el usuario, que puede ejecutarse incluso cuando **no hay ninguna sesión de usuario iniciada**. El SCM (*Service Control Manager* / Administrador de Control de Servicios) es el responsable de iniciarlo, pausarlo, reanudarlo y detenerlo.

La base de datos del SCM se almacena en el registro bajo:

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services
```

---

## 2. Ejecución de un servicio — APIs principales

### `StartServiceCtrlDispatcher`

Primera llamada obligatoria desde `main()`. Conecta el hilo principal del proceso con el SCM a través de una *named pipe*:

```
\Pipe\Net\NtControlPipeX
```

donde `X` se incrementa según el contador en:

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\ServiceCurrent
```

Recibe un puntero a un array de estructuras `SERVICE_TABLE_ENTRY` (una por servicio). No retorna hasta que todos los servicios hayan finalizado.

### `ServiceMain`

Entry Point del servicio. Se ejecuta en un nuevo hilo creado por `StartServiceCtrlDispatcher` al recibir la señal `SERVICE_START`. Sus responsabilidades:

- Llamar a `RegisterServiceCtrlHandler` para registrar la función de control.
- Informar al SCM del progreso de inicialización vía `SetServiceStatus` con estado `SERVICE_START_PENDING`.
- Lanzar el hilo que ejecutará el código específico del servicio.
- Actualizar el estado a `SERVICE_RUNNING`.
- Quedar bloqueada en `WaitForSingleObject(INFINITE)` hasta recibir la señal de parada.

### `RegisterServiceCtrlHandler`

Registra la función de control (`ControlHandler`) y retorna el `SERVICE_STATUS_HANDLE` necesario para las llamadas posteriores a `SetServiceStatus`.

### `SetServiceStatus`

Informa al SCM del estado actual. Utiliza la estructura `SERVICE_STATUS` con los campos:

| Campo                  | Descripción |
|------------------------|-------------|
| `dwServiceType`        | Tipo: `SERVICE_WIN32_OWN_PROCESS`, `SERVICE_WIN32_SHARE_PROCESS`, etc. |
| `dwCurrentState`       | Estado actual: `SERVICE_RUNNING`, `SERVICE_STOPPED`, `SERVICE_PAUSED`... |
| `dwControlsAccepted`   | Controles aceptados: `SERVICE_ACCEPT_STOP`, `SERVICE_ACCEPT_PAUSE_CONTINUE` |
| `dwWin32ExitCode`      | Código de error Win32 |
| `dwCheckPoint`         | Contador de progreso (incrementar en fases PENDING) |
| `dwWaitHint`           | Tiempo estimado en ms para llegar a la siguiente marca |

> ⚠️ Entre llamadas consecutivas con estado PENDING el tiempo transcurrido no debe superar el valor de `dwWaitHint` o el SCM considerará que el servicio falló y lo detendrá.

### Diagrama de flujo resumido

```
main()
  └─ StartServiceCtrlDispatcher()
        └─ [SCM envía SERVICE_START]
              └─ nuevo hilo → ServiceMain()
                    ├─ RegisterServiceCtrlHandler()  → SERVICE_STATUS_HANDLE
                    ├─ SetServiceStatus(START_PENDING)
                    ├─ CreateEvent(cls_serviceStopEvent)
                    ├─ CreateThread → ServiceThread (loop principal)
                    ├─ SetServiceStatus(RUNNING)
                    └─ WaitForSingleObject(cls_serviceStopEvent, INFINITE)
                          └─ [SCM envía SERVICE_CONTROL_STOP]
                                └─ ControlHandler → SetEvent → SERVICE_STOPPED
```

---

## 3. Programación del servicio (Visual C++)

Se crea un proyecto **Win32 Console Application** en Visual Studio 2010 con nombre `ClS`. Subsistema: `/SUBSYSTEM:CONSOLE`.

### `main()`

```cpp
int _tmain(int argc, _TCHAR* argv[])
{
    SERVICE_TABLE_ENTRY serviceTable[] = {
        { SERVICE_NAME, (LPSERVICE_MAIN_FUNCTION)CLS_ServiceMain },
        { NULL, NULL }
    };
    StartServiceCtrlDispatcher(serviceTable);
    return 0;
}
```

### `CLS_ServiceMain()`

```cpp
void WINAPI CLS_ServiceMain(DWORD dwArgc, LPTSTR *lpszArgv)
{
    cls_serviceStatusHandle = RegisterServiceCtrlHandler(
        SERVICE_NAME, CLS_ServiceCtrlHandler);
    if (!cls_serviceStatusHandle) return;

    CLS_InformarSCM(SERVICE_START_PENDING, NO_ERROR, 1, 1700);

    cls_serviceStopEvent = CreateEvent(NULL, TRUE, FALSE, "CLS_PararServicio");
    if (!cls_serviceStopEvent) {
        CLS_InformarSCM(SERVICE_STOPPED, NO_ERROR, 0, 0);
        return;
    }

    CLS_InformarSCM(SERVICE_START_PENDING, NO_ERROR, 2, 1800);

    cls_serviceRunning = TRUE;
    cls_servicePaused  = FALSE;
    cls_handle_thread  = (HANDLE)_beginthreadex(
        NULL, 0, (unsigned(__stdcall*)(void*))CLS_ServiceThread, NULL, 0, NULL);

    CLS_InformarSCM(SERVICE_RUNNING, NO_ERROR, 0, 0);

    while (true) {
        WaitForSingleObject(cls_serviceStopEvent, INFINITE);
        cls_serviceRunning = FALSE;
        CLS_InformarSCM(SERVICE_STOPPED, NO_ERROR, 0, 0);
        return;
    }
}
```

### `CLS_ServiceCtrlHandler()`

```cpp
void WINAPI CLS_ServiceCtrlHandler(DWORD codigoControl)
{
    switch (codigoControl) {
        case SERVICE_CONTROL_PAUSE:
            if (cls_serviceRunning && !cls_servicePaused) {
                CLS_InformarSCM(SERVICE_PAUSE_PENDING, NO_ERROR, 1, 1300);
                cls_servicePaused = TRUE;
                SuspendThread(cls_handle_thread);
                CLS_InformarSCM(SERVICE_PAUSED, NO_ERROR, 0, 0);
            }
            break;
        case SERVICE_CONTROL_CONTINUE:
            if (cls_serviceRunning && cls_servicePaused) {
                CLS_InformarSCM(SERVICE_CONTINUE_PENDING, NO_ERROR, 1, 1400);
                cls_servicePaused = FALSE;
                ResumeThread(cls_handle_thread);
                CLS_InformarSCM(SERVICE_RUNNING, NO_ERROR, 0, 0);
            }
            break;
        case SERVICE_CONTROL_INTERROGATE:
            CLS_InformarSCM(cls_serviceStatus.dwCurrentState, NO_ERROR, 0, 0);
            break;
        case SERVICE_CONTROL_STOP:
            CLS_InformarSCM(SERVICE_STOP_PENDING, NO_ERROR, 1, 2650);
            SetEvent(cls_serviceStopEvent);
            CLS_InformarSCM(cls_serviceStatus.dwCurrentState, NO_ERROR, 1, 3675);
            return;
        default:
            break;
    }
}
```

### `CLS_ServiceThread()`

```cpp
DWORD CLS_ServiceThread(LPDWORD param)
{
    while (cls_serviceRunning) {
        printf("El servicio está ACTIVO..\n");
        Beep(500, 500);
        Sleep(6000);
    }
    printf("El servicio está INACTIVO!..\n");
    return 0;
}
```

### `CLS_InformarSCM()`

```cpp
void CLS_InformarSCM(DWORD dwCurrentState, DWORD dwWin32ExitCode,
                     DWORD dwCheckPoint, DWORD dwWaitHint)
{
    cls_serviceStatus.dwServiceType    = SERVICE_WIN32_OWN_PROCESS;
    cls_serviceStatus.dwCurrentState   = dwCurrentState;
    cls_serviceStatus.dwWin32ExitCode  = dwWin32ExitCode;
    cls_serviceStatus.dwWaitHint       = dwWaitHint;

    cls_serviceStatus.dwControlsAccepted =
        (dwCurrentState == SERVICE_START_PENDING) ? 0
        : SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_PAUSE_CONTINUE;

    cls_serviceStatus.dwCheckPoint =
        ((dwCurrentState == SERVICE_RUNNING) ||
         (dwCurrentState == SERVICE_STOPPED)) ? 0 : dwCheckPoint++;

    SetServiceStatus(cls_serviceStatusHandle, &cls_serviceStatus);
}
```

---

## 4. Instalación del servicio

```bat
sc create ClS binPath= "C:\ruta\ClS.exe" DisplayName= "ClS Service"
sc start ClS
sc query ClS
sc stop ClS
sc delete ClS
```

El registro del servicio queda en:

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\ClS
```

Campos relevantes: `ImagePath`, `DisplayName`, `Start`, `Type`, `ObjectName`.

---

## 5. Depuración del servicio con OllyDbg

### Método 1 — Attach al proceso en ejecución

1. Iniciar el servicio: `sc start ClS`
2. En Olly: `File → Attach` → seleccionar el proceso `ClS.exe`
3. Olly para en `DbgBreakPoint` — pulsar F9 para dejarlo correr.

### Método 2 — INT3 en el Entry Point

Modificar el primer byte del EP (`0x55` = `PUSH EBP`) por `0xCC` (INT3) directamente en el ejecutable. Al iniciarse el servicio Olly se abrirá automáticamente. Restaurar el byte original antes de continuar.

### Interceptando señales de control

Las señales viajan desde el SCM al servicio a través de la pipe `\Pipe\Net\NtControlPipeX`. Dentro de `ADVAPI32.dll.StartServiceCtrlDispatcher`, la función queda bloqueada en `ReadFile` sobre esta pipe esperando señales. La señal llega en EAX en la dirección `0x77DC349E` (WinXP).

Para interceptar y modificar un control de parada (`1`) por uno de pausa (`2`):

1. Colocar BP en `0x77DC349E`.
2. Enviar señal de parada: `sc stop ClS`.
3. Olly para — EAX = `0x00000001` (STOP).
4. Cambiar EAX a `0x00000002` (PAUSE) y pulsar F9.
5. El servicio recibe la señal de pausa en lugar de parada.

Tabla de códigos de control:

| Código | Constante                    |
|--------|------------------------------|
| `1`    | `SERVICE_CONTROL_STOP`       |
| `2`    | `SERVICE_CONTROL_PAUSE`      |
| `3`    | `SERVICE_CONTROL_CONTINUE`   |
| `4`    | `SERVICE_CONTROL_INTERROGATE`|

---

## 6. Notas del SCM

El SCM (`services.exe`) reside en `%SYSTEMROOT%\system32\` y no puede detenerse directamente. Adjuntar el proceso a un debugger y cerrar el debugger fuerza su terminación, lo que desencadena un reinicio automático del sistema. Para cancelarlo:

```bat
shutdown /a
```

Una vez muerto el SCM cualquier operación que dependa de él queda inutilizada hasta el reinicio.

---

## 7. Práctica — Desempacando Alchemy Eye 11.5.0

### Descripción del objetivo

**Alchemy Eye** es un software de monitorización de red compuesto por dos ejecutables:

- `eyesrv.exe` — el servidor, corre como **servicio de Windows**, protegido con **ASProtect 1.2x**.
- `eyecli.exe` — el cliente gráfico que conecta con el servidor vía **sockets TCP** en el puerto **1081**.

El servidor es el que gestiona el estado de registro (`UNREGISTERED` / `DEBUG VERSION`).

### 7.1 Localización del OEP

Se carga `eyesrv.exe` en OllyIce con **todas las excepciones activadas**. Se pulsa F9 y se van superando con Shift+F9 anotando la última excepción producida: `0x00CB00E1`.

Se reinicia Olly (`Ctrl+F2`) y se modifica la configuración para parar solo en esa excepción. Al llegar a la última, se coloca un **BPM on Access** en la primera sección de código del ejecutable (Memory Map). Se supera con Shift+F9 y Olly aterriza en el OEP:

```
OEP: 0x0051A3F5
```

Sin Stolen Bytes. Se localiza la IAT siguiendo cualquier `CALL DWORD PTR [ptr_iat]`:

| Dato         | Valor       |
|--------------|-------------|
| Inicio IAT   | `0x0053200` |
| Final IAT    | `0x00532E40`|
| Longitud IAT | `0x0E40`    |

### 7.2 Localización y nopeado del CALL mágico

Se toma una entrada mala de la IAT (valor `0x00CC4E30`) y se coloca un **BPM on Write** en esa dirección. Se deshabilitan todas las excepciones y se pulsa F9. Olly para en la rutina de relleno de IAT del packer.

El packer anula los HBPs en sus manejadores de excepción, así que no se puede poner un HBP directamente en el CALL. Solución: esperar a que el packer reserve la zona `0x00CA0000` con `VirtualAlloc` y poner allí un **BP condicional en el RET** de VirtualAlloc:

```
Condición: EAX == 0x00CA0000
```

Cuando para, la zona está vacía. Se coloca un **BPM on Write** sobre la dirección del CALL dentro del loop y se espera a que se escriban sus bytes. Una vez escrito, se quita el BPM y se coloca un **BP normal** (F2) sobre el CALL:

```
CALL mágico: 0x00CAFC7A
POPAD (fin del loop): 0x00CAFC82
```

Se nopea el CALL mágico y se pone BP en el POPAD. Se pulsa F9 — Olly para en el POPAD. Se restaura el CALL nopeado con **Undo Selection** (`Ctrl+Z`).

### 7.3 Llegando al OEP y dumpeando

Con la IAT reparada se navega al OEP (`Ctrl+G` → `0x0051A3F5`) y se coloca un **BPM on Access**. Se pulsa F9 y tras dos o tres paradas por escritura Olly aterriza en el OEP.

Se dumpea con **OllyDump**:
- **Desmarcar** `Rebuild Import`.
- Pulsar `Get EIP as OEP`.
- Guardar como `eyesrv_dump.exe`.

### 7.4 Reparación de la IAT con ImpREC 1.7e

Se abre ImpREC y se attachea `eyesrv.exe` (el proceso original empacado):

| Campo | Valor        |
|-------|--------------|
| OEP   | `0x001A3F5`  |
| RVA   | `0x00132000` |
| Size  | `0x00000E40` |

`IAT AutoSearch` encuentra los valores correctamente. `Get Imports` deja **6 entradas sin resolver** — son APIs que el packer introdujo en la IAT antes de llegar a la rutina interceptada. Se resuelven manualmente o con el plugin `ASProtect 1.2 Emul API #2`.

Se guarda la tabla con **Save Tree** → `iat.txt`. Se aplica **Fix Dump** sobre `eyesrv_dump.exe` → genera `eyesrv_dump_.exe`.

### 7.5 Probando el dumpeado

```bat
sc stop eye
ren eyesrv.exe eyesrv_org.exe
ren eyesrv_dump_.exe eyesrv.exe
sc start eye
sc query eye
```

El servicio inicia correctamente. El cliente `eyecli.exe` conecta y funciona — en el About aparece `DEBUG VERSION` (cadena gestionada por el servidor).

---

## 8. Comunicación cliente-servidor — IPC vía Sockets

### 8.1 Descubrimiento

Al modificar la cadena `DEBUG VERSION` directamente en el cliente, el About sigue mostrando la original — el servidor tiene la voz cantante. La comunicación no usa named pipes (`CreateNamedPipe` no para), sino **sockets TCP**.

### 8.2 Secuencia de inicialización del socket en `eyesrv.exe`

El servidor crea el socket en la función `0x00450544`:

```cpp
// socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
af       = AF_INET       // 0x00000002 — IPv4
type     = SOCK_STREAM   // 0x00000001 — TCP full-duplex
protocol = IPPROTO_TCP
// Retorna: handle del socket → visible en la ventana de manejadores como '\Device\Afd'
```

A continuación llama a `bind` en `0x00409275` asociando el socket al puerto **1081**:

```
sockaddr_in.sin_family = AF_INET  (0x0002)
sockaddr_in.sin_port   = 0x0439   (= 1081 decimal, big-endian)
sockaddr_in.sin_addr   = 0.0.0.0  (todas las interfaces)
```

Después llama a `listen` para poner el socket a la escucha y crea dos hilos (`_beginthreadex`) cuyos Entry Points son `0x004503B6` y `0x0048C03F`. El primero gestiona las conexiones entrantes mediante `accept`, bloqueándose en esa llamada hasta que conecta un cliente.

### 8.3 Interceptando sockets

Se puede interceptar cualquier dato enviado/recibido colocando un BP en las llamadas a `wsock32.send` / `wsock32.recv` dentro de los hilos del servidor. La señal de control modifica el comportamiento del cliente en tiempo real.

### 8.4 Diagrama de flujo (Sockets)

```
eyesrv.exe (servicio)
  ├─ socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)   → handle socket
  ├─ bind(socket, 0.0.0.0:1081)
  ├─ listen(socket, backlog)
  └─ hilo 1: accept(socket) ← bloqueado esperando cliente
       └─ [eyecli.exe conecta]
             ├─ recv / send  ← intercambio de datos
             └─ estado registro / configuración monitores
```

---

## Resultado

- ✅ **Servicio propio** programado en Visual C++ (ClS) con todas las funciones SCM implementadas.
- ✅ **Depuración** de servicios con OllyDbg mediante attach y método INT3.
- ✅ **Interceptación de señales de control** SCM vía pipe `\Pipe\Net\NtControlPipeX`.
- ✅ **Desempacado** de `eyesrv.exe` (ASProtect 1.2x) con IAT reparada.
- ✅ **Comunicación IPC** via sockets TCP puerto 1081 descubierta y trazada.

---

## Notas técnicas

- El SCM no tolera que `StartServiceCtrlDispatcher` tarde más de 30 segundos en ejecutarse (tipo `SERVICE_WIN32_OWN_PROCESS`) — superado ese tiempo el SCM descarga el proceso automáticamente.
- El campo `dwWaitHint` en `SERVICE_STATUS` es crítico: entre dos llamadas consecutivas con estado `PENDING` no pueden pasar más milisegundos de los indicados en ese campo.
- El packer de `eyesrv.exe` anula los HBPs mediante sus manejadores de excepción — hay que esperar a que el bloque del packer sea asignado por `VirtualAlloc` y usar BPs normales en lugar de hardware.
- El servidor gestiona el estado de registro y lo envía al cliente por socket — parchear solo el cliente no tiene efecto.

---

## Referencias

- Writeup original: Snat — CracksLatinoS (Julio 2015)
- Tutoriales relacionados: `875-Servicio de Windows con Armadillo 3.xx by azegc`, `1287-Debugging a Windows service startup with Olly by Saccopharynx`
- MSDN: `StartServiceCtrlDispatcher`, `ServiceMain`, `RegisterServiceCtrlHandler`, `SetServiceStatus`
- Herramientas: OllyIce 1.10, ImpREC 1.7e, RDG Packer Detector v0.7.2, Visual Studio 2010
- Contacto original del autor: CracksLatinoS
