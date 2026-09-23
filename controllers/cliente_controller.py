from database.db_conection import conectar_db
from models.cliente import Cliente


class ClienteController:

    # ============================================================
    # REGISTRAR CLIENTE
    # ============================================================

    def registrar_cliente(self, ruc, razon_social, estado="ACTIVO"):

        # Convertir a texto por seguridad
        ruc = str(ruc).strip()
        razon_social = str(razon_social).strip()

        # Validaciones básicas
        if not ruc:
            raise ValueError("El RUC es obligatorio.")

        if not razon_social:
            raise ValueError("La razón social es obligatoria.")

        if len(ruc) != 11 or not ruc.isdigit():
            raise ValueError(
                "El RUC debe contener exactamente 11 dígitos."
            )

        conn = conectar_db()

        try:

            cursor = conn.cursor()

            # Verificar si el RUC ya existe
            cursor.execute(
                """
                SELECT id
                FROM clientes
                WHERE ruc = ?
                """,
                (ruc,)
            )

            cliente_existente = cursor.fetchone()

            if cliente_existente:
                raise ValueError(
                    f"El RUC {ruc} ya se encuentra registrado."
                )

            # Insertar cliente
            cursor.execute(
                """
                INSERT INTO clientes
                (ruc, razon_social, estado)
                VALUES (?, ?, ?)
                """,
                (
                    ruc,
                    razon_social,
                    estado
                )
            )

            conn.commit()

            cliente_id = cursor.lastrowid

            return Cliente(
                id=cliente_id,
                ruc=ruc,
                razon_social=razon_social,
                estado=estado
            )

        except Exception:

            conn.rollback()
            raise

        finally:

            conn.close()


    # ============================================================
    # BUSCAR CLIENTE POR RUC
    # ============================================================

    def buscar_por_ruc(self, ruc):

        # IMPORTANTE:
        # El RUC se maneja como texto.
        ruc = str(ruc).strip()

        conn = conectar_db()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    ruc,
                    razon_social,
                    estado
                FROM clientes
                WHERE ruc = ?
                """,
                (ruc,)
            )

            fila = cursor.fetchone()

            if not fila:
                return None

            return Cliente(
                id=fila[0],
                ruc=str(fila[1]),
                razon_social=fila[2],
                estado=fila[3]
            )

        finally:

            conn.close()


    # ============================================================
    # BUSCAR CLIENTES
    # ============================================================

    def buscar(self, texto):

        texto = str(texto).strip()

        conn = conectar_db()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    ruc,
                    razon_social,
                    estado
                FROM clientes
                WHERE ruc LIKE ?
                   OR razon_social LIKE ?
                ORDER BY razon_social
                """,
                (
                    f"%{texto}%",
                    f"%{texto}%"
                )
            )

            filas = cursor.fetchall()

            clientes = []

            for fila in filas:

                cliente = Cliente(
                    id=fila[0],
                    ruc=str(fila[1]),
                    razon_social=fila[2],
                    estado=fila[3]
                )

                clientes.append(cliente)

            return clientes

        finally:

            conn.close()


    # ============================================================
    # OBTENER TODOS LOS CLIENTES
    # ============================================================

    def obtener_todos(self):

        conn = conectar_db()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    ruc,
                    razon_social,
                    estado
                FROM clientes
                ORDER BY razon_social
                """
            )

            filas = cursor.fetchall()

            clientes = []

            for fila in filas:

                clientes.append(
                    Cliente(
                        id=fila[0],
                        ruc=str(fila[1]),
                        razon_social=fila[2],
                        estado=fila[3]
                    )
                )

            return clientes

        finally:

            conn.close()


    # ============================================================
    # ACTUALIZAR CLIENTE
    # ============================================================

    def actualizar_cliente(
        self,
        cliente_id,
        ruc,
        razon_social,
        estado="ACTIVO"
    ):

        ruc = str(ruc).strip()
        razon_social = str(razon_social).strip()

        # Validaciones
        if not ruc:
            raise ValueError("El RUC es obligatorio.")

        if not razon_social:
            raise ValueError("La razón social es obligatoria.")

        if len(ruc) != 11 or not ruc.isdigit():
            raise ValueError(
                "El RUC debe contener exactamente 11 dígitos."
            )

        conn = conectar_db()

        try:

            cursor = conn.cursor()

            # Comprobar que el RUC no pertenezca a otro cliente
            cursor.execute(
                """
                SELECT id
                FROM clientes
                WHERE ruc = ?
                AND id != ?
                """,
                (
                    ruc,
                    cliente_id
                )
            )

            if cursor.fetchone():

                raise ValueError(
                    f"El RUC {ruc} ya pertenece a otro cliente."
                )

            # Actualizar
            cursor.execute(
                """
                UPDATE clientes
                SET
                    ruc = ?,
                    razon_social = ?,
                    estado = ?
                WHERE id = ?
                """,
                (
                    ruc,
                    razon_social,
                    estado,
                    cliente_id
                )
            )

            conn.commit()

            if cursor.rowcount == 0:

                raise ValueError(
                    "No se encontró el cliente indicado."
                )

            return True

        except Exception:

            conn.rollback()
            raise

        finally:

            conn.close()


    # ============================================================
    # CAMBIAR ESTADO
    # ============================================================

    def cambiar_estado(self, cliente_id, estado):

        estados_validos = [
            "ACTIVO",
            "INACTIVO"
        ]

        if estado not in estados_validos:

            raise ValueError(
                "El estado debe ser ACTIVO o INACTIVO."
            )

        conn = conectar_db()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE clientes
                SET estado = ?
                WHERE id = ?
                """,
                (
                    estado,
                    cliente_id
                )
            )

            conn.commit()

            return cursor.rowcount > 0

        except Exception:

            conn.rollback()
            raise

        finally:

            conn.close()