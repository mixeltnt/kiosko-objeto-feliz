from modelos.producto import Producto

class ItemCarrito:
    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = int(cantidad)
        self.subtotal = 0.0

    def calcular_subtotal(self) -> float:
        self.subtotal = round(self.producto.calcular_precio_iva() * self.cantidad, 2)
        return self.subtotal
