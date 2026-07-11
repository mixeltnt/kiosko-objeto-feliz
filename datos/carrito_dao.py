from configuracion.conexion_bd import obtener_conexion

class CarritoDAO:
    @staticmethod
    def crear(id_cliente: int) -> int:
        sql = """
        INSERT INTO CARRITO (ID_CLIENTE, SUBTOTAL, DESCUENTO_APLICADO, TOTAL)
        VALUES (:id_cliente, 0, 0, 0)
        RETURNING ID_CARRITO INTO :id_carrito
        """
        with obtener_conexion() as con:
            cur = con.cursor()
            id_out = cur.var(int)
            cur.execute(
                sql,
                {
                    "id_cliente": id_cliente,
                    "id_carrito": id_out
                }
            )
            con.commit()
            # Oracle devuelve una lista -> tomamos el primer valor
            return int(id_out.getvalue()[0])

    @staticmethod
    def actualizar_totales(id_carrito: int, subtotal: float, descuento: float, total: float):
        sql = """
        UPDATE CARRITO
        SET SUBTOTAL = :s,
            DESCUENTO_APLICADO = :d,
            TOTAL = :t
        WHERE ID_CARRITO = :id
        """
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(
                sql,
                {
                    "s": float(subtotal),
                    "d": float(descuento),
                    "t": float(total),
                    "id": id_carrito
                }
            )
            con.commit()

    @staticmethod
    def listar():
        sql = """
        SELECT ID_CARRITO,
               ID_CLIENTE,
               FECHA_CREACION,
               SUBTOTAL,
               DESCUENTO_APLICADO,
               TOTAL
        FROM CARRITO
        ORDER BY ID_CARRITO DESC
        """
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql)
            return cur.fetchall()
