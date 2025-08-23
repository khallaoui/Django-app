@echo off
echo ========================================
echo    CONFIGURATION MYSQL - DJANGO
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

echo Configuration MySQL pour Django...
echo.

REM Exécuter le script de configuration MySQL
py setup_mysql.py

echo.
echo ========================================
echo Configuration MySQL terminee
echo ========================================
pause