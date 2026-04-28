import tkinter as tk
from tkinter import messagebox


class Interfaz:
    """Interfaz gráfica del sistema de turnos."""

    def __init__(self, controlador):
        self.ctrl = controlador

        self.root = tk.Tk()
        self.root.title("Sistema de Turnos")
        self.root.geometry("700x500")

        self._crear_layout()
        self._actualizar()

    def _crear_layout(self):
        """Define la estructura principal de la interfaz."""

        # ===== FRAME SUPERIOR (entrada + botones) =====
        frame_top = tk.Frame(self.root)
        frame_top.pack(fill="x", padx=10, pady=10)

        self.entry_nombre = tk.Entry(frame_top, width=30)
        self.entry_nombre.grid(row=0, column=0, padx=5)

        tk.Button(
            frame_top, text="Turno Normal",
            command=self._turno_normal
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            frame_top, text="Turno Prioritario",
            command=self._turno_prioritario
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            frame_top, text="Atender",
            command=self._atender
        ).grid(row=0, column=3, padx=5)

        # ===== FRAME INFERIOR (cola + historial) =====
        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(fill="both", expand=True, padx=10, pady=10)

        frame_bottom.grid_columnconfigure(0, weight=1)
        frame_bottom.grid_columnconfigure(1, weight=1)
        frame_bottom.grid_rowconfigure(0, weight=1)

        # ===== COLA =====
        frame_cola = tk.Frame(frame_bottom)
        frame_cola.grid(row=0, column=0, sticky="nsew", padx=5)

        tk.Label(frame_cola, text="Cola", font=("Arial", 12, "bold")).pack()

        self.lista = tk.Listbox(frame_cola)
        self.lista.pack(fill="both", expand=True)

        # ===== HISTORIAL =====
        frame_hist = tk.Frame(frame_bottom)
        frame_hist.grid(row=0, column=1, sticky="nsew", padx=5)

        tk.Label(frame_hist, text="Historial", font=("Arial", 12, "bold")).pack()

        self.historial = tk.Listbox(frame_hist)
        self.historial.pack(fill="both", expand=True)

    def _turno_normal(self):
        self._crear_turno(False)

    def _turno_prioritario(self):
        self._crear_turno(True)

    def _crear_turno(self, prioritario):
        nombre = self.entry_nombre.get().strip()

        if not nombre:
            messagebox.showwarning("Error", "Nombre vacío")
            return

        try:
            self.ctrl.tomar_turno(nombre, prioritario)
            self.ctrl.guardar_estado()

            self.entry_nombre.delete(0, tk.END)
            self._actualizar()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _atender(self):
        turno = self.ctrl.atender()

        if not turno:
            messagebox.showinfo("Info", "No hay turnos")
        else:
            self.ctrl.guardar_estado()

        self._actualizar()

    def _actualizar(self):
        """Refresca cola e historial."""

        self.lista.delete(0, tk.END)
        for t in self.ctrl.ver_cola():
            self.lista.insert(tk.END, t)

        self.historial.delete(0, tk.END)
        for t in self.ctrl.ver_historial():
            self.historial.insert(
                tk.END, f"{t['numero']} - {t['nombre']}"
            )

    def ejecutar(self):
        """Inicia la aplicación."""
        self.root.mainloop()