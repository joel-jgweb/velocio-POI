from PIL import Image
import os

LOGO_PATH = "static/logo.png"
print("Chemin attendu:", LOGO_PATH)
print("Existe?", os.path.exists(LOGO_PATH))

if os.path.exists(LOGO_PATH):
    img = Image.open(LOGO_PATH)
    print("Taille image:", img.size)
else:
    print("Image introuvable !")
