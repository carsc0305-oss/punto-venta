from database.db_conection import conectar_db

class Producto:
    def __init__(self, id=None, codigo_barras=None, nombre=None, precio=None, stock_actual=None):
        self.id = id
        self.codigo_barras = codigo_barras
        self.nombre = nombre
        self.precio = precio
        self.stock_actual = stock_actual

    # Guardar y actualizar producto 
    def guardar(self) -> bool | None:
        try:
            with conectar_db() as conn:
                cursor = conn.cursor()
                if self.id is None:
                    cursor.execute(
                        """INSERT INTO productos (codigo_barras, nombre, precio, stock_actual)
                        VALUES (?, ?, ?, ?)""",
                        (self.codigo_barras, self.nombre, self.precio, self.stock_actual)
                    )
                else:
                    cursor.execute(
                        """UPDATE productos SET codigo_barras = ?, nombre = ?, precio = ?, stock_actual = ?
                        WHERE id = ?""",
                        (self.codigo_barras, self.nombre, self.precio, self.stock_actual, self.id)
                    )
                conn.commit()
                if self.id is None:
                    self.id = cursor.lastrowid
                return True
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"Error en Producto.guardar: {e}")
            return None

    # Obtener la lista de productos
    @staticmethod
    def obtener_todos() -> list['Producto']:
        try:
            with conectar_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT id, codigo_barras, nombre, precio, stock_actual
                    FROM productos ORDER BY id"""
                )
                rows = cursor.fetchall()
                productos_list = []
                if rows:
                    for row in rows:
                        productos_list.append(Producto(
                            id=row[0],
                            codigo_barras=row[1],
                            nombre=row[2],
                            precio=row[3],
                            stock_actual=row[4]
                        ))
                return productos_list
        except Exception as e:
            print(f"Error en Producto.obtener_todos: {e}")
            return []

    # Eliminar producto
    @staticmethod
    def eliminar(producto_id) -> bool | None:
        try:
            with conectar_db() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
                conn.commit()
                return True
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            print(f"Error en Producto.eliminar: {e}")
            return None
    
    # Buscar producto por código de barras
    @staticmethod
    def buscar_por_codigo(codigo_barras) -> 'Producto | None':
        try:
            with conectar_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT id, codigo_barras, nombre, precio, stock_actual
                    FROM productos WHERE codigo_barras = ?""",
                    (codigo_barras,)
                )
                row = cursor.fetchone()
                if row:
                    return Producto(
                        id=row[0],
                        codigo_barras=row[1],
                        nombre=row[2],
                        precio=row[3],
                        stock_actual=row[4]
                    )
                return None
        except Exception as e:
            print(f"Error en Producto.buscar_por_codigo: {e}")
            return None
    
    @staticmethod
    def buscar_por_id(producto_id) -> 'Producto | None':
        try:
            with conectar_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """SELECT id, codigo_barras, nombre, precio, stock_actual
                    FROM productos WHERE id = ?""",
                    (producto_id,)
                )
                row = cursor.fetchone()
                if row:
                    return Producto(
                        id=row[0],
                        codigo_barras=row[1],
                        nombre=row[2],
                        precio=row[3],
                        stock_actual=row[4]
                    )
                return None
        except Exception as e:
            print(f"Error en Producto.buscar_por_id: {e}")
            return None
