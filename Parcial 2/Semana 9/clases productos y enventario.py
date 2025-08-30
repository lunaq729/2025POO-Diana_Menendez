# ==========================
# Clase Producto
# ==========================
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.__id = id_producto
        self.__nombre = nombre
        self.__cantidad = cantidad
        self.__precio = precio

    # Getters
    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_cantidad(self):
        return self.__cantidad

    def get_precio(self):
        return self.__precio

    # Setters
    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_cantidad(self, cantidad):
        self.__cantidad = cantidad

    def set_precio(self, precio):
        self.__precio = precio

    def __str__(self):
        return f"ID: {self.__id} | Nombre: {self.__nombre} | Cantidad: {self.__cantidad} | Precio: ${self.__precio:.2f}"


# ==========================
# Clase Inventario
# ==========================
class Inventario:
    def __init__(self):
        self.productos = []

    def añadir_producto(self, producto):
        if any(p.get_id() == producto.get_id() for p in self.productos):
            print("⚠️ Error: El ID ya existe. No se puede añadir el producto.")
            return
        self.productos.append(producto)
        print("✅ Producto añadido correctamente.")

    def eliminar_producto(self, id_producto):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
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
