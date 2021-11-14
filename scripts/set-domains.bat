@echo off
TITLE IPA - modifying HOSTS file
ECHO.

:: BatchGotAdmin
:-------------------------------------
:: Check for permissions
FSUTIL dirty query %SystemDrive% >nul
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"="
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------


:ACCEPTED
setlocal enabledelayedexpansion
::Backup hosts
copy /b/v/y %WINDIR%\System32\drivers\etc\hosts %~dp0\..\temp\hosts.%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
::Create your list of host domains
for /F "tokens=1,2 delims=	" %%A in (%~dp0\domains.txt) do (
    SET _host=%%B
    SET _ip=%%A
    SET NEWLINE=^& echo.
    ECHO Adding !_ip!       !_host!
    :: strip out this specific line and store in tmp file
    type %WINDIR%\System32\drivers\etc\hosts | findstr /v !_host! > tmp.txt
    :: re-add the line to it
    ECHO %NEWLINE%^!_ip!	!_host! >> tmp.txt
    :: overwrite host file
    copy /b/v/y tmp.txt %WINDIR%\System32\drivers\etc\hosts
    del tmp.txt
)

ipconfig /flushdns
ECHO.
ECHO.
ECHO Finished, you may close this window now.
ECHO.
PAUSE
EXIT
