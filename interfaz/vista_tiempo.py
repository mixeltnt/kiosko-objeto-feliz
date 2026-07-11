import tkinter as tk
from tkinter import ttk, messagebox

from servicios.api_tiempo import ApiTiempo

class VistaTiempo(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._armar_ui()

    def _armar_ui(self):
        ttk.Label(
            self,
            text="API del Clima (Tiempo actual)",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w")

        box = ttk.LabelFrame(self, text="Clima en Santiago de Chile", padding=10)
        box.pack(fill="x", pady=10)

        self.lbl_estado = ttk.Label(box, text="Presiona 'Consultar' para obtener el clima.")
        self.lbl_estado.pack(anchor="w")

        self.var_resultado = tk.StringVar(value="(sin datos)")
        ttk.Label(
            box,
            textvariable=self.var_resultado,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=10)

        ttk.Button(box, text="Consultar clima", command=self.consultar).pack(anchor="e")

        ttk.Label(
            self,
            text="Datos obtenidos desde API externa en formato JSON.",
            foreground="gray"
        ).pack(anchor="w")

    def consultar(self):
        try:
            clima = ApiTiempo.obtener_clima_santiago()

            texto = (
                f"🌡 Temperatura: {clima['temperatura']} °C\n"
                f"💨 Viento: {clima['viento']} km/h\n"
                f"🧭 Dirección viento: {clima['direccion_viento']}°\n"
                f"🕒 Hora medición: {clima['hora']}"
            )

            self.var_resultado.set(texto)
            self.lbl_estado.config(text="OK: clima obtenido desde API.")
        except Exception as e:
            messagebox.showerror("Clima", str(e))
            self.lbl_estado.config(text="Error al consultar API del clima.")
