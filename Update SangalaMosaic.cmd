@echo off
REM ==========================================================================
REM  Update Sangala Mosaic to the latest version from GitHub.
REM  Double-click this file. No admin, no install, no git needed.
REM
REM  Sangala Mosaic is a single page -- SangalaMosaic.html -- so this replaces
REM  just that one file (and fetches the turaco icon it uses on the Desktop
REM  shortcut, if it is missing).
REM
REM  It only downloads when there is actually a newer version, and it never
REM  leaves you half-updated: if the page does not download completely, nothing
REM  on your computer is changed.
REM
REM  It also puts a "Sangala Mosaic" icon on your Desktop -- and refreshes it if
REM  you have moved this folder -- whether or not there was anything new. If you
REM  only have this .cmd, running it once installs the whole program.
REM ==========================================================================
setlocal
cd /d "%~dp0"

set "BASE=https://raw.githubusercontent.com/GlenBull/SangalaMosaic/main"
set "HTML=SangalaMosaic.html"
set "ICO=Turaco.ico"
set "TMPHTML=SangalaMosaic.html.new"
set "TMPICO=Turaco.ico.new"

echo Checking for a newer Sangala Mosaic...
echo.

if exist "%TMPHTML%" del "%TMPHTML%" >nul 2>&1
if exist "%TMPICO%"  del "%TMPICO%"  >nul 2>&1

REM ---- 1. Download the page. curl is built into Windows 10/11; PowerShell is the fallback.
call :download "%BASE%/%HTML%" "%TMPHTML%"
if not exist "%TMPHTML%" goto :failed

REM A good page ends with the closing </html> tag; a truncated download will not.
find "</html>" "%TMPHTML%" >nul 2>&1
if errorlevel 1 goto :badfile

REM ---- 2. Compare release versions. The marker on line 2 is the first match in
REM     each file; taking the first line makes the About-screen reference (which
REM     also mentions the marker name) irrelevant. Same version -> nothing to do.
set "REMOTEVER="
set "LOCALVER="
for /f "delims=" %%V in ('findstr /c:"SANGALA_MOSAIC_VERSION" "%TMPHTML%"') do if not defined REMOTEVER set "REMOTEVER=%%V"
if exist "%HTML%" for /f "delims=" %%V in ('findstr /c:"SANGALA_MOSAIC_VERSION" "%HTML%"') do if not defined LOCALVER set "LOCALVER=%%V"

if defined LOCALVER if "%LOCALVER%"=="%REMOTEVER%" (
  del "%TMPHTML%" >nul 2>&1
  echo Already up to date - nothing downloaded.
  call :geticon
  call :shortcut
  echo.
  pause
  exit /b 0
)

REM ---- 3. There is a newer version (or no copy yet). Swap the page in.
echo A newer version is available. Updating...
if exist "%HTML%" copy /y "%HTML%" "%HTML%.bak" >nul
move /y "%TMPHTML%" "%HTML%" >nul
if not exist "%HTML%" goto :failed

REM ---- 4. Make sure the turaco icon is present, then place/refresh the shortcut.
call :geticon
call :shortcut

echo.
echo Done - Sangala Mosaic is up to date.
echo.
echo   Open it from the "Sangala Mosaic" icon on your Desktop. If a page was
echo   already open in your browser, press F5 to refresh it.
echo.
echo   (Your previous version was saved as %HTML%.bak, just in case.)
echo.
pause
exit /b 0

REM ==========================================================================
:download
REM  %1 = URL, %2 = output file. curl if present, else PowerShell.
where curl >nul 2>&1
if %errorlevel%==0 (
  curl -L -f -s -o "%~2" "%~1"
) else (
  powershell -NoProfile -Command "try { Invoke-WebRequest -Uri '%~1' -OutFile '%~2' -UseBasicParsing } catch { exit 1 }"
)
goto :eof

REM ==========================================================================
:geticon
REM  Fetch the turaco icon if it is missing (it rarely changes). Best effort:
REM  a failure here never fails the update -- the app runs without it.
if exist "%ICO%" goto :eof
call :download "%BASE%/%ICO%" "%TMPICO%"
for %%F in ("%TMPICO%") do if %%~zF GTR 1000 move /y "%TMPICO%" "%ICO%" >nul 2>&1
if exist "%TMPICO%" del "%TMPICO%" >nul 2>&1
goto :eof

REM ==========================================================================
:shortcut
REM  Put (or refresh) a "Sangala Mosaic" icon on the Desktop that opens the page
REM  in THIS folder with the turaco icon -- so it keeps working after an update
REM  and is corrected if the folder has been moved. Convenience only: it writes
REM  only to the user's own Desktop, and never changes the update's exit code.
REM  Paths travel as environment variables so spaces/apostrophes cannot break the
REM  quoting, and SpecialFolders finds the real Desktop even under OneDrive.
if not exist "%~dp0%HTML%" goto :eof
set "SANGALA_HOME=%~dp0"
set "SANGALA_TARGET=%~dp0%HTML%"
set "SANGALA_ICON=%~dp0%ICO%"
powershell -NoProfile -Command "try { $ws = New-Object -ComObject WScript.Shell; $p = Join-Path $ws.SpecialFolders('Desktop') 'Sangala Mosaic.lnk'; $l = $ws.CreateShortcut($p); $l.TargetPath = $env:SANGALA_TARGET; $l.WorkingDirectory = $env:SANGALA_HOME.TrimEnd('\'); if (Test-Path $env:SANGALA_ICON) { $l.IconLocation = $env:SANGALA_ICON + ',0' }; $l.Description = 'Sangala Mosaic - Mosaic Design Tool'; $l.Save(); exit 0 } catch { exit 1 }" >nul 2>&1
if errorlevel 1 goto :eof
echo.
echo   A "Sangala Mosaic" icon is on your Desktop, ready to use.
goto :eof

REM ==========================================================================
:badfile
del "%TMPHTML%" >nul 2>&1
del "%TMPICO%"  >nul 2>&1
:failed
echo.
echo Update FAILED - could not download a complete copy.
echo Your current Sangala Mosaic was NOT changed, so it still works.
echo Check the internet connection and run this again.
echo.
pause
exit /b 1
