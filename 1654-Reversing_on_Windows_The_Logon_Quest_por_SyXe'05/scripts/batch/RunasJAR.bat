@echo off
SetLocal
cls

echo.
echo.
echo        Runas JAR Enabler
echo. ------------------------------
echo.
echo Adding JAR runas command..
reg ADD HKLM\SOFTWARE\Classes\jarfile\shell\runas\command /ve /t REG_SZ /d "\"C:\Program Files\Java\jre1.8.0_60\bin\javaw.exe\" -jar \"%%1\" %%*" /f
if %ERRORLEVEL% neq 0 goto Error
call :Colorize 06 OK
echo Showing icon LUAShield..
reg ADD HKLM\SOFTWARE\Classes\jarfile\shell\runas /v HasLUAShield /t REG_SZ /d "" /f
if %ERRORLEVEL% neq 0 goto Error
call :Colorize 06 OK
echo Adding open command..
reg ADD HKLM\SOFTWARE\Classes\jarfile\shell\open\command /ve /t REG_SZ /d "\"C:\Program Files\Java\jre1.8.0_60\bin\javaw.exe\" -jar \"%%1\" %%*" /f
if %ERRORLEVEL% neq 0 goto Error
call :Colorize 06 OK
EndLocal
exit /B 0

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

:Error
echo Error creando Menu contextual
EndLocal
exit /B 1