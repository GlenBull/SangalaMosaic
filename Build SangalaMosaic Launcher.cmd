@echo off
REM ==========================================================================
REM  Build SangalaMosaic.exe -- the desktop launcher for Sangala Mosaic.
REM  It is a real program (like Sangala Studio's exe), so it is NOT blocked the
REM  way school/managed Windows blocks .cmd scripts. Double-clicking it opens
REM  SangalaMosaic.html (kept next to it) in the browser. The turaco icon is
REM  embedded, so the exe and any Desktop shortcut to it show the turaco.
REM  Compiled in-box with the .NET compiler already in Windows -- no admin.
REM
REM  Needs, together in this folder:  SangalaMosaicLauncher.cs  and  Turaco.ico
REM  After building, keep SangalaMosaic.exe next to SangalaMosaic.html.
REM ==========================================================================
setlocal
cd /d "%~dp0"

set "OUT=SangalaMosaic.exe"
set "CSC=%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if not exist "%CSC%" set "CSC=%WINDIR%\Microsoft.NET\Framework\v4.0.30319\csc.exe"
if not exist "%CSC%" ( echo Could not find the built-in .NET compiler ^(csc.exe^). & pause & exit /b 1 )
if not exist "Turaco.ico" ( echo Could not find Turaco.ico ^(the program icon^) in this folder. & pause & exit /b 1 )

echo Building %OUT% ...
"%CSC%" /nologo /target:winexe /out:"%OUT%" ^
  /win32icon:"Turaco.ico" ^
  /reference:System.dll ^
  /reference:System.Drawing.dll ^
  /reference:System.Windows.Forms.dll ^
  "SangalaMosaicLauncher.cs"

if errorlevel 1 (
  echo.
  echo BUILD FAILED. Copy the red error messages above and send them back.
  echo.
  pause
  exit /b 1
)

echo.
echo Build succeeded:  "%~dp0%OUT%"
echo Keep SangalaMosaic.exe next to SangalaMosaic.html, then double-click the exe.
echo.
pause
