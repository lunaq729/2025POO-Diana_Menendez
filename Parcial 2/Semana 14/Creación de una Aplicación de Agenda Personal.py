import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # pip install tkcalendar

DATOS_FILE = "eventos.json"  # Archivo para persistir los eventos

# ======================
# Configuración JSON embebida
# ======================
config_json = """
{
  "app": {
    "title": "Agenda Personal - Ejemplo GUI Diana",
    "size": "700x400",
    "bg": "#f5f5f5",
    "widgets": [
      {
        "type": "Frame",
        "name": "frame_inputs",
        "options": { "bg": "#f0f8ff", "pady": 10 },
        "pack": { "side": "top", "fill": "x" }
      },
      {
        "type": "Label",
        "parent": "frame_inputs",
        "options": { "text": "Fecha:", "bg": "#f0f8ff" },
        "grid": { "row": 0, "column": 0, "padx": 5, "pady": 5, "sticky": "e" }
      },
      {
        "type": "DateEntry",
        "name": "entry_fecha",
        "parent": "frame_inputs",
        "options": { "width": 12, "background": "darkblue", "foreground": "white", "borderwidth": 2, "date_pattern": "dd/mm/yyyy" },
        "grid": { "row": 0, "column": 1, "padx": 5, "pady": 5 }
      },
      {
        "type": "Label",
        "parent": "frame_inputs",
        "options": { "text": "Hora:", "bg": "#f0f8ff" },
        "grid": { "row": 0, "column": 2, "padx": 5, "pady": 5, "sticky": "e" }
      },
      {
        "type": "Entry",
        "name": "entry_hora",
        "parent": "frame_inputs",
        "options": { "width": 10, "bg": "#fffacd" },
        "grid": { "row": 0, "column": 3, "padx": 5, "pady": 5 }
      },
      {
        "type": "Label",
        "parent": "frame_inputs",
        "options": { "text": "Descripción:", "bg": "#f0f8ff" },
        "grid": { "row": 0, "column": 4, "padx": 5, "pady": 5, "sticky": "e" }
      },
      {
        "type": "Entry",
        "name": "entry_desc",
        "parent": "frame_inputs",
        "options": { "width": 30, "bg": "#fffacd" },
        "grid": { "row": 0, "column": 5, "padx": 5, "pady": 5 }
      },
      {
        "type": "Label",
        "parent": "frame_inputs",
        "options": { "text": "Cantidad:", "bg": "#f0f8ff" },
        "grid": { "row": 0, "column": 6, "padx": 5, "pady": 5, "sticky": "e" }
      },
      {
        "type": "Entry",
        "name": "entry_cantidad",
        "parent": "frame_inputs",
        "options": { "width": 8, "bg": "#fffacd" },
        "grid": { "row": 0, "column": 7, "padx": 5, "pady": 5 }
      },
      {
        "type": "Frame",
        "name": "frame_lista",
        "options": { "bg": "#e6e6fa", "pady": 10 },
        "pack": { "fill": "both", "expand": true }
      },
      {
        "type": "Treeview",
        "name": "tree",
        "parent": "frame_lista",
        "options": { "columns": ["Fecha", "Hora", "Descripción", "Cantidad"], "show": "headings" },
        "pack": { "fill": "both", "expand": true, "padx": 10, "pady": 10 }
      },
      {
        "type": "Frame",
        "name": "frame_botones",
        "options": { "bg": "#dcdcdc", "pady": 10 },
        "pack": { "side": "bottom", "fill": "x" }
      },
      {
        "type": "Button",
        "name": "btn_agregar",
        "parent": "frame_botones",
        "options": { "text": "Agregar Evento", "command": "agregar_evento", "bg": "#98fb98", "activebackground": "#32cd32" },
        "pack": { "side": "left", "padx": 10 }
      },
      {
        "type": "Button",
        "name": "btn_eliminar",
        "parent": "frame_botones",
        "options": { "text": "Eliminar Evento Seleccionado", "command": "eliminar_evento", "bg": "#ff7f7f", "activebackground": "#ff4040" },
        "pack": { "side": "left", "padx": 10 }
      },
      {
        "type": "Button",
        "name": "btn_salir",
        "parent": "frame_botones",
        "options": { "text": "Salir", "command": "salir", "bg": "#ffa500", "activebackground": "#ff8c00" },
        "pack": { "side": "right", "padx": 10 }
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
# Funciones para guardar y cargar eventos
# ======================
def cargar_eventos():
    if os.path.exists(DATOS_FILE):
        with open(DATOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_eventos(eventos):
    with open(DATOS_FILE, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)

# ======================
# Funciones de la lógica principal
# ======================
def refrescar_tree():
    tree = widgets["tree"]
    tree.delete(*tree.get_children())
    for evento in eventos_memoria:
        tree.insert("", tk.END, values=(evento["fecha"], evento["hora"], evento["descripcion"], evento["cantidad"]))

def agregar_evento():
    fecha = widgets["entry_fecha"].get()
    hora = widgets["entry_hora"].get()
    descripcion = widgets["entry_desc"].get()
    cantidad = widgets["entry_cantidad"].get()

    if not (fecha and hora and descripcion.strip() and cantidad.strip()):
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return

    if not cantidad.isdigit():
        messagebox.showwarning("Advertencia", "La cantidad debe ser un número entero.")
        return

    nuevo_evento = {
        "fecha": fecha,
        "hora": hora,
        "descripcion": descripcion.strip(),
        "cantidad": cantidad.strip()
    }
    eventos_memoria.append(nuevo_evento)
    guardar_eventos(eventos_memoria)
    refrescar_tree()

    widgets["entry_hora"].delete(0, tk.END)
    widgets["entry_desc"].delete(0, tk.END)
    widgets["entry_cantidad"].delete(0, tk.END)

def eliminar_evento():
    tree = widgets["tree"]
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione un evento para eliminar.")
        return

    confirm = messagebox.askyesno("Confirmar", "¿Desea eliminar el evento seleccionado?")
    if confirm:
        for item in seleccion:
            valores = tree.item(item, "values")
            # Buscar y eliminar del arreglo en memoria
            for evento in eventos_memoria:
                if (evento["fecha"], evento["hora"], evento["descripcion"], evento["cantidad"]) == valores:
                    eventos_memoria.remove(evento)
                    break
            tree.delete(item)
        guardar_eventos(eventos_memoria)
        refrescar_tree()

def salir():
    root.quit()

# ======================
# Crear ventana principal y cargar configuración
# ======================
root = tk.Tk()
root.title(config["app"]["title"])
root.geometry(config["app"]["size"])
root.configure(bg=config["app"]["bg"])

widgets = {}

for widget in config["app"]["widgets"]:
    tipo = widget["type"]
    nombre = widget.get("name")
    opciones = widget.get("options", {})
    parent = root if "parent" not in widget else widgets[widget["parent"]]

    if tipo == "Frame":
        w = tk.Frame(parent, **opciones)
    elif tipo == "Label":
        w = tk.Label(parent, **opciones)
    elif tipo == "Entry":
        w = tk.Entry(parent, **opciones)
    elif tipo == "DateEntry":
        w = DateEntry(parent, **opciones)
    elif tipo == "Button":
        cmd = opciones.get("command")
        if cmd == "agregar_evento":
            opciones["command"] = agregar_evento
        elif cmd == "eliminar_evento":
            opciones["command"] = eliminar_evento
        elif cmd == "salir":
            opciones["command"] = salir
        w = tk.Button(parent, **opciones)
    elif tipo == "Treeview":
        cols = opciones.pop("columns", [])
        w = ttk.Treeview(parent, columns=cols, **opciones)
        for col in cols:
            w.heading(col, text=col)
            if col == "Fecha":
                w.column(col, width=100)
            elif col == "Hora":
                w.column(col, width=80)
            elif col == "Cantidad":
                w.column(col, width=80)
            else:
                w.column(col, width=300)
    else:
        continue

    if nombre:
        widgets[nombre] = w

    if "pack" in widget:
        w.pack(**widget["pack"])
    elif "grid" in widget:
        w.grid(**widget["grid"])

# ======================
# Inicializar lista en memoria y cargar datos previos
# ======================
eventos_memoria = cargar_eventos()
refrescar_tree()

root.mainloop()
