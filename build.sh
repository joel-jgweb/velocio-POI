#!/bin/bash
echo "🚀 Compilation de Velocio-POI en exécutable Linux..."
PROJECT_DIR="$(dirname "$0")"
SRC_DIR="$PROJECT_DIR/src"
DIST_DIR="$PROJECT_DIR/dist"
BUILD_DIR="$PROJECT_DIR/build"
SPEC_FILE="$PROJECT_DIR/velocio-poi.spec"

# Vérifications
[ ! -f "$SRC_DIR/splash.html" ] && echo "❌ Erreur : splash.html introuvable" && exit 1
[ ! -f "$SRC_DIR/server.py" ] && echo "❌ Erreur : server.py introuvable" && exit 1

# Nettoyage
echo "🧹 Nettoyage des anciens builds..."
rm -rf "$BUILD_DIR" "$DIST_DIR" "$SPEC_FILE"

# Génération du .spec
cat > "$SPEC_FILE" << 'EOF'
a = Analysis(
    ['src/start.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/templates', 'templates'),
        ('src/static', 'static'),
        ('src/splash.html', '.'),
        ('src/uploads', 'uploads'),
    ],
    hiddenimports=[
        'flask',
        'gpxpy',
        'shapely',
        'folium',
        'requests',
        'lxml',
        'geopy',
        'markupsafe',
        'jinja2',
        'click',
        'itsdangerous',
        'werkzeug.serving',
        'server',
        'cache',
        'overpass',
        'poi',
        'enrich',
        'gpx_utils',
        'exporter',
        'map',
        'config'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=None,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='velocio-poi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # <--- CONSOLE DÉSACTIVÉE
)
EOF

# Lancement
echo "📦 Lancement de PyInstaller..."
# --noconsole = pas de fenêtre terminal
pyinstaller --clean --noconsole "$SPEC_FILE"

# Fin
if [ $? -eq 0 ]; then
    echo "✅ Succès ! Lance : ./dist/velocio-poi/velocio-poi"
else
    echo "❌ Échec"
    exit 1
fi

chmod +x dist/velocio-poi/velocio-poi 2>/dev/null || true