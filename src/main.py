import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import webbrowser
import sys
import subprocess
import time
import os

PORT = 5000
FLASK_PATH = "server.py"
LOGO_PATH = "static/logo.png"
flask_process = None

def start_flask():
    global flask_process
    flask_process = subprocess.Popen([sys.executable, FLASK_PATH])
    time.sleep(2)

def on_continue():
    threading.Thread(target=start_flask, daemon=True).start()
    time.sleep(2)
    webbrowser.open(f"http://127.0.0.1:{PORT}")
    root.iconify()

def on_close():
    global flask_process
    if flask_process and flask_process.poll() is None:
        flask_process.terminate()
        flask_process.wait()
    root.destroy()
    sys.exit(0)

root = tk.Tk()
root.title("Velocio T&S - Démarrage")

main_frame = ttk.Frame(root, padding=18)
main_frame.pack(fill="both", expand=True)

# --- Logo ---
if os.path.exists(LOGO_PATH):
    logo_img = Image.open(LOGO_PATH)
    w, h = logo_img.size
    base_w = 140
    if w > base_w:
        ratio = base_w / w
        logo_img = logo_img.resize((base_w, int(h * ratio)), Image.LANCZOS)
    logo = ImageTk.PhotoImage(logo_img)
    logo_label = ttk.Label(main_frame, image=logo)
    logo_label.image = logo
    logo_label.pack(pady=(0, 12))

# --- Message ---
msg = (
    "Pour garantir le bon fonctionnement de Velocio T&S,\n"
    "merci de laisser cette boîte ouverte (elle restera en arrière-plan).\n\n"
    "Le bouton \"Fermer Velocio T&S\" ou la croix clorurera proprement l'appication\n\n"
    
    "Cliquez sur \"Continuer\" pour ouvrir l'application dans votre navigateur."
)
label = ttk.Label(main_frame, text=msg, wraplength=370, justify="left", font=("Arial", 11))
label.pack(pady=8)

# --- Boutons colorés ---
btn_frame = ttk.Frame(main_frame)
btn_frame.pack(pady=20)

btn_continuer = tk.Button(
    btn_frame,
    text="Continuer",
    width=18,
    command=on_continue,
    bg="green",
    fg="white",
    activebackground="#23a023",
    activeforeground="white",
    font=("Arial", 11, "bold")
)
btn_continuer.pack(side="left", padx=12)

btn_fermer = tk.Button(
    btn_frame,
    text="Fermer Velocio T&S",
    width=18,
    command=on_close,
    bg="red",
    fg="white",
    activebackground="#c82323",
    activeforeground="white",
    font=("Arial", 11, "bold")
)
btn_fermer.pack(side="left", padx=12)

root.protocol("WM_DELETE_WINDOW", on_close)

# --- Taille automatique ---
root.update_idletasks()
window_width = main_frame.winfo_reqwidth() + 30
window_height = main_frame.winfo_reqheight() + 30
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

root.mainloop()