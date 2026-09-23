import customtkinter as ctk

from controllers.cliente_controller import ClienteController
from views.cliente_view import ClienteView


# ============================================================
# CONFIGURACIÓN DE LA VENTANA
# ============================================================

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

app = ctk.CTk()

app.title("Prueba - Gestión de Clientes")
app.geometry("1000x650")


# ============================================================
# CONTROLLER
# ============================================================

cliente_controller = ClienteController()


# ============================================================
# VIEW
# ============================================================

vista_clientes = ClienteView(
    app,
    cliente_controller
)

vista_clientes.pack(
    fill="both",
    expand=True
)


# ============================================================
# EJECUTAR
# ============================================================

app.mainloop()