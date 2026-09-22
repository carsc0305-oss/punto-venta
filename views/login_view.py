import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from config import ICON_PATH, IMAGE_POST
from controllers.usuario_controller import UsuarioController

class LoginView(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Punto de Venta - Login")
        self.geometry("650x550")
        self.resizable(False, False)
        self.iconbitmap(ICON_PATH)

        self.usuario_controller = UsuarioController()

        self._crear_widgets()

    
    def _crear_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(self)
        card.grid(row=0, column=0, padx=10, pady=10)
        card.grid_columnconfigure(0, weight=1)

        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open(IMAGE_POST),
                dark_image=Image.open(IMAGE_POST),
                size=(150, 150))
            logo_label = ctk.CTkLabel(card, image=logo_image, text="")
            logo_label.grid(row=0, column=0, pady=(20, 0))
        except Exception:
            pass

        # Títulos
        ctk.CTkLabel(
            card, text="Punto de Venta",
            font=ctk.CTkFont(size=30, weight="bold")
        ).grid(row=1, column=0, pady=(35, 5))

        ctk.CTkLabel(
            card, 
            text="Inicie sesión para continuar en el sistema de Punto de Venta creado por ROELCODE.",
            font=ctk.CTkFont(size=14, weight="normal")
            ).grid(row=2, column=0, pady=(0, 30), padx=20)
        
        # Campo de entrada: Usuario
        self.entry_usuario = ctk.CTkEntry(
            card, placeholder_text="Nombre de Usuario", width=300, height=40,
            font=ctk.CTkFont(size=16, weight="normal")
        )
        self.entry_usuario.grid(row=3, column=0, pady=(0, 12))

        # Al presionar Enter, pasar al campo de contraseña
        self.entry_usuario.bind("<Return>", lambda e: self.entry_contrasena.focus())

        # Campo de entrada: Contraseña
        self.entry_contrasena = ctk.CTkEntry(
            card, placeholder_text="Contraseña", show="●", width=300, height=40,
            font=ctk.CTkFont(size=16, weight="normal")
        )
        self.entry_contrasena.grid(row=4, column=0, pady=(0, 12))

        # Al presionar Enter, ejecutar el login
        self.entry_contrasena.bind("<Return>", lambda e: self._login())

        # Botón de Inicio de Sesión
        ctk.CTkButton(
            card, text="Iniciar Sesión", width=300, height=38,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self._login
        ).grid(row=5, column=0, pady=(0, 15))

    def _login(self):
        nombre_usuario = self.entry_usuario.get()
        contrasena = self.entry_contrasena.get()

        exito, mensaje = self.usuario_controller.login(nombre_usuario, contrasena)

        if exito:
            self.destroy()

            from views.main_view import MainView
            app = MainView(self.usuario_controller)
            app.mainloop()
        else:
            messagebox.showerror("Error", mensaje)






        


