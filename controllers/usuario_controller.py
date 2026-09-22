from models.usuario import Usuario

class UsuarioController:

    def __init__(self):
        self.usuario_actual = None

    def login(self, nombre_usuario, contrasena) -> bool | str:
        if not nombre_usuario or not contrasena:
            return False, 'Complete los campos para iniciar sesión.'
        
        usuario = Usuario.autenticar(nombre_usuario, contrasena)
        if usuario:
            self.usuario_actual = usuario
            return True, 'Inicio de sesión exitoso.'
        
        return False, 'Nombre de usuario o contraseña incorrectos.'


    def cerrar_sesion(self):
        self.usuario_actual = None

    def obtener_usuarios(self) -> list[Usuario]:
        if not self.usuario_actual or not self.usuario_actual.rol_id == 1:  # Solo el admin puede ver la lista de usuarios
            return []
        
        return Usuario.obtener_todos()
    
    def registrar_usuario(self, usuario:Usuario, confirmar_contrasena:str) -> tuple[bool, str]:

        if not self.usuario_actual or not self.usuario_actual.rol_id == 1:  # Solo el admin puede registrar nuevos usuarios
            return False, 'No tienes permiso para registrar nuevos usuarios.'
        
        # Validaciones de campos
        if not usuario.nombre_completo or not usuario.nombre_usuario or not usuario.contrasena or not confirmar_contrasena:
            return False, "Complete todos los campos"
        
        if len(usuario.nombre_completo) < 3:
            return False, "El nombre completo debe tener al menos 3 caracteres"

        if len(usuario.nombre_usuario) < 3:
            return False, "El usuario debe tener al menos 3 caracteres"

        if usuario.contrasena != confirmar_contrasena:
            return False, "Las contraseñas no coinciden"

        if len(usuario.contrasena) < 4:
            return False, "La contraseña debe tener al menos 4 caracteres"
        
        try:
            usuario.guardar()
            return True, "Usuario registrado exitosamente"
        except Exception as e:
            if "UNIQUE" is str(e):
                return False, "El nombre de usuario ya existe"
            return False, "Error al registrar el usuario"
        
    
    def obtener_roles(self) -> list[tuple]:
        return Usuario.obtener_roles()
    
    def cambiar_estado_usuario(self, usuario_id, estado):
        if not self.usuario_actual or not self.usuario_actual.rol_id == 1:  
            return False, "Sin permisos"
        
        if usuario_id == self.usuario_actual.id:
            return False, "No puedes cambiar el estado de tu propio usuario"
        
        Usuario.cambiar_estado(usuario_id, estado)
        if estado:
            estado = "activado"
        else:
            estado = "desactivado"
        return True, f"Usuario {estado} correctamente"