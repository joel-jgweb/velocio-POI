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
