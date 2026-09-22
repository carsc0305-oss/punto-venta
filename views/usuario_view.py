import customtkinter as ctk
from tkinter import ttk
from config import ICON_PATH
from tkinter import messagebox


class UsuariosView(ctk.CTkFrame):
    def __init__(self, master, usuario_controller):
        super().__init__(master, fg_color="transparent")

        self.usuario_controller = usuario_controller
        self.roles = self.usuario_controller.obtener_roles()

        self._crear_header()
        self._crear_tabla()
        self._cargar_usuarios()


    def _crear_header(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=25, pady=(20, 12))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header, text="Gestión de Usuarios",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            header, text="+ Nuevo Usuario", width=150, height=34,
            command=self._abrir_formulario
        ).grid(row=0, column=1, sticky="e") 

    def _crear_tabla(self):
        from assets.styles.estilos import estilizar_tabla
        estilizar_tabla()

        tabla_frame = ctk.CTkFrame(self)
        tabla_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 12))
        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(0, weight=1)

        cols = ("id", "nombre_completo", "usuario", "rol", "estado", "fecha")
        self.tree = ttk.Treeview(tabla_frame, columns=cols, show="headings", height=12)

        self.tree.heading("id", text="ID")
        self.tree.heading("nombre_completo", text="Nombre Completo", anchor="w")# con aliniacion a la izquierda
        self.tree.heading("usuario", text="Usuario", anchor="w")
        self.tree.heading("rol", text="Rol")
        self.tree.heading("estado", text="Estado")
        self.tree.heading("fecha", text="Fecha Creación")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nombre_completo", width=200)
        self.tree.column("usuario", width=180)
        self.tree.column("rol", width=140, anchor="center")
        self.tree.column("estado", width=100, anchor="center")
        self.tree.column("fecha", width=180, anchor="center")

        scroll = ctk.CTkScrollbar(tabla_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=(8, 0), pady=8)
        scroll.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=8)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=25, pady=(0, 18))

        ctk.CTkButton(
            btn_frame, text="Activar", width=120, height=34,
            fg_color="#2FA572", hover_color="#288F62",
            command=lambda: self._cambiar_estado(1)
        ).grid(row=0, column=0, padx=(0, 6))

        ctk.CTkButton(
            btn_frame, text="Desactivar", width=120, height=34,
            fg_color="#C0392B", hover_color="#A93226",
            command=lambda: self._cambiar_estado(0)
        ).grid(row=0, column=1, padx=(0, 6))

        ctk.CTkButton(
            btn_frame, text="Refrescar", width=120, height=34,
            fg_color="gray", hover_color="gray30",
            command=self._cargar_usuarios
        ).grid(row=0, column=2)

    def _cambiar_estado(self, estado):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Seleccione un usuario")
            return

        usuario_id = self.tree.item(sel[0])["values"][0]
        exito = self.usuario_controller.cambiar_estado_usuario(usuario_id, estado)
        if exito:
            self._cargar_usuarios()
            messagebox.showinfo("Éxito", "Estado del usuario actualizado")
        else:
            messagebox.showerror("Error", "Error al actualizar el estado del usuario")


    def _cargar_usuarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        usuarios = self.usuario_controller.obtener_usuarios()
        for u in usuarios:
            if u.activo == 1:
                estado = "Activo"
            else:
                estado = "Inactivo"
            # estado = "Activo" if u.activo == 1 else "Inactivo"
            self.tree.insert("", "end", values=(u.id, u.nombre_completo, u.nombre_usuario, u.rol_nombre, estado, u.fecha_creacion))

    def _abrir_formulario(self):
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Registrar Usuario")
        dialogo.geometry("500x450")
        dialogo.resizable(False, False)
        dialogo.after(200, lambda: dialogo.iconbitmap(ICON_PATH))
        dialogo.grab_set() 
        dialogo.transient(self.winfo_toplevel()) 
        dialogo.grid_columnconfigure(0, weight=1)

        row_idx = 0
        ctk.CTkLabel(
            dialogo, text="Nuevo Usuario",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=row_idx, column=0, pady=(25, 18))
        row_idx += 1

        entry_nombre = ctk.CTkEntry(dialogo, placeholder_text="Nombre completo", width=270, height=36)
        entry_nombre.grid(row=row_idx, column=0, pady=(0, 10))
        row_idx += 1

        entry_usuario = ctk.CTkEntry(dialogo, placeholder_text="Nombre de usuario", width=270, height=36)
        entry_usuario.grid(row=row_idx, column=0, pady=(0, 10))
        row_idx += 1

        entry_contra = ctk.CTkEntry(dialogo, placeholder_text="Contraseña", show="●", width=270, height=36)
        entry_contra.grid(row=row_idx, column=0, pady=(0, 10))
        row_idx += 1

        entry_confirmar = ctk.CTkEntry(dialogo, placeholder_text="Confirmar contraseña", show="●", width=270, height=36)
        entry_confirmar.grid(row=row_idx, column=0, pady=(0, 10))
        row_idx += 1

        rol_nombres = []
        for r in self.roles:
            rol_nombres.append(r[1])

        combo_rol = ctk.CTkComboBox(dialogo, values=rol_nombres, width=270, height=36, state="readonly")
        combo_rol.set(rol_nombres[0])
        combo_rol.grid(row=row_idx, column=0, pady=(0, 15))
        row_idx += 1

        def registrar():
            from models.usuario import Usuario
            usuario = Usuario(
                nombre_completo=entry_nombre.get().strip(),
                nombre_usuario=entry_usuario.get().strip(),
                contrasena=entry_contra.get().strip(),
                rol_id=combo_rol.get()
            )

            confirmar = entry_confirmar.get().strip()

            for r in self.roles:
                if r[1] == usuario.rol_id:
                    usuario.rol_id = r[0]
                    break

            if not usuario.rol_id:
                messagebox.showerror("Error", "Seleccione un rol")
                return

            exito, mensaje = self.usuario_controller.registrar_usuario(usuario, confirmar)

            if exito:
                entry_nombre.delete(0, "end")
                entry_usuario.delete(0, "end")
                entry_contra.delete(0, "end")
                entry_confirmar.delete(0, "end")
                self._cargar_usuarios()
                dialogo.destroy()
                messagebox.showinfo("Éxito", mensaje) 
            else:
                messagebox.showerror("Error", mensaje)

        ctk.CTkButton(dialogo, text="Registrar", width=270, height=38, command=registrar).grid(row=row_idx, column=0, pady=(0, 10))