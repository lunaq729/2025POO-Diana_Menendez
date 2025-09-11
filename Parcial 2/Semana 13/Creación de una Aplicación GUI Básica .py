import json
import tkinter as tk
from tkinter import messagebox

# ======================
# Configuración JSON embebida con COLORES
# ======================
config_json = """
{
  "app": {
    "title": "Gestión de Datos - Ejemplo GUI Diana",
    "size": "400x300",
    "widgets": [
      {
        "type": "Frame",
        "name": "frame_superior",
        "options": { "bg": "#f0f8ff" },
        "pack": { "side": "top", "pady": 10 }
      },
      {
        "type": "Entry",
        "name": "entrada",
        "parent": "frame_superior",
        "options": { "width": 30, "bg": "#fffacd", "fg": "black" },
        "pack": { "side": "left", "padx": 5 }
      },
      {
        "type": "Button",
        "name": "btn_agregar",
        "parent": "frame_superior",
        "options": { "text": "Agregar", "command": "agregar", "bg": "#98fb98", "activebackground": "#32cd32" },
        "pack": { "side": "left", "padx": 5 }
      },
      {
        "type": "Listbox",
        "name": "lista",
        "options": { "width": 50, "height": 10, "selectmode": "multiple", "bg": "#e6e6fa", "fg": "black" },
        "pack": { "side": "top", "pady": 10 }
      },
      {
        "type": "Button",
        "name": "btn_limpiar",
        "options": { "text": "Limpiar", "command": "limpiar", "bg": "#ff7f7f", "activebackground": "#ff4040" },
        "pack": { "side": "top", "pady": 5 }
      }
    ]
  }
}
"""

# ======================
# Parsear JSON
# ======================
config = json.loads(config_json)

# ======================
# Funciones de la lógica
# ======================
def agregar():
    texto = entrada.get()
    if texto.strip():
        lista.insert(tk.END, texto)
        entrada.delete(0, tk.END)
    else:
        messagebox.showwarning("Advertencia", "No se puede agregar un texto vacío.")

def limpiar():
    seleccion = lista.curselection()
    if seleccion:
        for i in reversed(seleccion):
            lista.delete(i)
    else:
        lista.delete(0, tk.END)

# ======================
# Crear la ventana principal
# ======================
root = tk.Tk()
root.title(config["app"]["title"])
root.geometry(config["app"]["size"])
root.configure(bg="#dcdcdc")  # Fondo general de la ventana

widgets = {}

for widget in config["app"]["widgets"]:
    tipo = widget["type"]
    nombre = widget["name"]
    opciones = widget.get("options", {})
    parent = root if "parent" not in widget else widgets[widget["parent"]]

    # Crear widget según tipo
    if tipo == "Frame":
        w = tk.Frame(parent, **opciones)
    elif tipo == "Entry":
        w = tk.Entry(parent, **opciones)
    elif tipo == "Button":
        if opciones.get("command") == "agregar":
            opciones["command"] = agregar
        elif opciones.get("command") == "limpiar":
            opciones["command"] = limpiar
        w = tk.Button(parent, **opciones)
    elif tipo == "Listbox":
        w = tk.Listbox(parent, **opciones)
    else:
        continue

    widgets[nombre] = w
    pack_conf = widget.get("pack", {})
    w.pack(**pack_conf)

# ======================
# Variables globales útiles
# ======================
entrada = widgets.get("entrada")
lista = widgets.get("lista")

# ======================
# Ejecutar la app
# ======================
root.mainloop()
