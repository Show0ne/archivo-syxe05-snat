// ClS.cpp : Define el punto de entrada para la aplicación de consola.
//
#include "stdafx.h"
#include <windows.h>
#include <tchar.h>
#include <stdio.h>

#define NOMBRE_SERVICIO TEXT("ClS")

// Definimos las variables GLOBALES
bool					cls_serviceRunning;
bool					cls_servicePaused;
SERVICE_STATUS          cls_serviceStatus; 
SERVICE_STATUS_HANDLE   cls_serviceStatusHandle; 
HANDLE                  cls_serviceStopEvent = NULL;
HANDLE					cls_handle_thread;

// Se declaran los prototipos de función
void WINAPI CLS_ServiceCtrlHandler( DWORD ); 
void WINAPI CLS_ServiceMain( DWORD, LPTSTR * ); 
void CLS_InformarSCM( DWORD, DWORD, DWORD, DWORD );
DWORD CLS_ServiceThread( LPDWORD param );

//
// Función principal de la aplicación
//
int _tmain(int argc, _TCHAR* argv[])
{
	// Servicio tipo SERVICE_WIN32_OWN_PROCESS tiene un único ServiceMain().
    SERVICE_TABLE_ENTRY ServiceTableEntry[] = 
    { 
        { NOMBRE_SERVICIO, (LPSERVICE_MAIN_FUNCTION) CLS_ServiceMain }, 
        { NULL, NULL } 
    }; 

	// Registramos el ejecutable como servicio.
	if (!StartServiceCtrlDispatcher( ServiceTableEntry )) 
    { 
		printf( "Error StartServiceCtrlDispatcher 0x%08lx", GetLastError() );
    } 
	return 0;
}

//
//   Función Principal del Servicio (ServiceMain).
//
void WINAPI CLS_ServiceMain( DWORD dwArgc, LPTSTR *lpszArgv )
{
	// Registra la función de control del servicio.
	cls_serviceStatusHandle = RegisterServiceCtrlHandler( 
        NOMBRE_SERVICIO, 
        CLS_ServiceCtrlHandler);
	
    if( !cls_serviceStatusHandle )
    { 
		printf( "Error RegisterServiceCtrlHandler 0x%08lx", GetLastError() );
        return; 
    } 
	
    // Estos miembros de SERVICE_STATUS quedarán así:
	cls_serviceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS; 
    cls_serviceStatus.dwServiceSpecificExitCode = 0;    
	
	// Informamos al SCM del estado del servicio SERVICE_START_PENDING.
	CLS_InformarSCM( SERVICE_START_PENDING, NO_ERROR, 1, 1700 );
		
	// Creamos un Evento que firmará la función de control (CLS_ServiceCtrlHandler)
    // cuando éste reciba la señal de control SERVICE_CONTROL_STOP.
    cls_serviceStopEvent = CreateEvent(
	    NULL,					// atributos de seguridad por defecto.
        TRUE,					// reseteo del evento manual.
        FALSE,					// sin firmar.
        L"CLS_PararServicio");  // nombre del evento.

	// si no se pudo crear el evento abortamos
    if ( cls_serviceStopEvent == NULL)
	{
        CLS_InformarSCM( SERVICE_STOPPED, NO_ERROR, 0, 0 );
        return;
    }
	
	// Informamos al SCM de la progresión de estado del servicio.
	CLS_InformarSCM( SERVICE_START_PENDING, NO_ERROR, 2, 1800 );
	
    // Lanzamos el hilo que ejecutará el código específico del servicio.
	DWORD id;
	cls_handle_thread = CreateThread(
		0,
		0,
		(LPTHREAD_START_ROUTINE) CLS_ServiceThread,
		0,
		0,
		&id);
	
	// Informamos al SCM de que se completó la inicialización.
    CLS_InformarSCM( SERVICE_RUNNING, NO_ERROR, 0, 0 );
	cls_serviceRunning = TRUE;
	cls_servicePaused=FALSE;
	
	// Loopea hasta que el servicio termine..
	while( true )
    {
		// Esperara al evento 'cls_serviceStopEvent' indefinidamente.
        WaitForSingleObject(cls_serviceStopEvent, INFINITE);
		
		// detenemos el hilo de servicio y el propio servicio
		cls_serviceRunning = FALSE;
        CLS_InformarSCM( SERVICE_STOPPED, NO_ERROR, 0, 0 );
        return;
    }
}

//
//   Función de Control del Servicio que se registrará en la 
//	 llamada a RegisterServiceCtrlHandler().
//
void WINAPI CLS_ServiceCtrlHandler( DWORD codigoControl )
{
   // Despacha la petición de control recibida desde el SCM.
   switch( codigoControl ) 
   {  
	  case SERVICE_CONTROL_PAUSE:
		 if ( cls_serviceRunning && !cls_servicePaused )
		 {
			CLS_InformarSCM( SERVICE_PAUSE_PENDING, NO_ERROR, 1, 1300 );
			cls_servicePaused=TRUE;
			SuspendThread( cls_handle_thread );
			CLS_InformarSCM( SERVICE_PAUSED, NO_ERROR, 0, 0 );
		 }
		 break;

	  case SERVICE_CONTROL_CONTINUE:
		 if ( cls_serviceRunning && cls_servicePaused )
		 {
			CLS_InformarSCM( SERVICE_CONTINUE_PENDING, NO_ERROR, 1, 1400 );
			cls_servicePaused=FALSE;
			ResumeThread( cls_handle_thread );
			CLS_InformarSCM( SERVICE_RUNNING, NO_ERROR, 0, 0 );
		 }
		 break;

      case SERVICE_CONTROL_INTERROGATE:
		 CLS_InformarSCM( cls_serviceStatus.dwCurrentState, NO_ERROR, 0, 0 );
         break; 
 
      case SERVICE_CONTROL_STOP: 
         CLS_InformarSCM( SERVICE_STOP_PENDING, NO_ERROR, 1, 2650 );

         // Firma el evento de finalización del Servicio!
         SetEvent( cls_serviceStopEvent );
         CLS_InformarSCM(cls_serviceStatus.dwCurrentState, NO_ERROR, 1, 3675 );
         return;

	  default:
		  break;
   } 
}

//
//   Hilo de ejecución del Servicio, es su núcleo, quedará loopeando mientras no se
//	 baje la bandera cls_serviceRunning (boolean).
//
DWORD CLS_ServiceThread( LPDWORD param )
{
	while( cls_serviceRunning )
	{
			printf("El servicio está ACTIVO..\n");
			Beep( 500,500 );
			Sleep( 6000 );
	}

	printf("El servicio está INACTIVO!..\n");
	return 0;
}

//
//   Informa al SCM del estado del servicio
//
void CLS_InformarSCM( DWORD dwCurrentState,
                      DWORD dwWin32ExitCode,
					  DWORD dwCheckPoint,
                      DWORD dwWaitHint )
{
	// RELLENAMOS la estructura SERVICE_STATUS.
	cls_serviceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
	cls_serviceStatus.dwCurrentState = dwCurrentState;
    cls_serviceStatus.dwWin32ExitCode = dwWin32ExitCode;
    cls_serviceStatus.dwWaitHint = dwWaitHint;

	// Si el servicio está en estado 'pendiente de iniciación' NO aceptamos
	// ningún control por parte del SCM, esto es para prevenir un cuelgue del
	// servicio durante esta etapa, si no estamos iniciando entonces aceptamos
	// el control STOP y PAUSE_CONTINUE, es decir nuestro servicio se podrá
	// tanto detener como pausar y reanudar.
	{
        cls_serviceStatus.dwControlsAccepted = 0;
	}
    else
	{
		cls_serviceStatus.dwControlsAccepted = 
			SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_PAUSE_CONTINUE;
	}
    if ( (dwCurrentState == SERVICE_RUNNING) ||
           (dwCurrentState == SERVICE_STOPPED) )
	{
        cls_serviceStatus.dwCheckPoint = 0;
	}
     else
    {
		cls_serviceStatus.dwCheckPoint = dwCheckPoint++;
	}

	// Informamos al SCM del estado actual del servicio.
    SetServiceStatus( cls_serviceStatusHandle, &cls_serviceStatus );
}
