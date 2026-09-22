import customtkinter as ctk
from views.login_view import LoginView



def main():
    ctk.set_appearance_mode("light")  # Modos: "light", "dark", "system"
    # ctk.set_default_color_theme("green")
    
    # inicializar_db()

    app = LoginView()
    app.mainloop()

if __name__ == "__main__":
    main()


