from modelos.carrito import Carrito
from modelos.item_carrito import ItemCarrito
from modelos.producto import Producto
from datos.item_carrito_dao import ItemCarritoDAO
from datos.carrito_dao import CarritoDAO

class ServicioCarrito:
    @staticmethod
    def agregar_item_y_guardar(carrito: Carrito, producto: Producto, cantidad: int):
        item = ItemCarrito(producto, cantidad)
        subtotal_item = item.calcular_subtotal()
        carrito.agregar_item(item)
        carrito.calcular_total()

        # Persistencia
        ItemCarritoDAO.agregar_item(
            id_carrito=carrito.id_carrito,
            codigo_producto=producto.codigo,
            cantidad=cantidad,
            subtotal_item=subtotal_item
        )
        CarritoDAO.actualizar_totales(
            id_carrito=carrito.id_carrito,
            subtotal=carrito.subtotal,
            descuento=carrito.descuento_aplicado,
            total=carrito.total
        )
