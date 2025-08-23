@echo off
echo ========================================
echo    SERVEUR DJANGO - GESTION ALERTES
echo ========================================
echo.
echo Demarrage du serveur...
echo Application accessible sur: http://127.0.0.1:8000/
echo Administration sur: http://127.0.0.1:8000/admin/
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo ========================================
echo.

REM Aller dans le bon répertoire
cd /d "%~dp0"

REM Démarrer le serveur
py manage.py runserver

echo.
echo Serveur arrete.
pause