import json
import os
from modelo.sistema_turnos import SistemaGestionTurnos


class ControladorTurnos:
    """Controlador del sistema de turnos."""

    def __init__(self):
        self.sistema = SistemaGestionTurnos("Sistema de Turnos")
        self.ruta = os.path.join("datos", "estado.json")

    def tomar_turno(self, nombre: str, prioritario: bool = False) -> str:
        return self.sistema.tomar_turno(nombre, prioritario)

    def atender(self):
        return self.sistema.atender_siguiente()

    def ver_cola(self):
        return self.sistema.ver_cola()

    def ver_historial(self):
        return self.sistema.obtener_historial()

    def guardar_estado(self):
        os.makedirs("datos", exist_ok=True)

        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(self.sistema.exportar_estado(), f, indent=2)

    def cargar_estado(self):
        if not os.path.exists(self.ruta):
            return

        with open(self.ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.sistema.importar_estado(data)