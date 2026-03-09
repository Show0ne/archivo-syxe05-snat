@echo off
SetLocal
cls

echo.
echo.
echo        UAC Enabler
echo. --------------------------
echo.
echo "Enabling UAC"
reg ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 5 /f
reg ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA /t REG_DWORD /d 1 /f
reg ADD HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v PromptOnSecureDesktop /t REG_DWORD /d 1 /f
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
echo Error habilitando UAC
EndLocal
exit /B 1