from collections import deque
from datetime import datetime
from typing import Optional, List, Dict


class Turno:
    """Representa un turno del sistema."""

    def __init__(self, numero: str, nombre: str, prioritario: bool):
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        self.numero = numero
        self.nombre = nombre.strip()
        self.prioritario = prioritario
        self.hora = datetime.now().strftime("%H:%M:%S")

    def to_dict(self) -> Dict:
        """Convierte el turno a diccionario."""
        return {
            "numero": self.numero,
            "nombre": self.nombre,
            "prioritario": self.prioritario,
            "hora": self.hora,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Turno":
        """Crea un turno desde un diccionario."""
        turno = cls(data["numero"], data["nombre"], data["prioritario"])
        turno.hora = data["hora"]
        return turno

    def __str__(self) -> str:
        tipo = "P" if self.prioritario else "N"
        return f"{self.numero} - {self.nombre} ({tipo})"


class SistemaGestionTurnos:
    """Gestiona colas de turnos, prioridad e historial."""

    def __init__(self, nombre_servicio: str):
        self.nombre_servicio = nombre_servicio
        self._cola_normal = deque()
        self._cola_prioritaria = deque()
        self._historial = []

        self._contador_normal = 0
        self._contador_prioritario = 0

    def tomar_turno(self, nombre: str, prioritario: bool = False) -> str:
        """Asigna un turno."""
        if prioritario:
            self._contador_prioritario += 1
            numero = f"P-{self._contador_prioritario:03d}"
            turno = Turno(numero, nombre, True)
            self._cola_prioritaria.append(turno)
        else:
            self._contador_normal += 1
            numero = f"N-{self._contador_normal:03d}"
            turno = Turno(numero, nombre, False)
            self._cola_normal.append(turno)
        return None

    def atender_siguiente(self) -> Optional[Dict]:
        """Atiende el siguiente turno disponible."""
        turno = None

        if self._cola_prioritaria:
            turno = self._cola_prioritaria.popleft()
        elif self._cola_normal:
            turno = self._cola_normal.popleft()

        if turno:
            data = turno.to_dict()
            data["hora_atencion"] = datetime.now().strftime("%H:%M:%S")
            self._historial.append(data)
            return data

        return None

    def ver_cola(self) -> List[str]:
        """Devuelve lista de turnos pendientes."""
        resultado = []

        for t in self._cola_prioritaria:
            resultado.append(str(t))
        for t in self._cola_normal:
            resultado.append(str(t))

        return resultado

    def obtener_historial(self, n: int = 10) -> List[Dict]:
        """Devuelve últimos n atendidos."""
        return list(reversed(self._historial[-n:]))

    def exportar_estado(self) -> Dict:
        """Exporta estado completo."""
        return {
            "nombre_servicio": self.nombre_servicio,
            "contador_normal": self._contador_normal,
            "contador_prioritario": self._contador_prioritario,
            "cola_normal": [t.to_dict() for t in self._cola_normal],
            "cola_prioritaria": [t.to_dict() for t in self._cola_prioritaria],
            "historial": self._historial,
        }

    def importar_estado(self, data: Dict) -> None:
        """Restaura estado."""
        self.nombre_servicio = data["nombre_servicio"]
        self._contador_normal = data["contador_normal"]
        self._contador_prioritario = data["contador_prioritario"]

        self._cola_normal = deque(
            Turno.from_dict(t) for t in data["cola_normal"]
        )
        self._cola_prioritaria = deque(
            Turno.from_dict(t) for t in data["cola_prioritaria"]
        )
        self._historial = data["historial"]