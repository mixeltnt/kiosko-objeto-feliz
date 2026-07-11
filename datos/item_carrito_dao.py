from configuracion.conexion_bd import obtener_conexion

class ItemCarritoDAO:
    @staticmethod
    def agregar_item(id_carrito: int, codigo_producto: str, cantidad: int, subtotal_item: float):
        sql = """
        INSERT INTO ITEM_CARRITO (ID_CARRITO, CODIGO_PRODUCTO, CANTIDAD, SUBTOTAL_ITEM)
        VALUES (:idc, :cod, :cant, :sub)
        """
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, {"idc": id_carrito, "cod": codigo_producto, "cant": int(cantidad), "sub": float(subtotal_item)})
            con.commit()

    @staticmethod
    def listar_por_carrito(id_carrito: int):
        sql = """
        SELECT IC.ID_ITEM, IC.CODIGO_PRODUCTO, P.NOMBRE, IC.CANTIDAD, IC.SUBTOTAL_ITEM
        FROM ITEM_CARRITO IC
        JOIN PRODUCTO P ON P.CODIGO = IC.CODIGO_PRODUCTO
        WHERE IC.ID_CARRITO = :idc
        ORDER BY IC.ID_ITEM DESC
        """
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, {"idc": id_carrito})
            return cur.fetchall()

    @staticmethod
    def eliminar(id_item: int):
        sql = """DELETE FROM ITEM_CARRITO WHERE ID_ITEM=:id"""
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, {"id": id_item})
            con.commit()
