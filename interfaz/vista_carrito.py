import tkinter as tk
from tkinter import ttk, messagebox

from datos.cliente_dao import ClienteDAO
from datos.producto_dao import ProductoDAO
from datos.carrito_dao import CarritoDAO
from datos.item_carrito_dao import ItemCarritoDAO

from modelos.cliente import Cliente
from modelos.producto import Producto
from modelos.carrito import Carrito
from servicios.servicio_carrito import ServicioCarrito
from utilidades.formatos import dinero_clp

class VistaCarrito(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.carrito = None
        self._armar_ui()

    def _armar_ui(self):
        ttk.Label(self, text="Carrito (CRUD + cálculo)", font=("Segoe UI", 14, "bold")).pack(anchor="w")

        top = ttk.Frame(self)
        top.pack(fill="x", pady=10)

        # Seleccion de cliente
        self.var_cliente_id = tk.StringVar()
        ttk.Label(top, text="ID Cliente:").pack(side="left")
        ttk.Entry(top, textvariable=self.var_cliente_id, width=10).pack(side="left", padx=6)
        ttk.Button(top, text="Crear carrito para cliente", command=self.crear_carrito).pack(side="left", padx=6)

        self.lbl_carrito = ttk.Label(top, text="Carrito: (no creado)")
        self.lbl_carrito.pack(side="right")

        # Agregar items
        box = ttk.LabelFrame(self, text="Agregar producto", padding=10)
        box.pack(fill="x")

        self.var_codigo = tk.StringVar()
        self.var_cantidad = tk.StringVar(value="1")

        ttk.Label(box, text="Código producto").grid(row=0, column=0, sticky="w")
        ttk.Entry(box, textvariable=self.var_codigo).grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(box, text="Cantidad").grid(row=0, column=2, sticky="w")
        ttk.Entry(box, textvariable=self.var_cantidad, width=8).grid(row=0, column=3, sticky="w", padx=5)

        ttk.Button(box, text="Agregar", command=self.agregar_item).grid(row=0, column=4, padx=5)
        ttk.Button(box, text="Refrescar items", command=self.cargar_items).grid(row=0, column=5, padx=5)

        box.columnconfigure(1, weight=1)

        # Tabla items
        cols = ("ID_ITEM","CODIGO","NOMBRE","CANTIDAD","SUBTOTAL_ITEM")
        self.tabla = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c in cols:
            self.tabla.heading(c, text=c)
            self.tabla.column(c, width=160 if c!="NOMBRE" else 280)
        self.tabla.pack(fill="both", expand=True, pady=10)

        # Totales
        tot = ttk.Frame(self)
        tot.pack(fill="x")
        self.lbl_subtotal = ttk.Label(tot, text="Subtotal: $0")
        self.lbl_desc = ttk.Label(tot, text="Descuento: $0")
        self.lbl_total = ttk.Label(tot, text="Total: $0", font=("Segoe UI", 11, "bold"))
        self.lbl_total.pack(side="right")
        self.lbl_desc.pack(side="right", padx=12)
        self.lbl_subtotal.pack(side="right", padx=12)

        # Voucher
        ttk.Button(self, text="Mostrar voucher", command=self.mostrar_voucher).pack(anchor="e")

    def on_show(self):
        # nada especial
        pass

    def crear_carrito(self):
        try:
            id_cliente = int(self.var_cliente_id.get())
        except:
            messagebox.showerror("Error", "ID Cliente inválido.")
            return

        fila = ClienteDAO.buscar_por_id(id_cliente)
        if not fila:
            messagebox.showerror("Error", "Cliente no existe.")
            return

        idc, rut, nombre, email, hashpw, nivel = fila
        cliente = Cliente(idc, nombre, email, rut, nivel, hashpw)

        try:
            id_carrito = CarritoDAO.crear(id_cliente)
            self.carrito = Carrito(id_carrito=id_carrito, cliente=cliente)
            self.lbl_carrito.config(text=f"Carrito: {id_carrito} (cliente {id_cliente})")
            self.cargar_items()
            messagebox.showinfo("OK", f"Carrito creado: {id_carrito}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def agregar_item(self):
        if not self.carrito:
            messagebox.showerror("Error", "Primero crea un carrito para un cliente.")
            return

        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showerror("Validación", "Ingresa código de producto.")
            return

        try:
            cantidad = int(self.var_cantidad.get())
            if cantidad <= 0:
                raise ValueError()
        except:
            messagebox.showerror("Validación", "Cantidad inválida.")
            return

        fila = ProductoDAO.buscar_por_codigo(codigo)
        if not fila:
            messagebox.showerror("Error", "Producto no existe.")
            return

        cod, nombre, precio_neto, estado = fila
        if estado != "ACTIVO":
            messagebox.showerror("Error", "Producto está INACTIVO.")
            return

        producto = Producto(cod, nombre, float(precio_neto), estado)

        try:
            ServicioCarrito.agregar_item_y_guardar(self.carrito, producto, cantidad)
            self.cargar_items()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cargar_items(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)

        if not self.carrito:
            self.lbl_subtotal.config(text="Subtotal: $0")
            self.lbl_desc.config(text="Descuento: $0")
            self.lbl_total.config(text="Total: $0")
            return

        filas = ItemCarritoDAO.listar_por_carrito(self.carrito.id_carrito)
        for f in filas:
            # f: id_item, codigo, nombre, cantidad, subtotal_item
            id_item, cod, nom, cant, sub = f
            self.tabla.insert("", "end", values=(id_item, cod, nom, cant, float(sub)))

        # refrescar totales desde memoria
        self.carrito.calcular_total()
        self.lbl_subtotal.config(text=f"Subtotal: {dinero_clp(self.carrito.subtotal)}")
        self.lbl_desc.config(text=f"Descuento: {dinero_clp(self.carrito.descuento_aplicado)}")
        self.lbl_total.config(text=f"Total: {dinero_clp(self.carrito.total)}")

    def mostrar_voucher(self):
        if not self.carrito:
            messagebox.showerror("Error", "No hay carrito.")
            return
        self.carrito.calcular_total()
        messagebox.showinfo("Voucher", self.carrito.imprimir_voucher())
