import tkinter as tk
from tkinter import ttk, messagebox

from servicios.api_externa import ApiExterna

class VistaApi(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._armar_ui()

    def _armar_ui(self):
        ttk.Label(self, text="Consumo de API Externa (JSON)", font=("Segoe UI", 14, "bold")).pack(anchor="w")

        box = ttk.LabelFrame(self, text="Tipo de cambio USD -> CLP", padding=10)
        box.pack(fill="x", pady=10)

        self.lbl_estado = ttk.Label(box, text="Presiona 'Consultar' para traer datos dinámicos.")
        self.lbl_estado.pack(anchor="w")

        self.var_valor = tk.StringVar(value="(sin datos)")
        ttk.Label(box, textvariable=self.var_valor, font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=8)

        ttk.Button(box, text="Consultar API", command=self.consultar).pack(anchor="e")

        info = ttk.Label(self, text="Se procesa la respuesta JSON y se muestra en pantalla.", foreground="gray")
        info.pack(anchor="w")

    def on_show(self):
        # opcional: no auto-consultar para no depender de internet siempre
        pass

    def consultar(self):
        try:
            tasa = ApiExterna.obtener_tipo_cambio_usd_a_clp()
            self.var_valor.set(f"1 USD = {tasa:,.2f} CLP")
            self.lbl_estado.config(text="OK: datos recibidos y procesados desde JSON.")
        except Exception as e:
            messagebox.showerror("API", str(e))
            self.lbl_estado.config(text="Error al consultar API.")
