class Habitacion:
    def __init__(self, numero, tipo, precio):
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.disponible = True

    def reservar(self):
        if self.disponible:
            self.disponible = False
            return True
        return False

    def liberar(self):
        self.disponible = True


class Cliente:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula


class Reserva:
    def __init__(self, cliente, habitacion, dias):
        self.cliente = cliente
        self.habitacion = habitacion
        self.dias = dias
        self.total = self.habitacion.precio * self.dias

    def mostrar_resumen(self):
        print("\n🔒 RESERVA CONFIRMADA:")
        print(f"Cliente: {self.cliente.nombre} - Cédula: {self.cliente.cedula}")
        print(f"Habitación: {self.habitacion.numero} ({self.habitacion.tipo})")
        print(f"Días: {self.dias}")
        print(f"Total a pagar: ${self.total:.2f}")


# Programa principal
def main():
    # Crear algunas habitaciones
    habitaciones = [
        Habitacion(101, "Individual", 50),
        Habitacion(102, "Doble", 80),
        Habitacion(201, "Suite", 120)
    ]

    print("=== Bienvenido al sistema de reservas del Hotel POO ===")

    nombre = input("Diana : ")
    cedula = input("1310404395: ")
    cliente = Cliente(nombre, cedula)

    print("\nHabitaciones disponibles:")
    for h in habitaciones:
        estado = "Disponible" if h.disponible else "Ocupada"
        print(f"Habitación {h.numero} - Tipo: {h.tipo} - Precio: ${h.precio} por noche - {estado}")

    seleccion = int(input("Ingrese el número de habitación que desea reservar: "))
    dias = int(input("¿Cuántos días desea quedarse?: "))

    # Buscar habitación
    habitacion_elegida = None
    for h in habitaciones:
        if h.numero == seleccion:
            habitacion_elegida = h
            break

    if habitacion_elegida and habitacion_elegida.reservar():
        reserva = Reserva(cliente, habitacion_elegida, dias)
        reserva.mostrar_resumen()
    else:
        print("❌ Lo sentimos, la habitación no está disponible o no existe.")

main()
