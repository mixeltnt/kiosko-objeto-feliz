from modelos.persona import Persona

class Cliente(Persona):
    def __init__(self, id_cliente: int, nombre: str, email: str, rut: str, nivel: str, contrasena_hash: bytes):
        super().__init__(nombre, email, rut)
        self.id_cliente = id_cliente
        self.nivel = nivel
        self.contrasena_hash = contrasena_hash

    def aplicar_descuento(self, subtotal: float) -> float:
        # ejemplo de regla: estudiante 10%
        if (self.nivel or "").upper() == "ESTUDIANTE":
            return round(subtotal * 0.10, 2)
        return 0.0
