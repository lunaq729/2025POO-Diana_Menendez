import json
import os

# ==========================
# Clase Producto
# ==========================
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.__id = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    def get_precio(self):
        return self.__precio

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad

    def set_precio(self, precio):
        self.__precio = precio

    def __str__(self):
        return f"ID: {self.__id} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"

    def to_dict(self):
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "cantidad": self.__cantidad,
            "precio": self.__precio
        }


# ==========================
# Clase Inventario
# ==========================
class Inventario:
    def __init__(self, archivo="inventario.json"):
        self.archivo = archivo
        self.productos = []
        self.cargar_inventario()

    def cargar_inventario(self):
        """Carga el inventario desde el archivo JSON, o lo crea si no existe"""
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        producto = Producto(item["id"], item["nombre"], item["cantidad"], item["precio"])
                        self.productos.append(producto)
                print("📂 Inventario cargado exitosamente.")
            else:
                self.crear_inventario_inicial()
        except (json.JSONDecodeError, PermissionError) as e:
            print(f"⚠️ Error al leer el archivo: {e}")

    def crear_inventario_inicial(self):
        """Crea un inventario inicial con productos de papelería"""
        inventario_inicial = [
            {"id": "P001", "nombre": "Cuaderno universitario", "cantidad": 50, "precio": 2.50},
            {"id": "P002", "nombre": "Lápiz HB", "cantidad": 200, "precio": 0.25},
            {"id": "P003", "nombre": "Borrador blanco", "cantidad": 100, "precio": 0.30},
            {"id": "P004", "nombre": "Marcador negro", "cantidad": 75, "precio": 1.10},
            {"id": "P005", "nombre": "Resma de papel A4", "cantidad": 20, "precio": 4.80},
            {"id": "P006", "nombre": "Tijeras escolares", "cantidad": 40, "precio": 1.75},
            {"id": "P007", "nombre": "Regla plástica 30cm", "cantidad": 60, "precio": 0.90},
            {"id": "P008", "nombre": "Cartulina blanca", "cantidad": 150, "precio": 0.50},
            {"id": "P009", "nombre": "Bolígrafo azul", "cantidad": 300, "precio": 0.35},
            {"id": "P010", "nombre": "Pegamento en barra", "cantidad": 80, "precio": 1.20}
        ]
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(inventario_inicial, f, indent=4, ensure_ascii=False)
        for item in inventario_inicial:
            self.productos.append(Producto(item["id"], item["nombre"], item["cantidad"], item["precio"]))
        print("📂 Inventario inicial creado con productos de papelería.")

    def guardar_inventario(self):
        """Guarda el inventario actual en el archivo JSON"""
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([p.to_dict() for p in self.productos], f, indent=4, ensure_ascii=False)
            print("💾 Cambios guardados en el archivo.")
        except PermissionError:
            print("⚠️ Error: No se tiene permiso para escribir en el archivo.")

    def añadir_producto(self, producto):
        if any(p.get_id() == producto.get_id() for p in self.productos):
            print("⚠️ Error: El ID ya existe. No se puede añadir el producto.")
            return
        self.productos.append(producto)
        self.guardar_inventario()
        print("✅ Producto añadido correctamente.")

    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                self.guardar_inventario()
                print("🗑️ Producto eliminado correctamente.")
                return
        print("⚠️ No se encontró un producto con ese ID.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if cantidad is not None:
                    p.set_cantidad(cantidad)
                if precio is not None:
                    p.set_precio(precio)
                self.guardar_inventario()
                print("🔄 Producto actualizado correctamente.")
                return
        print("⚠️ No se encontró un producto con ese ID.")

    def buscar_producto(self, nombre):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print("\n🔍 Resultados de búsqueda:")
            for p in resultados:
                print(p)
        else:
            print("⚠️ No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        if not self.productos:
            print("📦 El inventario está vacío.")
            return
        print("\n📋 Lista de productos en inventario:")
        for p in self.productos:
            print(p)


# ==========================
# Interfaz de usuario
# ==========================
def menu():
    inventario = Inventario()

    while True:
        print("\n===== SISTEMA DE GESTIÓN DE INVENTARIO =====")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_prod = input("Ingrese ID del producto: ")
                nombre = input("Ingrese nombre: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                nuevo = Producto(id_prod, nombre, cantidad, precio)
                inventario.añadir_producto(nuevo)
            except ValueError:
                print("⚠️ Error: Datos inválidos.")

        elif opcion == "2":
            id_prod = input("Ingrese el ID del producto a eliminar: ")
            inventario.eliminar_producto(id_prod)

        elif opcion == "3":
            id_prod = input("Ingrese el ID del producto a actualizar: ")
            try:
                cantidad = input("Nueva cantidad (dejar vacío para no cambiar): ")
                precio = input("Nuevo precio (dejar vacío para no cambiar): ")

                cantidad = int(cantidad) if cantidad else None
                precio = float(precio) if precio else None
                inventario.actualizar_producto(id_prod, cantidad, precio)
            except ValueError:
                print("⚠️ Error: Datos inválidos.")

        elif opcion == "4":
            nombre = input("Ingrese el nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_todos()

        elif opcion == "6":
            print("👋 Saliendo del sistema...")
            break

        else:
            print("⚠️ Opción no válida.")


# ==========================
# Ejecución del programa
# ==========================
if __name__ == "__main__":
    menu()


