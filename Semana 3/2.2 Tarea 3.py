# Clase base
class ClimaSemanal:
    def __init__(self):
        self.__temperaturas = []  # Encapsulado

    def ingresar_temperaturas(self):
        print("Ingresa la temperatura de cada día de la semana:")
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        for dia in dias:
            temp = float(input(f"{dia}: "))
            self.__temperaturas.append(temp)

    def calcular_promedio(self):
        return sum(self.__temperaturas) / len(self.__temperaturas)

    def mostrar_resultado(self):
        promedio = self.calcular_promedio()
        print(f"\nEl promedio semanal es: {promedio:.2f}°C")


# Clase hija usando herencia y polimorfismo
class ClimaExtendido(ClimaSemanal):
    def mostrar_resultado(self):
        promedio = self.calcular_promedio()
        if promedio > 30:
            estado = "Caluroso"
        elif promedio >= 15:
            estado = "Templado"
        else:
            estado = "Frío"
        print(f"\nPromedio: {promedio:.2f}°C — Clima {estado}")

# Programa principal
def main():
    clima = ClimaExtendido()
    clima.ingresar_temperaturas()
    clima.mostrar_resultado()

 main()
