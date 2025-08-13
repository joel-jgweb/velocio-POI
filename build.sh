#!/bin/bash

# 1. Crée le dossier compilLinux et le venv
COMPIL_DIR="../compilLinux"
VENV_DIR="$COMPIL_DIR/venv"
REQUIREMENTS="requirements.txt"

echo "🛠️ Création du dossier $COMPIL_DIR et de l'environnement virtuel..."
mkdir -p "$COMPIL_DIR"
python3 -m venv "$VENV_DIR"

# 2. Active le venv
source "$VENV_DIR/bin/activate"

# 3. Installe les dépendances du projet (si requirements.txt présent)
if [ -f "$REQUIREMENTS" ]; then
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS"
else
    echo "⚠️  Pas de requirements.txt trouvé. Installe manuellement les dépendances."
fi

# 4. Installe PyInstaller
pip install pyinstaller

# 5. Compile avec PyInstaller
echo "🚀 Compilation avec PyInstaller (environnement compilLinux)..."
pyinstaller --clean velocio-poi.spec

# 6. Désactive le venv
deactivate

echo "✅ Compilation terminée."
echo "Les fichiers générés sont dans dist/"