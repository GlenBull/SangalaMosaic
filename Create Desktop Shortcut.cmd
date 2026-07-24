@echo off
rem Creates a "Sangala Mosaic" shortcut on your Desktop that opens the app,
rem with the turaco icon. Run this once; keep SangalaMosaic.html and Turaco.ico
rem together in this folder.
setlocal
set "APPDIR=%~dp0"
if "%APPDIR:~-1%"=="\" set "APPDIR=%APPDIR:~0,-1%"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$app=$env:APPDIR; $d=[Environment]::GetFolderPath('Desktop'); $w=New-Object -ComObject WScript.Shell; $s=$w.CreateShortcut((Join-Path $d 'Sangala Mosaic.lnk')); $s.TargetPath=(Join-Path $app 'SangalaMosaic.html'); $s.WorkingDirectory=$app; $s.IconLocation=((Join-Path $app 'Turaco.ico')+',0'); $s.Description='Sangala Mosaic - Mosaic Design Tool'; $s.Save()"
echo.
echo Created a "Sangala Mosaic" shortcut on your Desktop.
pause
