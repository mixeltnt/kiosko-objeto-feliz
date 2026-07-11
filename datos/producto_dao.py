from configuracion.conexion_bd import obtener_conexion

class ProductoDAO:
    @staticmethod
    def crear(codigo: str, nombre: str, precio_neto: float, estado: str = "ACTIVO"):
        sql = """INSERT INTO PRODUCTO (CODIGO, NOMBRE, PRECIO_NETO, ESTADO) VALUES (:c,:n,:p,:e)"""
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, {"c": codigo, "n": nombre, "p": float(precio_neto), "e": estado})
            con.commit()

    @staticmethod
    def listar(activos_solo: bool = False):
        if activos_solo:
            sql = """SELECT CODIGO, NOMBRE, PRECIO_NETO, ESTADO FROM PRODUCTO WHERE ESTADO='ACTIVO' ORDER BY NOMBRE"""
            params = {}
        else:
            sql = """SELECT CODIGO, NOMBRE, PRECIO_NETO, ESTADO FROM PRODUCTO ORDER BY NOMBRE"""
            params = {}
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, params)
            return cur.fetchall()

    @staticmethod
    def buscar_por_codigo(codigo: str):
        sql = """SELECT CODIGO, NOMBRE, PRECIO_NETO, ESTADO FROM PRODUCTO WHERE CODIGO=:c"""
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, {"c": codigo})
            return cur.fetchone()

    @staticmethod
    def actualizar(codigo: str, nombre: str, precio_neto: float, estado: str):
        sql = """UPDATE PRODUCTO SET NOMBRE=:n, PRECIO_NETO=:p, ESTADO=:e WHERE CODIGO=:c"""
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, {"c": codigo, "n": nombre, "p": float(precio_neto), "e": estado})
            con.commit()

    @staticmethod
    def eliminar(codigo: str):
        sql = """DELETE FROM PRODUCTO WHERE CODIGO=:c"""
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, {"c": codigo})
            con.commit()
