from typing import List
from modelos.item_carrito import ItemCarrito
from modelos.cliente import Cliente

class Carrito:
    def __init__(self, id_carrito: int = None, cliente: Cliente = None):
        self.id_carrito = id_carrito
        self.cliente = cliente
        self.items: List[ItemCarrito] = []
        self.subtotal = 0.0
        self.descuento_aplicado = 0.0
        self.total = 0.0

    def agregar_item(self, item: ItemCarrito):
        self.items.append(item)

    def calcular_subtotales(self) -> float:
        self.subtotal = round(sum(i.calcular_subtotal() for i in self.items), 2)
        return self.subtotal

    def calcular_total(self) -> float:
        self.calcular_subtotales()
        self.descuento_aplicado = self.cliente.aplicar_descuento(self.subtotal) if self.cliente else 0.0
        self.total = round(self.subtotal - self.descuento_aplicado, 2)
        return self.total

    def imprimir_voucher(self) -> str:
        lineas = ["=== VOUCHER ==="]
        if self.cliente:
            lineas.append(f"Cliente: {self.cliente.nombre} ({self.cliente.nivel})")
            lineas.append(f"RUT: {self.cliente.rut}")
        lineas.append("")
        for it in self.items:
            lineas.append(f"- {it.producto.nombre} x{it.cantidad} = ${it.calcular_subtotal():.0f}")
        lineas.append("")
        lineas.append(f"Subtotal: ${self.subtotal:.0f}")
        lineas.append(f"Descuento: ${self.descuento_aplicado:.0f}")
        lineas.append(f"TOTAL: ${self.total:.0f}")
        return "\n".join(lineas)
