@echo off
REM ===============================================================
REM  Create Desktop Shortcut.cmd
REM
REM  Puts a "Sangala Mosaic" icon on your Desktop so you can start
REM  the program without hunting for this folder.
REM
REM  Double-click this file once. It points the shortcut at the
REM  SangalaMosaic.html sitting next to it, with the turaco icon, so
REM  it works no matter where you keep the Sangala Mosaic folder - and
REM  it keeps working after Update SangalaMosaic.cmd updates the program.
REM
REM  No admin rights are needed: it only writes to your own Desktop.
REM  Safe to run again - it simply refreshes the shortcut.
REM ===============================================================
setlocal
set "SANGALA_HOME=%~dp0"
set "SANGALA_TARGET=%~dp0SangalaMosaic.html"
set "SANGALA_ICON=%~dp0Turaco.ico"

echo.
echo   Creating a Desktop shortcut for Sangala Mosaic...

if not exist "%SANGALA_TARGET%" (
  echo.
  echo   Could not find SangalaMosaic.html in this folder:
  echo     %SANGALA_HOME%
  echo.
  echo   Keep this file next to SangalaMosaic.html, then run it again.
  echo.
  pause
  exit /b 1
)

REM  The paths travel as environment variables, so folder names with
REM  spaces or apostrophes cannot break the quoting. SpecialFolders
REM  finds the real Desktop even when OneDrive has redirected it. The
REM  turaco icon is used only if Turaco.ico is present.
powershell -NoProfile -Command "try { $ws = New-Object -ComObject WScript.Shell; $desktop = $ws.SpecialFolders('Desktop'); $path = Join-Path $desktop 'Sangala Mosaic.lnk'; $lnk = $ws.CreateShortcut($path); $lnk.TargetPath = $env:SANGALA_TARGET; $lnk.WorkingDirectory = $env:SANGALA_HOME.TrimEnd('\'); if (Test-Path $env:SANGALA_ICON) { $lnk.IconLocation = $env:SANGALA_ICON + ',0' }; $lnk.Description = 'Sangala Mosaic - Mosaic Design Tool'; $lnk.Save(); Write-Host ''; Write-Host ('   Shortcut created: ' + $path); exit 0 } catch { Write-Host ''; Write-Host ('   Could not create the shortcut: ' + $_.Exception.Message); exit 1 }"

if errorlevel 1 (
  echo.
  echo   The shortcut was not created. You can still make one by hand:
  echo   right-click SangalaMosaic.html, choose Show more options,
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
