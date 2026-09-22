import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from config import ICON_PATH, ADMIN_IMG, ALMACEN_IMG, VENTAS_IMG
from views.usuario_view import UsuariosView
from views.producto_view import ProductoView
from controllers.producto_controller import ProductoController

from controllers.venta_controller import VentaController

class MainView(ctk.CTk):
    def __init__(self, usuario_controller):
        super().__init__()

        self.usuario_controller = usuario_controller
        usuario = usuario_controller.usuario_actual

        self.producto_controller = ProductoController()

        # El controlador de ventas necesita el ID y nombre del cajero
        self.venta_controller = VentaController(usuario.id, usuario.nombre_completo)

        self.title("Punto de Venta - Sistama")
        self.geometry("1400x800")
        self.minsize(900, 550)
        self.iconbitmap(ICON_PATH)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=210, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content.grid(row=0, column=1, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self._crear_sidebar(usuario)
        self._mostrar_bienvenida(usuario)


    def _crear_sidebar(self, usuario):
        self.sidebar.grid_columnconfigure(0, weight=1)

        row_idx = 0
         
        ctk.CTkLabel(
            self.sidebar, text="Punto de Venta",
            font=ctk.CTkFont(size=25, weight="bold")
        ).grid(row=row_idx, column=0, pady=(25, 5))
        row_idx += 1

        # Información del usuario en el sidebar
        ctk.CTkLabel(
            self.sidebar,
            text=f"{usuario.nombre_completo}",
            font=ctk.CTkFont(size=14, weight="normal")
        ).grid(row=row_idx, column=0)
        row_idx += 1

        ctk.CTkLabel(
            self.sidebar,
            text=f"({usuario.rol_nombre})",
        ).grid(row=row_idx, column=0, pady=(0, 25))
        row_idx += 1

        # Botón de Inicio (Home)
        ctk.CTkButton(
            self.sidebar, text="Inicio", height=36,
            command=lambda: self._mostrar_bienvenida(usuario)
        ).grid(row=row_idx, column=0, sticky="ew", padx=12, pady=3)
        row_idx += 1

        if usuario.rol_id == 1:
            ctk.CTkButton(
                self.sidebar, text="Usuarios", height=36,
                command=self._mostrar_usuarios
            ).grid(row=row_idx, column=0, sticky="ew", padx=12, pady=3)
            row_idx += 1

        if usuario.rol_id == 1 or usuario.rol_id == 3:
            ctk.CTkButton(
                self.sidebar, text="Productos", height=36,
                command=self._mostrar_productos
            ).grid(row=row_idx, column=0, sticky="ew", padx=12, pady=3)
            row_idx += 1

        if usuario.rol_id == 1 or usuario.rol_id == 2:
            ctk.CTkButton(
                self.sidebar, text="Ventas", height=36,
                command=self._mostrar_ventas
            ).grid(row=row_idx, column=0, sticky="ew", padx=12, pady=3)
            row_idx += 1

        # Espacio flexible para empujar el botón de Cerrar Sesión al final
        spacer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        spacer.grid(row=row_idx, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(row_idx, weight=1)
        row_idx += 1

        # Botón Cerrar Sesión
        ctk.CTkButton(
            self.sidebar, text="Cerrar Sesión", height=36,
            fg_color="#C0392B", hover_color="#A93226",
            command=self._cerrar_sesion
        ).grid(row=row_idx, column=0, sticky="ew", padx=12, pady=(0, 18))

    def _limpiar_contenido(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def _mostrar_bienvenida(self, usuario):
        self._limpiar_contenido()

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        # Seleccionar imagen de fondo según el rol
        try:
            if usuario.rol_id == 1:
                bg_image = ctk.CTkImage(light_image=Image.open(ADMIN_IMG), size=(1200, 600))
            elif usuario.rol_id == 2:
                bg_image = ctk.CTkImage(light_image=Image.open(VENTAS_IMG), size=(1200, 600))
            elif usuario.rol_id == 3:
                bg_image = ctk.CTkImage(light_image=Image.open(ALMACEN_IMG), size=(1200, 600))

            bg_label = ctk.CTkLabel(self.content, image=bg_image, text="")
            bg_label.grid(row=0, column=0, sticky="nsew", pady=20)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar la imagen: {str(e)}")

        # Tarjeta de bienvenida
        frame = ctk.CTkFrame(self.content)
        frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=(0, 12))
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame, text=f"Bienvenido, {usuario.nombre_completo}",
            font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=0, column=0, pady=(15, 0))

        ctk.CTkLabel(frame, text=f"Rol: {usuario.rol_nombre}").grid(row=1, column=0)
        ctk.CTkLabel(frame, text="Seleccione una opción del menú lateral").grid(row=2, column=0, pady=(0, 15))


    def _cerrar_sesion(self):
        self.usuario_controller.cerrar_sesion()
        self.destroy()

        from views.login_view import LoginView
        app = LoginView()
        app.mainloop()

    def _mostrar_usuarios(self):
        self._limpiar_contenido()
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=0)
        UsuariosView(self.content, self.usuario_controller).grid(row=0, column=0, sticky="nsew")

    def _mostrar_productos(self):
        self._limpiar_contenido()
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=0)
        ProductoView(self.content, self.producto_controller).grid(row=0, column=0, sticky="nsew")


    def _mostrar_ventas(self):
        """Cambia el contenido central al módulo de ventas."""
        self._limpiar_contenido()
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=0)
        from views.venta_view import VentaView
        VentaView(self.content, self.venta_controller).grid(row=0, column=0, sticky="nsew")