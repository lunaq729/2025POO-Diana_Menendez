import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # pip install tkcalendar

DATOS_FILE = "Tareas.json"  # Archivo para persistir los eventos


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
    tree.delete(*tree.get_children())
    for evento in eventos_memoria:
        tree.insert(
            "",
            tk.END,
            values=(evento["tarea"], evento["fecha"], evento["hora"], evento["descripcion"], evento["estado"])
        )


def agregar_evento():
    tarea = entry_tarea.get().strip()
    fecha = entry_fecha.get()
    hora = entry_hora.get().strip()
    descripcion = entry_desc.get().strip()

    if not (tarea and fecha and hora and descripcion):
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        return

    nuevo_evento = {
        "tarea": tarea,
        "fecha": fecha,
        "hora": hora,
        "descripcion": descripcion,
        "estado": "Pendiente"
    }
    eventos_memoria.append(nuevo_evento)
    guardar_eventos(eventos_memoria)
    refrescar_tree()

    entry_tarea.delete(0, tk.END)
    entry_hora.delete(0, tk.END)
    entry_desc.delete(0, tk.END)


def eliminar_evento():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione una tarea para eliminar.")
        return

    confirm = messagebox.askyesno("Confirmar", "¿Desea eliminar la tarea seleccionada?")
    if confirm:
        for item in seleccion:
            valores = tree.item(item, "values")
            for evento in eventos_memoria:
                if (evento["tarea"], evento["fecha"], evento["hora"], evento["descripcion"], evento["estado"]) == valores:
                    eventos_memoria.remove(evento)
                    break
            tree.delete(item)
        guardar_eventos(eventos_memoria)
        refrescar_tree()


def marcar_completada():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione una tarea para marcar como completada.")
        return

    for item in seleccion:
        valores = tree.item(item, "values")
        for evento in eventos_memoria:
            if (evento["tarea"], evento["fecha"], evento["hora"], evento["descripcion"], evento["estado"]) == valores:
                evento["estado"] = "Completada"
                break
    guardar_eventos(eventos_memoria)
    refrescar_tree()


def editar_evento():
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Seleccione una tarea para editar.")
        return

    item = seleccion[0]
    valores = tree.item(item, "values")

    # Buscar la tarea original
    for evento in eventos_memoria:
        if (evento["tarea"], evento["fecha"], evento["hora"], evento["descripcion"], evento["estado"]) == valores:
            tarea_original = evento
            break
    else:
        return

    abrir_modal_edicion(tarea_original)


def abrir_modal_edicion(tarea_original):
    # Ventana modal
    modal = tk.Toplevel(root)
    modal.title("Editar Tarea")
    modal.geometry("400x250")
    modal.grab_set()

    tk.Label(modal, text="Tarea:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_tarea_modal = tk.Entry(modal, width=30)
    entry_tarea_modal.grid(row=0, column=1, padx=5, pady=5)
    entry_tarea_modal.insert(0, tarea_original["tarea"])

    tk.Label(modal, text="Fecha:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_fecha_modal = DateEntry(modal, width=12, date_pattern="dd/mm/yyyy")
    entry_fecha_modal.grid(row=1, column=1, padx=5, pady=5)
    entry_fecha_modal.set_date(tarea_original["fecha"])

    tk.Label(modal, text="Hora:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_hora_modal = tk.Entry(modal, width=15)
    entry_hora_modal.grid(row=2, column=1, padx=5, pady=5)
    entry_hora_modal.insert(0, tarea_original["hora"])

    tk.Label(modal, text="Descripción:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_desc_modal = tk.Entry(modal, width=30)
    entry_desc_modal.grid(row=3, column=1, padx=5, pady=5)
    entry_desc_modal.insert(0, tarea_original["descripcion"])

    def guardar_cambios():
        tarea_original["tarea"] = entry_tarea_modal.get().strip()
        tarea_original["fecha"] = entry_fecha_modal.get()
        tarea_original["hora"] = entry_hora_modal.get().strip()
        tarea_original["descripcion"] = entry_desc_modal.get().strip()
        guardar_eventos(eventos_memoria)
        refrescar_tree()
        modal.destroy()

    btn_guardar = tk.Button(modal, text="Guardar Cambios", bg="lightblue", command=guardar_cambios)
    btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)


def salir():
    root.quit()


# ======================
# Crear ventana principal
# ======================
root = tk.Tk()
root.title("Gestor de Tareas")
root.geometry("800x400")
root.configure(bg="#f5f5f5")

# Frame de inputs
frame_inputs = tk.Frame(root, bg="#f0f8ff", pady=10)
frame_inputs.pack(side="top", fill="x")

tk.Label(frame_inputs, text="Tarea:", bg="#f0f8ff").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_tarea = tk.Entry(frame_inputs, width=20, bg="#fffacd")
entry_tarea.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_inputs, text="Fecha:", bg="#f0f8ff").grid(row=0, column=2, padx=5, pady=5, sticky="e")
entry_fecha = DateEntry(frame_inputs, width=12, date_pattern="dd/mm/yyyy")
entry_fecha.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_inputs, text="Hora:", bg="#f0f8ff").grid(row=0, column=4, padx=5, pady=5, sticky="e")
entry_hora = tk.Entry(frame_inputs, width=10, bg="#fffacd")
entry_hora.grid(row=0, column=5, padx=5, pady=5)

tk.Label(frame_inputs, text="Descripción:", bg="#f0f8ff").grid(row=0, column=6, padx=5, pady=5, sticky="e")
entry_desc = tk.Entry(frame_inputs, width=30, bg="#fffacd")
entry_desc.grid(row=0, column=7, padx=5, pady=5)

# Frame de lista
frame_lista = tk.Frame(root, bg="#e6e6fa", pady=10)
frame_lista.pack(fill="both", expand=True)

tree = ttk.Treeview(
    frame_lista,
    columns=("Tarea", "Fecha", "Hora", "Descripción", "Estado"),
    show="headings"
)
tree.pack(fill="both", expand=True, padx=10, pady=10)

for col in ("Tarea", "Fecha", "Hora", "Descripción", "Estado"):
    tree.heading(col, text=col)
    tree.column(col, width=120 if col != "Descripción" else 250)

# Vincular doble clic para abrir modal de edición
tree.bind("<Double-1>", lambda e: editar_evento())

# Frame de botones
frame_botones = tk.Frame(root, bg="#dcdcdc", pady=10)
frame_botones.pack(side="bottom", fill="x")

btn_agregar = tk.Button(frame_botones, text="Añadir Tarea", command=agregar_evento, bg="#98fb98")
btn_agregar.pack(side="left", padx=10)

btn_completar = tk.Button(frame_botones, text="Marcar como Completada", command=marcar_completada, bg="#90ee90")
btn_completar.pack(side="left", padx=10)

btn_editar = tk.Button(frame_botones, text="Editar Tarea", command=editar_evento, bg="#87ceeb")
btn_editar.pack(side="left", padx=10)

btn_eliminar = tk.Button(frame_botones, text="Eliminar Tarea", command=eliminar_evento, bg="#ff7f7f")
btn_eliminar.pack(side="left", padx=10)

btn_salir = tk.Button(frame_botones, text="Salir", command=salir, bg="#ffa500")
btn_salir.pack(side="right", padx=10)

# ======================
# Inicializar lista en memoria
# ======================
eventos_memoria = cargar_eventos()
refrescar_tree()

root.mainloop()
