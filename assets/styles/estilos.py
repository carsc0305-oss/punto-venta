import customtkinter as ctk
from tkinter import ttk

def estilizar_tabla():
    modo = ctk.get_appearance_mode()
    style = ttk.Style()
    style.theme_use("clam")

    if modo == "Dark":
        bg = "#2b2b2b"
        fg = "#DCE4EE"
        field_bg = "#2b2b2b"
        heading_bg = "#1f1f1f"
        heading_fg = "#DCE4EE"
        sel_bg = "#1f6aa5"
        heading_active = "#333333"
    else:
        bg = "#ffffff"
        fg = "#1a1a1a"
        field_bg = "#ffffff"
        heading_bg = "#e8e8e8"
        heading_fg = "#1a1a1a"
        sel_bg = "#3B8ED0"
        heading_active = "#d0d0d0"

    style.configure("Treeview",
                    background=bg, foreground=fg,
                    fieldbackground=field_bg, rowheight=32,
                    font=("Segoe UI", 13))
    style.configure("Treeview.Heading",
                    background=heading_bg, foreground=heading_fg,
                    font=("Segoe UI", 13, "bold"), relief="flat")
    style.map("Treeview",
              background=[("selected", sel_bg)],
              foreground=[("selected", "white")])
    style.map("Treeview.Heading",
              background=[("active", heading_active)])