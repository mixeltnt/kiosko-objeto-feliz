import tkinter as tk
from tkinter import ttk, messagebox

from datos.cliente_dao import ClienteDAO
from utilidades.validaciones import validar_correo, validar_rut, limpiar_rut
from utilidades.seguridad import hash_password

class VistaClientes(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._armar_ui()

    def _armar_ui(self):
        ttk.Label(self, text="Clientes (CRUD)", font=("Segoe UI", 14, "bold")).pack(anchor="w")

        form = ttk.LabelFrame(self, text="Formulario", padding=10)
        form.pack(fill="x", pady=10)

        self.var_rut = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_nivel = tk.StringVar(value="NORMAL")
        self.var_password = tk.StringVar()

        # Grid form
        for i in range(4):
            form.columnconfigure(i, weight=1)

        ttk.Label(form, text="RUT").grid(row=0, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.var_rut).grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(form, text="Nombre").grid(row=0, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.var_nombre).grid(row=0, column=3, sticky="ew", padx=5)

        ttk.Label(form, text="Email").grid(row=1, column=0, sticky="w", pady=(8,0))
        ttk.Entry(form, textvariable=self.var_email).grid(row=1, column=1, sticky="ew", padx=5, pady=(8,0))

        ttk.Label(form, text="Nivel (NORMAL/ESTUDIANTE)").grid(row=1, column=2, sticky="w", pady=(8,0))
        ttk.Entry(form, textvariable=self.var_nivel).grid(row=1, column=3, sticky="ew", padx=5, pady=(8,0))

        ttk.Label(form, text="Password (solo al crear)").grid(row=2, column=0, sticky="w", pady=(8,0))
        ttk.Entry(form, textvariable=self.var_password, show="*").grid(row=2, column=1, sticky="ew", padx=5, pady=(8,0))

        botones = ttk.Frame(form)
        botones.grid(row=3, column=0, columnspan=4, sticky="e", pady=(10,0))

        ttk.Button(botones, text="Crear", command=self.crear).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar (por ID)", command=self.actualizar).pack(side="left", padx=4)
        ttk.Button(botones, text="Eliminar (por ID)", command=self.eliminar).pack(side="left", padx=4)

        # Tabla
        ttk.Label(self, text="Listado").pack(anchor="w")
        self.var_id_accion = tk.StringVar()
        fila_id = ttk.Frame(self)
        fila_id.pack(fill="x", pady=(0,6))
        ttk.Label(fila_id, text="ID para actualizar/eliminar:").pack(side="left")
        ttk.Entry(fila_id, textvariable=self.var_id_accion, width=10).pack(side="left", padx=6)
        ttk.Button(fila_id, text="Refrescar", command=self.cargar).pack(side="right")

        cols = ("ID", "RUT", "NOMBRE", "EMAIL", "NIVEL", "FECHA")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=140 if c != "ID" else 60)
        self.tabla.pack(fill="both", expand=True)

    def on_show(self):
        self.cargar()

    def cargar(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for fila in ClienteDAO.listar():
            self.tabla.insert("", "end", values=fila)

    def crear(self):
        rut = limpiar_rut(self.var_rut.get())
        nombre = self.var_nombre.get().strip()
        email = self.var_email.get().strip()
        nivel = self.var_nivel.get().strip().upper()
        password = self.var_password.get()

        if not validar_rut(rut):
            messagebox.showerror("Validación", "RUT inválido.")
            return
        if not validar_correo(email):
            messagebox.showerror("Validación", "Correo inválido.")
            return
        if len(password) < 6:
            messagebox.showerror("Validación", "La password debe tener al menos 6 caracteres.")
            return
        if nivel not in ("NORMAL", "ESTUDIANTE"):
            messagebox.showerror("Validación", "Nivel debe ser NORMAL o ESTUDIANTE.")
            return

        try:
            idc = ClienteDAO.crear(rut, nombre, email, hash_password(password), nivel)
            messagebox.showinfo("OK", f"Cliente creado con ID {idc}.")
            self.var_password.set("")
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        try:
            idc = int(self.var_id_accion.get())
        except:
            messagebox.showerror("Error", "Ingresa un ID válido.")
            return

        rut = limpiar_rut(self.var_rut.get())
        nombre = self.var_nombre.get().strip()
        email = self.var_email.get().strip()
        nivel = self.var_nivel.get().strip().upper()

        if rut and not validar_rut(rut):
            messagebox.showerror("Validación", "RUT inválido.")
            return
        if email and not validar_correo(email):
            messagebox.showerror("Validación", "Correo inválido.")
            return

        try:
            ClienteDAO.actualizar(idc, rut, nombre, email, nivel)
            messagebox.showinfo("OK", "Cliente actualizado.")
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        try:
            idc = int(self.var_id_accion.get())
        except:
            messagebox.showerror("Error", "Ingresa un ID válido.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            return

        try:
            ClienteDAO.eliminar(idc)
            messagebox.showinfo("OK", "Cliente eliminado.")
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))
