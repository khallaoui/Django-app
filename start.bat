@echo off
echo ========================================
echo    DEMARRAGE APPLICATION DJANGO
echo ========================================
echo.

REM Aller dans le bon répertoire
cd /d "%~dp0"

REM Vérifier si manage.py existe
if not exist "manage.py" (
    echo ERREUR: manage.py non trouve
    echo Assurez-vous d'etre dans le bon repertoire
    pause
    exit /b 1
)

echo Configuration rapide avec SQLite...
echo.

REM Exécuter le script de configuration
py setup_quick.py

echo.
echo ========================================
echo Configuration terminee
echo ========================================
pause