.386
.model flat, stdcall
option casemap :none
include DirectLoader.inc

.code

Inicio:
   
   invoke SetEnvironmentVariable,addr nombre_variable,addr valor_variable
   invoke SetEnvironmentVariable,addr nombre_variable2,addr valor_variable2
   
 sigue:
   invoke CreateFile,addr offset_nombre,GENERIC_READ,FILE_SHARE_READ,NULL,\
                     OPEN_EXISTING,FILE_ATTRIBUTE_HIDDEN,0
   inc eax
   test eax, eax
   jne existe
   

   mov existencia, FALSE
   invoke GetModuleHandle,NULL
   mov manejador_proceso, eax
   
   invoke FindResource,manejador_proceso,DUMPEADO,RT_RCDATA
   mov manejador_recurso, eax
   
   INVOKE SizeofResource, manejador_proceso, eax
   mov tamano_recurso, eax
   
   INVOKE LoadResource, manejador_proceso,  manejador_recurso
   mov direc_recurso, eax
   
   invoke CreateFile,addr offset_nombre,GENERIC_WRITE,FILE_SHARE_WRITE+FILE_SHARE_DELETE,NULL,\
                     CREATE_ALWAYS,FILE_ATTRIBUTE_HIDDEN,0
   mov manejador_archivo, eax
   invoke WriteFile,eax,direc_recurso,tamano_recurso,addr bytes_escritos,NULL
   invoke CloseHandle,manejador_archivo
   
 existe:
   invoke CreateProcess,addr offset_nombre,NULL,NULL,NULL,NULL,NULL,NULL,NULL,\
						addr StartupInfo,addr ProcessInformation
   test    eax,eax
   jz     Problema_CreateProcess
    
   invoke WaitForSingleObject,ProcessInformation.hProcess, INFINITE
    
   cmp existencia, TRUE
   je Salida
    
   invoke CloseHandle,ProcessInformation.hProcess
   invoke Sleep,5000
   invoke DeleteFile,addr offset_nombre
   jmp Salida
    
 Problema_CreateProcess:
   invoke MessageBoxA,NULL,offset error_cProcess,offset Titulo,NULL
   jmp Salida
   
 Problema_ExeNoEncontrado:
   invoke MessageBoxA,NULL,offset error_exe,offset Titulo,NULL
   jmp Salida
 
 Salida:
   invoke GetLastError
   invoke ExitProcess,eax

END Inicio