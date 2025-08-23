@echo off
echo ========================================
echo    CREATION BASE DE DONNEES MYSQL
echo ========================================
echo.

REM Aller dans le bon répertoire
cd /d "%~dp0"

echo Probleme detecte: Base de donnees manquante
echo Solution: Creation de la base de donnees
echo.

REM Exécuter le script de création de base de données
py create_database.py

echo.
echo ========================================
echo Creation terminee
echo ========================================
pause