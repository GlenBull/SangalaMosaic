@echo off
REM ===============================================================
REM  Create Desktop Shortcut.cmd
REM
REM  Puts a "Sangala Mosaic" icon on your Desktop so you can start
REM  the program without hunting for this folder.
REM
REM  Double-click this file once. It points the shortcut at
REM  SangalaMosaic.exe sitting next to it (the turaco icon is built in),
REM  so it works no matter where you keep the Sangala Mosaic folder - and
REM  it keeps working after Update SangalaMosaic.cmd updates the program.
REM
REM  No admin rights are needed: it only writes to your own Desktop.
REM  Safe to run again - it simply refreshes the shortcut.
REM ===============================================================
setlocal
set "SANGALA_HOME=%~dp0"
set "SANGALA_TARGET=%~dp0SangalaMosaic.exe"
REM  THE SHORTCUT TAKES ITS PICTURE FROM Turaco.ico, NOT FROM THE EXE. Windows caches an icon
REM  against the file it came from, so rebuilding the launcher in place leaves the Desktop showing
REM  the OLD picture however many times the shortcut is remade - clearing the cache does not shift
REM  it, but a file Windows has not cached does. The icon's home is the .ico anyway, and the exe
REM  still carries it for anyone who runs the exe directly.
set "SANGALA_ICON=%~dp0Turaco.ico"

echo.
echo   Creating a Desktop shortcut for Sangala Mosaic...

if not exist "%SANGALA_TARGET%" (
  echo.
  echo   Could not find SangalaMosaic.exe in this folder:
  echo     %SANGALA_HOME%
  echo.
  echo   Keep this file next to SangalaMosaic.exe, then run it again.
  echo.
  pause
  exit /b 1
)

REM  The paths travel as environment variables, so folder names with
REM  spaces or apostrophes cannot break the quoting. SpecialFolders
REM  finds the real Desktop even when OneDrive has redirected it. The
REM  turaco icon is embedded in the exe, so the shortcut takes its icon
REM  straight from the target.
powershell -NoProfile -Command "try { $ws = New-Object -ComObject WScript.Shell; $desktop = $ws.SpecialFolders('Desktop'); $path = Join-Path $desktop 'Sangala Mosaic.lnk'; $lnk = $ws.CreateShortcut($path); $lnk.TargetPath = $env:SANGALA_TARGET; $lnk.WorkingDirectory = $env:SANGALA_HOME.TrimEnd('\'); $lnk.IconLocation = $env:SANGALA_ICON + ',0'; $lnk.Description = 'Sangala Mosaic - Mosaic Design Tool'; $lnk.Save(); Write-Host ''; Write-Host ('   Shortcut created: ' + $path); exit 0 } catch { Write-Host ''; Write-Host ('   Could not create the shortcut: ' + $_.Exception.Message); exit 1 }"

if errorlevel 1 (
  echo.
  echo   The shortcut was not created. You can still make one by hand:
  echo   right-click SangalaMosaic.exe, choose Show more options,
  echo   then Send to - Desktop.
  echo.
  pause
  exit /b 1
)

echo.
echo   Done. Look for the "Sangala Mosaic" icon on your Desktop and
echo   double-click it to start.
echo.
pause
