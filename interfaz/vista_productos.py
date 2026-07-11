import tkinter as tk
from tkinter import ttk, messagebox

from datos.producto_dao import ProductoDAO

class VistaProductos(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._armar_ui()

    def _armar_ui(self):
        ttk.Label(self, text="Productos (CRUD)", font=("Segoe UI", 14, "bold")).pack(anchor="w")

        form = ttk.LabelFrame(self, text="Formulario", padding=10)
        form.pack(fill="x", pady=10)
        for i in range(4):
            form.columnconfigure(i, weight=1)

        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_estado = tk.StringVar(value="ACTIVO")

        ttk.Label(form, text="Código").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_codigo).grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(form, text="Nombre").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.var_nombre).grid(row=0, column=3, sticky="ew", padx=5)

        ttk.Label(form, text="Precio neto").grid(row=1, column=0, sticky="w", pady=(8,0))
        ttk.Entry(form, textvariable=self.var_precio).grid(row=1, column=1, sticky="ew", padx=5, pady=(8,0))

        ttk.Label(form, text="Estado (ACTIVO/INACTIVO)").grid(row=1, column=2, sticky="w", pady=(8,0))
        ttk.Entry(form, textvariable=self.var_estado).grid(row=1, column=3, sticky="ew", padx=5, pady=(8,0))

        botones = ttk.Frame(form)
        botones.grid(row=2, column=0, columnspan=4, sticky="e", pady=(10,0))
        ttk.Button(botones, text="Crear", command=self.crear).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar", command=self.actualizar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar", command=self.eliminar).pack(side="left", padx=4)

        ttk.Label(self, text="Listado").pack(anchor="w")
        ttk.Button(self, text="Refrescar", command=self.cargar).pack(anchor="e", pady=(0,6))

        cols = ("CODIGO","NOMBRE","PRECIO_NETO","ESTADO")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=12)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=200 if c!="CODIGO" else 100)
        self.tabla.pack(fill="both", expand=True)

    def on_show(self):
        self.cargar()

    def cargar(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for fila in ProductoDAO.listar():
            self.tabla.insert("", "end", values=fila)

    def _leer_precio(self):
        try:
            return float(self.var_precio.get())
        except:
            raise ValueError("Precio neto inválido.")

    def crear(self):
        codigo = self.var_codigo.get().strip()
        nombre = self.var_nombre.get().strip()
        estado = self.var_estado.get().strip().upper()
        try:
            precio = self._leer_precio()
        except Exception as e:
            messagebox.showerror("Validación", str(e)); return
        if not codigo or not nombre:
            messagebox.showerror("Validación", "Código y nombre son obligatorios."); return
        if estado not in ("ACTIVO","INACTIVO"):
            messagebox.showerror("Validación", "Estado debe ser ACTIVO o INACTIVO."); return
        try:
            ProductoDAO.crear(codigo, nombre, precio, estado)
            messagebox.showinfo("OK","Producto creado.")
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        codigo = self.var_codigo.get().strip()
        nombre = self.var_nombre.get().strip()
        estado = self.var_estado.get().strip().upper()
        try:
            precio = self._leer_precio()
        except Exception as e:
            messagebox.showerror("Validación", str(e)); return
        if not codigo:
            messagebox.showerror("Validación", "Código es obligatorio para actualizar."); return
        try:
            ProductoDAO.actualizar(codigo, nombre, precio, estado)
            messagebox.showinfo("OK","Producto actualizado.")
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Validación", "Código es obligatorio para eliminar."); return
        if not messagebox.askyesno("Confirmar", f"¿Eliminar producto {codigo}?"):
            return
        try:
            ProductoDAO.eliminar(codigo)
            messagebox.showinfo("OK","Producto eliminado.")
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))
