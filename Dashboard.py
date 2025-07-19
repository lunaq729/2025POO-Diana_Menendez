import subprocess
import os

# Función que ejecuta un archivo Python y muestra su salida y errores
def run_python_file(filepath):
    print(f"\n--- Ejecutando: {filepath} ---\n")
    try:
        # Ejecuta el archivo con el mismo intérprete de Python
        result = subprocess.run(
            [os.sys.executable, filepath],
            capture_output=True,
            text=True,
            check=True
        )
        print(">>> SALIDA:")
        print(result.stdout)
        if result.stderr:
            print(">>> ERRORES (si hay):")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        # Muestra detalles si el script tiene errores de ejecución
        print(f"Error al ejecutar {filepath}")
        print(f"Código de retorno: {e.returncode}")
        print("Salida:")
        print(e.stdout)
        print("Errores:")
        print(e.stderr)
    except FileNotFoundError:
        # Si no se encuentra el archivo
        print(f"Archivo no encontrado: {filepath}")
    print("-" * 60)


def main():
    # Ruta base del proyecto donde están los scripts
    base_dir = r"C:\Users\HOLA\PycharmProjects\2525-POO_Menendez-Diana"

    # Diccionario con las opciones del menú y rutas de archivos a ejecutar
    archivos = {
        '1': r"Parcial 01\Semana 2\Tarea 2.py",
        '2': r"Parcial 01\Semana 3\3 Tarea 3.py",
        '3': r"Parcial 01\Semana 3\Tarea 3.py",
        '4': r"Parcial 01\Semana 4\Caracteristica Poo.py",
        '5': r"Parcial 01\Semana 5\desarrollo de un programa en python.py",
        '6': r"Parcial 01\Semana 6\Clase, Definición de Objeto, Herencia, Encapsulación y Polimorfismo.py",
        '7': r"Parcial 01\Semana 7\Contructor y destructor.py",
        '0': "Salir"
    }

    # Menú principal interactivo
    while True:
        print("\n===== MENÚ DE EJECUCIÓN DE ARCHIVOS =====")
        for key, path in archivos.items():
            nombre = os.path.basename(path) if key != '0' else path
            print(f"{key} - {nombre}")

        # Solicita opción al usuario
        eleccion = input("\nSeleccione un archivo para ejecutar (o '0' para salir): ").strip()

        if eleccion == '0':
            print("Saliendo del programa.")
            break
        elif eleccion in archivos:
            ruta_completa = os.path.join(base_dir, archivos[eleccion])
            # Verifica que el archivo exista antes de ejecutarlo
            if os.path.exists(ruta_completa):
                run_python_file(ruta_completa)
            else:
                print(f"Archivo no encontrado: {ruta_completa}")
        else:
            print("Opción inválida. Intente de nuevo.")


# Punto de entrada del script
if __name__ == "__main__":
    main()