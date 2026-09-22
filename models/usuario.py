import hashlib
from database.db_conection import conectar_db

class Usuario:
    def __init__(self, id=None, nombre_completo=None, nombre_usuario=None, contrasena=None, rol_id=None, activo=1, fecha_creacion=None, rol_nombre=None):
        self.id = id
        self.nombre_completo = nombre_completo
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.rol_id = rol_id
        self.activo = activo
        self.fecha_creacion = fecha_creacion
        self.rol_nombre = rol_nombre


    def _hash_password(contrasena):
        return hashlib.sha256(contrasena.encode()).hexdigest()
    
    def autenticar(nombre_usuario, contrasena)-> 'Usuario | None':
        hashed = Usuario._hash_password(contrasena)

        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.id, u.nombre_completo, u.nombre_usuario, u.contrasena, r.nombre, u.activo, u.rol_id
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id
                WHERE u.nombre_usuario = ? AND u.activo = 1
            ''', (nombre_usuario,))

            usuario = cursor.fetchone()
            if usuario and usuario[3] == hashed:
                return Usuario(
                    id=usuario[0],
                    nombre_completo=usuario[1],
                    nombre_usuario=usuario[2],
                    contrasena=usuario[3],
                    rol_nombre=usuario[4],
                    activo=usuario[5],
                    rol_id=usuario[6]
                )
            
        return None
    
    def obtener_todos() -> list['Usuario']:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT u.id, u.nombre_completo, u.nombre_usuario, r.nombre, u.activo, u.fecha_creacion
                FROM usuarios u
                JOIN roles r ON u.rol_id = r.id
            ''')

            usuarios = []
            for usuario in cursor.fetchall():
                usuarios.append(Usuario(
                    id=usuario[0],
                    nombre_completo=usuario[1],
                    nombre_usuario=usuario[2],
                    rol_nombre=usuario[3],
                    activo=usuario[4],
                    fecha_creacion=usuario[5]
                ))
            
            return usuarios

    def guardar(self) -> int | None:

        try:
            self.contrasena = Usuario._hash_password(self.contrasena)
            with conectar_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO usuarios (nombre_completo, nombre_usuario, contrasena, rol_id)
                    VALUES (?, ?, ?, ?)
                ''', (self.nombre_completo, self.nombre_usuario, self.contrasena, self.rol_id))
                conn.commit()
                self.id = cursor.lastrowid
                return self.id
        except Exception as e:
            conn.rollback()
            return None
        

    def cambiar_estado(usuario_id, estado) -> bool | None:
        try:
            with conectar_db() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE usuarios
                    SET activo = ?
                    WHERE id = ?
                ''', (estado, usuario_id))
                conn.commit()
                return True
        except Exception as e:
            conn.rollback()
            return False
        
    def obtener_roles() -> list[tuple]:
        with conectar_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, nombre FROM roles')
            return cursor.fetchall()
    