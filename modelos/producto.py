class Producto:
    IVA = 0.19

    def __init__(self, codigo: str, nombre: str, precio_neto: float, estado: str = "ACTIVO"):
        self.codigo = codigo
        self.nombre = nombre
        self.precio_neto = float(precio_neto)
        self.estado = estado

    def calcular_precio_iva(self) -> float:
        return round(self.precio_neto * (1 + self.IVA), 2)
