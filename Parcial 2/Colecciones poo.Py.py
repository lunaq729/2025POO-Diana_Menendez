import json


class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self._id_producto = id_producto
        self._nombre = nombre  # aquí puede ser nombre de prenda, por ejemplo "Camisa azul"
        self._cantidad = cantidad
        self._precio = precio

    @property
    def id_producto(self):
        return self._id_producto

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad):
        if nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa.")

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio >= 0:
            self._precio = nuevo_precio
        else:
            raise ValueError("El precio no puede ser negativo.")

    def to_dict(self):
        return {
            "id_producto": self._id_producto,
            "nombre": self._nombre,
            "cantidad": self._cantidad,
            "precio": self._precio
        }

    def __str__(self):
        return f"{self._id_producto:<10} {self._nombre:<20} {self._cantidad:<10} ${self._precio:<10.2f}"


class Inventario:
    def __init__(self):
        self.productos = {}

    def añadir_producto(self, producto):
        if producto.id_producto in self.productos:
            raise KeyError("Ya existe un producto con este ID.")
        self.productos[producto.id_producto] = producto

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
        else:
            raise KeyError("Producto no encontrado.")

    def actualizar_cantidad(self, id_producto, nueva_cantidad):
        if id_producto in self.productos:
            self.productos[id_producto].cantidad = nueva_cantidad
        else:
            raise KeyError("Producto no encontrado.")

    def actualizar_precio(self, id_producto, nuevo_precio):
        if id_producto in self.productos:
            self.productos[id_producto].precio = nuevo_precio
        else:
            raise KeyError("Producto no encontrado.")

    def buscar_producto_por_nombre(self, nombre):
        encontrados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        if encontrados:
            print(f"\nProductos encontrados con '{nombre}':")
            print(f"{'ID':<10} {'Nombre':<20} {'Cantidad':<10} {'Precio':<10}")
            print("-" * 55)
            for p in encontrados:
                print(p)
        else:
            print("No se encontraron productos con ese nombre.")

    def mostrar_todos_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print(f"\n{'ID':<10} {'Nombre':<20} {'Cantidad':<10} {'Precio':<10}")
            print("-" * 55)
            for producto in self.productos.values():
                print(producto)

    def guardar_en_archivo(self, nombre_archivo):
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump({pid: p.to_dict() for pid, p in self.productos.items()},
                      f, indent=4, ensure_ascii=False)

    def cargar_desde_archivo(self, nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
                self.productos = {pid: Producto(**info) for pid, info in datos.items()}
        except FileNotFoundError:
            print("Archivo no encontrado. Se creará uno nuevo al guardar.")


def menu():
    inventario = Inventario()
    archivo = "inventario_ropa.json"  # Archivo modificado para ropa
    inventario.cargar_desde_archivo(archivo)

    while True:
        print("\n--- Menú de Gestión de Inventario de Ropa ---")
        print("1. Añadir prenda")
        print("2. Eliminar prenda")
        print("3. Actualizar cantidad")
        print("4. Actualizar precio")
        print("5. Buscar prenda por nombre")
        print("6. Mostrar todas las prendas")
        print("7. Guardar y salir")
        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                id_producto = input("ID de la prenda (único): ").strip()
                nombre = input("Nombre de la prenda: ").strip()
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.añadir_producto(producto)
                print("Prenda añadida exitosamente.")

            elif opcion == "2":
                id_producto = input("ID de la prenda a eliminar: ").strip()
                inventario.eliminar_producto(id_producto)
                print("Prenda eliminada.")

            elif opcion == "3":
                id_producto = input("ID de la prenda a actualizar cantidad: ").strip()
                nueva_cantidad = int(input("Nueva cantidad: "))
                inventario.actualizar_cantidad(id_producto, nueva_cantidad)
                print("Cantidad actualizada.")

            elif opcion == "4":
                id_producto = input("ID de la prenda a actualizar precio: ").strip()
                nuevo_precio = float(input("Nuevo precio: "))
                inventario.actualizar_precio(id_producto, nuevo_precio)
                print("Precio actualizado.")

            elif opcion == "5":
                nombre = input("Nombre o parte del nombre para buscar: ").strip()
                inventario.buscar_producto_por_nombre(nombre)

            elif opcion == "6":
                inventario.mostrar_todos_productos()

            elif opcion == "7":
                inventario.guardar_en_archivo(archivo)
                print("Inventario guardado. Saliendo...")
                break

            else:
                print("Opción no válida. Intente de nuevo.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu()
