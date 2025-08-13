#!/bin/bash

DIST_DIR="dist"
OUT_DIR="DistriLinux"
EXECUTABLE="velocio_T&S"
ICON="icon.png"
README="GUIDE.txt"
SRC_ICON="src/static/icon.ico"
DST_ICON="$DIST_DIR/$ICON"
INSTALL_SCRIPT="$OUT_DIR/install.sh"

echo "🛠️ Création du dossier de distribution Linux..."

# Conversion automatique de icon.ico en icon.png (si nécessaire)
if [ ! -f "$DST_ICON" ]; then
    if [ -f "$SRC_ICON" ]; then
        mkdir -p "$DIST_DIR"
        if command -v convert >/dev/null 2>&1; then
            convert "$SRC_ICON" "$DST_ICON"
            if [ $? -eq 0 ]; then
                echo "✅ Icône convertie : $DST_ICON"
            else
                echo "❌ Erreur lors de la conversion de l'icône."
                exit 1
            fi
        else
            echo "❌ ImageMagick (convert) n'est pas installé. Installe-le avec : sudo apt install imagemagick"
            exit 1
        fi
    else
        echo "❌ Fichier source introuvable : $SRC_ICON"
        exit 1
    fi
fi

# Création du dossier de distribution
mkdir -p "$OUT_DIR"

# Copie de l’exécutable
if [ -f "$DIST_DIR/$EXECUTABLE" ]; then
    cp "$DIST_DIR/$EXECUTABLE" "$OUT_DIR/"
    echo "✔️  $EXECUTABLE copié."
else
    echo "❌ Erreur : $DIST_DIR/$EXECUTABLE introuvable !"
    exit 1
fi

# Copie de l’icône
if [ -f "$DST_ICON" ]; then
    cp "$DST_ICON" "$OUT_DIR/"
    echo "✔️  $ICON copié."
else
    echo "❌ Erreur : $DST_ICON introuvable !"
    exit 1
fi

# Génération du script install.sh pour l'utilisateur final
cat > "$INSTALL_SCRIPT" <<'EOF'
#!/bin/bash

APPNAME="velocio_T&S"
ICON="icon.png"
LAUNCHER="velocio_T&S.desktop"
INSTALLDIR="/usr/local/bin"
DESKTOPDIR="$HOME/Bureau"
ICONDIR="$HOME/.local/share/icons"
MENU_DIR="$HOME/.local/share/applications"

echo "🔧 Installation de \$APPNAME dans \$INSTALLDIR"
sudo cp "\$APPNAME" "\$INSTALLDIR/"
sudo chmod +x "\$INSTALLDIR/\$APPNAME"

echo "🖼️ Installation de l'icône"
mkdir -p "\$ICONDIR"
cp "\$ICON" "\$ICONDIR/\$ICON"

# Création du lanceur .desktop (menu + bureau)
cat > "\$MENU_DIR/\$LAUNCHER" <<EOL
[Desktop Entry]
Type=Application
Name=Velocio Traces & Spots
Exec=\$INSTALLDIR/\$APPNAME
Icon=\$ICONDIR/\$ICON
Terminal=false
Categories=Other;
EOL
chmod +x "\$MENU_DIR/\$LAUNCHER"
echo "✔️  Lanceur créé dans le menu (Autres)"

cp "\$MENU_DIR/\$LAUNCHER" "\$DESKTOPDIR/\$LAUNCHER"
chmod +x "\$DESKTOPDIR/\$LAUNCHER"
echo "✔️  Lanceur copié sur le bureau"

echo "✅ Installation terminée !"
echo "Un raccourci a été ajouté sur votre bureau et dans le menu (Autres)"
echo "Pour désinstaller, supprimez /usr/local/bin/\$APPNAME, \$ICONDIR/\$ICON et \$MENU_DIR/\$LAUNCHER"
EOF

chmod +x "$INSTALL_SCRIPT"
echo "✔️  Script install.sh généré dans $OUT_DIR/"

# Création/ajout du guide d’utilisation
cat > "$OUT_DIR/$README" <<EOF
==========================================
Velocio Traces & Spots - Installation Linux
==========================================

1. Ouvrez un terminal dans le dossier DistriLinux
2. Tapez : chmod +x install.sh
3. Lancez le script : ./install.sh

L’application apparaîtra dans le menu (rubrique Autres) et un raccourci sera ajouté sur votre bureau.

Exécutable : velocio_T&S
Icône : icon.png

Pour toute question ou bug : https://github.com/joel-jgweb/velocio-POI
EOF
echo "✔️  $README créé."

echo "✅ Distribution prête dans $OUT_DIR/"