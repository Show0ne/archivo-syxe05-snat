@echo off
SetLocal
cls

if ""%1"" == """" goto ErrorParams
set filename="%1"
if ""%2"" == """" goto ErrorParams
set userName="%2"
if not ""%3"" == """" set retval=""


echo.
echo       ADMIN INTEGRATOR
echo. -------------------------
echo.
echo path found: %filename%
echo user found: %userName%
echo.
set /p "= Taking ownership of %filename%, please wait.. " < nul
takeown /F %filename%
echo ErrorLevel: %ERRORLEVEL%
set error=1
if %ERRORLEVEL% neq 0 goto Error

call :Colorize 06 OK
echo.
set /p "= Adding admin ACE's " < nul
echo .
icacls %filename% /grant %2%:(F)
set error=2
echo ErrorLevel: %ERRORLEVEL%
if %ERRORLEVEL% neq 0 goto Error

call :Colorize 06 OK
echo.
set /p "= Restoring TrustedInstaller ownership.. " < nul
echo.
icacls %filename% /setowner "NT SERVICE\TrustedInstaller"
set error=3
if %ERRORLEVEL% neq 0 goto Error

call :Colorize 06 OK
echo.&call :Colorize 06  Hecho^!

if defined retval EndLocal & set %3=0 & exit /B 0
if not defined retval EndLocal & exit /B 0

:Colorize
echo off
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
	set "DEL=%%a"
)

<nul set /p .=. > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
echo(%DEL%%DEL%%DEL%
del "%~2" >nul
goto :eof

:ErrorParams
echo Parametros incorrectos
echo  Uso:
echo      Integrator.bat ^<ruta a archivo.exe^> ^<user name^>
echo.
EndLocal
exit /B 1

:Error
if defined retval EndLocal & set %3=%error% & exit /B 0
if not defined retval EndLocal & exit /B %error%