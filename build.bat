@echo off
:: ---------------------------------------------------------------------------
:: Script de compilation pour velocio-POI - Version corrigée
:: ---------------------------------------------------------------------------
cd /d "%~dp0"

echo ===[ DEBUT DU BUILD ]===

:: Vérification de Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH.
    echo Installez Python depuis https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

:: Création de l'environnement virtuel si inexistant
if not exist venv (
    echo.
    echo [INFO] Création de l'environnement virtuel 'venv'...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERREUR] Échec de la création de l'environnement virtuel.
        pause
        exit /b 3
    )
    echo [OK] Environnement virtuel créé.
)

:: Activation
echo.
echo [INFO] Activation de l'environnement virtuel...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel.
    pause
    exit /b 4
)

:: Mise à jour de pip
echo.
echo [INFO] Mise à jour de pip...
python -m pip install --upgrade pip

:: Installation des dépendances
echo.
if exist requirements.txt (
    echo [INFO] Installation des dépendances...
    pip install -r requirements.txt
) else (
    echo [ERREUR] Fichier requirements.txt introuvable.
    pause
    exit /b 5
)

:: Installation de PyInstaller
echo.
echo [INFO] Installation de PyInstaller...
pip install pyinstaller

:: Compilation SANS fenêtre de terminal
echo.
echo [INFO] Compilation avec PyInstaller (mode sans console)...
pyinstaller --clean --onedir --windowed --add-data "src\templates;templates" --add-data "src\static;static" --add-data "src\uploads;uploads" --add-data "src\splash.html;." src\start.py

if %errorlevel% neq 0 (
    echo [ERREUR] La compilation a échoué.
    pause
    exit /b 8
)

echo.
echo [SUCCÈS] ✅ Compilation terminée !
echo L'application sera lancée SANS fenêtre de terminal.
echo Exécutable : 'dist\start\start.exe'
pause