@echo off
SetLocal
cls

if ""%1"" == """" goto ErrorParams
set filePath="%1"
echo path found: %filePath%
if ""%2"" == """" goto ErrorParams
set userName="%2"
echo user found: %userName%

echo.
echo.
echo       ADMIN REMOVER
echo. ------------------------
echo.
set /p "= Deleting %userName% ACE.. " < nul
icacls %filePath% /remove %userName%
call :Colorize 06 OK
echo.&call :Colorize 06  Hecho^!
pause > nul
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