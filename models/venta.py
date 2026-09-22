from database.db_conection import conectar_db

class DetalleVenta:
    """Modelo para representar cada item de una venta."""
    def __init__(self, producto_id, cantidad, precio_unitario, subtotal):
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal

    def guardar(self, cursor, venta_id):
        """Guarda el detalle en la BD y actualiza el stock."""
        cursor.execute(
            """INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)""",
            (venta_id, self.producto_id, self.cantidad,
             self.precio_unitario, self.subtotal)
        )
        cursor.execute(
            "UPDATE productos SET stock_actual = stock_actual - ? WHERE id = ?",
            (self.cantidad, self.producto_id)
        )

class Venta:
    def __init__(self, id=None, usuario_id=None, fecha_venta=None,
                 subtotal=0, impuestos=0, total=0):
        self.id = id
        self.usuario_id = usuario_id
        self.fecha_venta = fecha_venta
        self.subtotal = subtotal
        self.impuestos = impuestos
        self.total = total

    @staticmethod
    def crear(usuario_id, detalles, subtotal, impuestos, total):
        """Registra una venta en la BD con valores ya calculados por el Controller.

        Args:
            usuario_id: ID del usuario que realiza la venta.
            detalles: Lista de objetos DetalleVenta.
            subtotal: Suma de los subtotales de cada item (calculado por Controller).
            impuestos: Monto de impuestos aplicados (calculado por Controller).
            total: Monto total de la venta (calculado por Controller).

        Returns:
            int: ID de la venta registrada.
        """
        try:
            with conectar_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO ventas (usuario_id, subtotal, impuestos, total) VALUES (?, ?, ?, ?)",
                    (usuario_id, subtotal, impuestos, total)
                )
                venta_id = cursor.lastrowid

                for detalle in detalles:
                    detalle.guardar(cursor, venta_id)

                conn.commit()
                return venta_id
        except Exception:
            conn.rollback()
            return None

    @staticmethod
    def obtener_todas():
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT v.id, u.nombre_usuario, v.fecha_venta, v.subtotal, v.impuestos, v.total
                   FROM ventas v
                   JOIN usuarios u ON v.usuario_id = u.id
                   ORDER BY v.id DESC"""
            )
            return cursor.fetchall() or []

    @staticmethod
    def obtener_detalle(venta_id):
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT p.nombre, dv.cantidad, dv.precio_unitario, dv.subtotal
                   FROM detalle_ventas dv
                   JOIN productos p ON dv.producto_id = p.id
                   WHERE dv.venta_id = ?""",
                (venta_id,)
            )
            return cursor.fetchall() or []