from controlador.controlador_turnos import ControladorTurnos
from vista.interfaz import Interfaz


def main():
    """Punto de entrada del sistema."""
    controlador = ControladorTurnos()
    controlador.cargar_estado()

    app = Interfaz(controlador)
    app.ejecutar()


if __name__ == "__main__":
    main()