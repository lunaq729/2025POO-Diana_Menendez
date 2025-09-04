import json
import os

# Clases con métodos para serializar y deserializar JSON

class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.informacion = (titulo, autor)  # tupla inmutable
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"{self.informacion[0]} por {self.informacion[1]} (ISBN: {self.isbn})"

    def to_dict(self):
        return {
            "titulo": self.informacion[0],
            "autor": self.informacion[1],
            "categoria": self.categoria,
            "isbn": self.isbn,
        }

    @staticmethod
    def from_dict(data):
        return Libro(data["titulo"], data["autor"], data["categoria"], data["isbn"])

class Usuario:
    def __init__(self, nombre, user_id):
        self.nombre = nombre
        self.user_id = user_id
        self.libros_prestados = []

    def __str__(self):
        return f"{self.nombre} (ID: {self.user_id})"

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "user_id": self.user_id,
            "libros_prestados": [libro.to_dict() for libro in self.libros_prestados],
        }

    @staticmethod
    def from_dict(data):
        usuario = Usuario(data["nombre"], data["user_id"])
        usuario.libros_prestados = [Libro.from_dict(libro) for libro in data.get("libros_prestados", [])]
        return usuario


class Biblioteca:
    def __init__(self):
        self.libros = {}  # isbn: Libro
        self.usuarios = {}  # user_id: Usuario
        self.ids_usuarios = set()

    # Métodos para cargar y guardar en JSON

    def cargar_json(self):
        # Cargar libros
        if os.path.exists("libros.json"):
            with open("libros.json", "r", encoding="utf-8") as f:
                libros_data = json.load(f)
                for libro_dict in libros_data:
                    libro = Libro.from_dict(libro_dict)
                    self.libros[libro.isbn] = libro
        # Cargar usuarios
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r", encoding="utf-8") as f:
                usuarios_data = json.load(f)
                for usu_dict in usuarios_data:
                    usuario = Usuario.from_dict(usu_dict)
                    self.usuarios[usuario.user_id] = usuario
                    self.ids_usuarios.add(usuario.user_id)

    def guardar_json(self):
        # Guardar libros
        libros_data = [libro.to_dict() for libro in self.libros.values()]
        with open("libros.json", "w", encoding="utf-8") as f:
            json.dump(libros_data, f, indent=4, ensure_ascii=False)
        # Guardar usuarios
        usuarios_data = [usuario.to_dict() for usuario in self.usuarios.values()]
        with open("usuarios.json", "w", encoding="utf-8") as f:
            json.dump(usuarios_data, f, indent=4, ensure_ascii=False)

    # Funciones del sistema (agregar, quitar, prestar, devolver, etc.)

    def agregar_libro(self, libro):
        self.libros[libro.isbn] = libro
        print(f"Libro añadido: {libro.informacion[0]}")
        self.guardar_json()

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            del self.libros[isbn]
            print("Libro eliminado.")
            self.guardar_json()
        else:
            print("ISBN no encontrado.")

    def registrar_usuario(self, usuario):
        if usuario.user_id not in self.ids_usuarios:
            self.usuarios[usuario.user_id] = usuario
            self.ids_usuarios.add(usuario.user_id)
            print(f"Usuario registrado: {usuario.nombre}")
            self.guardar_json()
        else:
            print("ID de usuario ya existe.")

    def dar_baja_usuario(self, user_id):
        if user_id in self.ids_usuarios:
            del self.usuarios[user_id]
            self.ids_usuarios.remove(user_id)
            print("Usuario dado de baja.")
            self.guardar_json()
        else:
            print("Usuario no encontrado.")

    def prestar_libro(self, user_id, isbn):
        if user_id in self.usuarios and isbn in self.libros:
            usuario = self.usuarios[user_id]
            libro = self.libros[isbn]
            if libro not in usuario.libros_prestados:
                usuario.libros_prestados.append(libro)
                print(f"Libro '{libro.informacion[0]}' prestado a {usuario.nombre}.")
                self.guardar_json()
            else:
                print("El usuario ya tiene este libro prestado.")
        else:
            print("Usuario o libro no encontrado.")

    def devolver_libro(self, user_id, isbn):
        if user_id in self.usuarios:
            usuario = self.usuarios[user_id]
            antes = len(usuario.libros_prestados)
            usuario.libros_prestados = [libro for libro in usuario.libros_prestados if libro.isbn != isbn]
            despues = len(usuario.libros_prestados)
            if antes > despues:
                print("Libro devuelto.")
                self.guardar_json()
            else:
                print("El usuario no tenía ese libro prestado.")
        else:
            print("Usuario no encontrado.")

    def buscar_libros(self, tipo, valor):
        resultados = []
        valor = valor.lower()
        if tipo == "titulo":
            resultados = [l for l in self.libros.values() if l.informacion[0].lower() == valor]
        elif tipo == "autor":
            resultados = [l for l in self.libros.values() if l.informacion[1].lower() == valor]
        elif tipo == "categoria":
            resultados = [l for l in self.libros.values() if l.categoria.lower() == valor]
        if resultados:
            print(f"Resultados para {tipo} '{valor}':")
            for libro in resultados:
                print(f" - {libro}")
        else:
            print("No se encontraron libros.")

    def listar_libros_prestados(self, user_id):
        if user_id in self.usuarios:
            usuario = self.usuarios[user_id]
            if usuario.libros_prestados:
                print(f"Libros prestados a {usuario.nombre}:")
                for libro in usuario.libros_prestados:
                    print(f" - {libro}")
            else:
                print("No tiene libros prestados.")
        else:
            print("Usuario no encontrado.")

    def listar_usuarios(self):
        print("Usuarios registrados:")
        for usuario in self.usuarios.values():
            print(f" - {usuario}")

    def listar_libros_disponibles(self):
        print("Libros disponibles en la biblioteca:")
        for libro in self.libros.values():
            print(f" - {libro}")

    def listar_libros_prestados_todos(self):
        print("Libros prestados a todos los usuarios:")
        for usuario in self.usuarios.values():
            if usuario.libros_prestados:
                print(f"{usuario.nombre}:")
                for libro in usuario.libros_prestados:
                    print(f" - {libro}")

    def listar_todos_libros(self):
        print("Todos los libros en la biblioteca:")
        if not self.libros:
            print("No hay libros registrados.")
        for libro in self.libros.values():
            print(f"- {libro.informacion[0]} por {libro.informacion[1]} (ISBN: {libro.isbn})")

def menu():
    biblioteca = Biblioteca()
    biblioteca.cargar_json()  # cargar datos si existen al iniciar

    opciones = {
        "1": "Añadir libro",
        "2": "Quitar libro",
        "3": "Registrar usuario",
        "4": "Dar de baja usuario",
        "5": "Prestar libro",
        "6": "Devolver libro",
        "7": "Buscar libro por título",
        "8": "Buscar libro por autor",
        "9": "Buscar libro por categoría",
        "10": "Listar libros prestados de un usuario",
        "11": "Listar todos los usuarios",
        "12": "Listar libros disponibles",
        "13": "Listar todos los libros prestados",
        "14": "Listar todos los libros en general",
        "0": "Salir"
    }

    while True:
        print("\n--- Biblioteca General ---")
        for clave, desc in opciones.items():
            print(f"{clave}. {desc}")
        opcion = input("Elige una opción: ")

        if opcion == "0":
            print("Saliendo...")
            break
        elif opcion == "1":
            titulo = input("Título: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            libro = Libro(titulo, autor, categoria, isbn)
            biblioteca.agregar_libro(libro)
        elif opcion == "2":
            isbn = input("ISBN del libro a quitar: ")
            biblioteca.quitar_libro(isbn)
        elif opcion == "3":
            nombre = input("Nombre del usuario: ")
            user_id = input("ID único del usuario: ")
            usuario = Usuario(nombre, user_id)
            biblioteca.registrar_usuario(usuario)
        elif opcion == "4":
            user_id = input("ID del usuario a dar de baja: ")
            biblioteca.dar_baja_usuario(user_id)
        elif opcion == "5":
            user_id = input("ID del usuario: ")
            isbn = input("ISBN del libro a prestar: ")
            biblioteca.prestar_libro(user_id, isbn)
        elif opcion == "6":
            user_id = input("ID del usuario: ")
            isbn = input("ISBN del libro a devolver: ")
            biblioteca.devolver_libro(user_id, isbn)
        elif opcion == "7":
            titulo = input("Título a buscar: ")
            biblioteca.buscar_libros("titulo", titulo)
        elif opcion == "8":
            autor = input("Autor a buscar: ")
            biblioteca.buscar_libros("autor", autor)
        elif opcion == "9":
            categoria = input("Categoría a buscar: ")
            biblioteca.buscar_libros("categoria", categoria)
        elif opcion == "10":
            user_id = input("ID del usuario: ")
            biblioteca.listar_libros_prestados(user_id)
        elif opcion == "11":
            biblioteca.listar_usuarios()
        elif opcion == "12":
            biblioteca.listar_libros_disponibles()
        elif opcion == "13":
            biblioteca.listar_libros_prestados_todos()
        elif opcion == "14":
            biblioteca.listar_todos_libros()
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
