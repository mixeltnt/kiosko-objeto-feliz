import tkinter as tk
from tkinter import ttk

from interfaz.vista_clientes import VistaClientes
from interfaz.vista_productos import VistaProductos
from interfaz.vista_carrito import VistaCarrito
from interfaz.vista_api import VistaApi
from interfaz.vista_tiempo import VistaTiempo


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kiosko Objeto Feliz - Tkinter (simulación web)")
        self.geometry("1020x620")
        self.minsize(980, 580)

        # Contenedor principal
        contenedor = ttk.Frame(self)
        contenedor.pack(fill="both", expand=True)

        contenedor.columnconfigure(0, weight=0)
        contenedor.columnconfigure(1, weight=1)
        contenedor.rowconfigure(0, weight=1)

        # ===== Menu lateral=====
        self.menu = ttk.Frame(contenedor, padding=10)
        self.menu.grid(row=0, column=0, sticky="ns")

        ttk.Label(
            self.menu,
            text="MENÚ",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=(0, 10))

        ttk.Button(self.menu, text="Clientes",
                   command=lambda: self.mostrar("clientes")).pack(fill="x", pady=5)

        ttk.Button(self.menu, text="Productos",
                   command=lambda: self.mostrar("productos")).pack(fill="x", pady=5)

        ttk.Button(self.menu, text="Carrito",
                   command=lambda: self.mostrar("carrito")).pack(fill="x", pady=5)

        ttk.Button(self.menu, text="API (USD/CLP)",
                   command=lambda: self.mostrar("api")).pack(fill="x", pady=5)

        ttk.Button(self.menu, text="Clima",
                   command=lambda: self.mostrar("clima")).pack(fill="x", pady=5)

        ttk.Separator(self.menu, orient="horizontal").pack(fill="x", pady=12)

        ttk.Label(
            self.menu,
            text="Tip: usa el panel derecho\npara CRUD y demo.",
            justify="left"
        ).pack(anchor="w")

        # ===== Panel derecho =====
        self.panel = ttk.Frame(contenedor, padding=10)
        self.panel.grid(row=0, column=1, sticky="nsew")
        self.panel.rowconfigure(0, weight=1)
        self.panel.columnconfigure(0, weight=1)

        # ===== Vistas =====
        self.vistas = {
            "clientes": VistaClientes(self.panel),
            "productos": VistaProductos(self.panel),
            "carrito": VistaCarrito(self.panel),
            "api": VistaApi(self.panel),
            "clima": VistaTiempo(self.panel),
        }

        for vista in self.vistas.values():
            vista.grid(row=0, column=0, sticky="nsew")

        self.mostrar("clientes")

    def mostrar(self, clave: str):
        vista = self.vistas.get(clave)
        if vista:
            vista.tkraise()
            vista.on_show()
