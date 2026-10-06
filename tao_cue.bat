@echo off
rem Tao file .cue cho anh dia PS1 mot track (Mode2/2352).
rem Cach dung: keo tha file .bin len tep nay,
rem hoac nhay dup de tao .cue cho moi file .bin trong cung thu muc.
setlocal DisableDelayedExpansion
cd /d "%~dp0"
if "%~1"=="" goto tat_ca
:tung_file
if "%~1"=="" goto xong
call :tao "%~1"
shift
goto tung_file
:tat_ca
set "co=0"
for %%F in (*.bin) do (set "co=1" & call :tao "%%~fF")
if "%co%"=="0" echo Khong thay file .bin nao trong thu muc nay.
goto xong
:tao
if /i not "%~x1"==".bin" (echo Bo qua "%~nx1" - khong phai file .bin & goto :eof)
> "%~dpn1.cue" (
  echo FILE "%~nx1" BINARY
  echo   TRACK 01 MODE2/2352
  echo     INDEX 01 00:00:00
)
echo Da tao "%~n1.cue"
goto :eof
:xong
echo.
pause
