@echo off
REM SC Schiffskauf-Planer neu bauen (Preise live von UEX ziehen).
cd /d "%~dp0"
py schiffskauf_planer_bauen.py
if errorlevel 1 (
  echo.
  echo FEHLER beim Bauen - bitte Internetverbindung pruefen.
  pause
  exit /b 1
)
echo.
echo Fertig. SC_Schiffskauf_Planer.html wurde aktualisiert.
pause
