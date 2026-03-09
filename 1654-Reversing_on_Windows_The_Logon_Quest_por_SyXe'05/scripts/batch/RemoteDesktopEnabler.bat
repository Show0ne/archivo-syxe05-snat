@echo off
SetLocal
cls

echo.
echo.
echo      Remote Desktop Service Enabler
echo. ---------------------------------------
echo.
echo "Adding firewall rules"
netsh advfirewall firewall set rule name="Escritorio Remoto (TCP de entrada)" new Profile=Domain Enable=Yes 1< nul
if %ERRORLEVEL% neq 0 goto Error
call :Colorize 06 OK
echo.&echo "Allowing remote connection"
reg ADD "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f 1< nul
if %ERRORLEVEL% neq 0 goto Error
call :Colorize 06  Hecho^!
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
echo Error habilitando regla de entrada en el cortafuegos
EndLocal
exit /B 1