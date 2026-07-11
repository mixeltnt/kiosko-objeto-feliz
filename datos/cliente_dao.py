from configuracion.conexion_bd import obtener_conexion

class ClienteDAO:
    @staticmethod
    def crear(rut: str, nombre: str, email: str, contrasena_hash: bytes, nivel: str) -> int:
        sql = """
        INSERT INTO CLIENTE (RUT, NOMBRE, EMAIL, CONTRASENA_HASH, NIVEL)
        VALUES (:rut, :nombre, :email, :hash, :nivel)
        RETURNING ID_CLIENTE INTO :id_cliente
        """
        with obtener_conexion() as con:
            cur = con.cursor()
            id_out = cur.var(int)

            cur.execute(
                sql,
                {
                    "rut": rut,
                    "nombre": nombre,
                    "email": email,
                    "hash": contrasena_hash,
                    "nivel": nivel,
                    "id_cliente": id_out
                }
            )

            con.commit()
            # Oracle devuelve una lista -> tomamos el primer valor
            return int(id_out.getvalue()[0])

    @staticmethod
    def listar():
        sql = """
        SELECT ID_CLIENTE, RUT, NOMBRE, EMAIL, NIVEL, FECHA_REGISTRO
        FROM CLIENTE
        ORDER BY ID_CLIENTE DESC
        """
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql)
            return cur.fetchall()

    @staticmethod
    def buscar_por_id(id_cliente: int):
        sql = """
        SELECT ID_CLIENTE, RUT, NOMBRE, EMAIL, CONTRASENA_HASH, NIVEL
        FROM CLIENTE
        WHERE ID_CLIENTE = :id
        """
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, {"id": id_cliente})
            return cur.fetchone()

    @staticmethod
    def actualizar(id_cliente: int, rut: str, nombre: str, email: str, nivel: str):
        sql = """
        UPDATE CLIENTE
        SET RUT = :rut,
            NOMBRE = :nombre,
            EMAIL = :email,
            NIVEL = :nivel
        WHERE ID_CLIENTE = :id
        """
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(
                sql,
                {
                    "rut": rut,
                    "nombre": nombre,
                    "email": email,
                    "nivel": nivel,
                    "id": id_cliente
                }
            )
            con.commit()

    @staticmethod
    def eliminar(id_cliente: int):
        sql = "DELETE FROM CLIENTE WHERE ID_CLIENTE = :id"
        with obtener_conexion() as con:
            cur = con.cursor()
            cur.execute(sql, {"id": id_cliente})
            con.commit()
