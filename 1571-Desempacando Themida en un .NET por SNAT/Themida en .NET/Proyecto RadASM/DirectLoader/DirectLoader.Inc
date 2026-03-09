; #########################################################################

include windows.inc
include kernel32.inc
include user32.inc
include shell32.inc

includelib kernel32.lib
includelib user32.lib
includelib shell32.lib


; #########################################################################
.const
DUMPEADO           equ 5
TAMANO_BUFFER      equ 4

.data
offset_nombre      db 'DirectAccess_CLS.exe',0
error_salida       db 'Termina ejecución del Loader',0
Titulo             db 'Loader para Direct Access 2.8.0.0',0  
error_exe          db 'Ejecutable no encontrado!',0
error_cProcess     db 'Error CreateProcess!',0
nombre_variable    db 'WLRegGetStatus',0
valor_variable     db '1',0
nombre_variable2   db 'WLRegGetLicenseInfo',0
valor_variable2    db 'snat,CLS,123456-000;snat@gmail.com;2500;30000810;PowerLicense',0
manejador_archivo  dd ?
manejador_recurso  dd ?
manejador_proceso  dd ?
tamano_recurso     dd ?
direc_recurso      dd ?
buffer_variable    dd ?
bytes_escritos     dd ?
existencia         BOOL TRUE

.data?
StartupInfo 		 STARTUPINFO <>
ProcessInformation PROCESS_INFORMATION <>

