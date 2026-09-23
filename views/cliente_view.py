import customtkinter as ctk
from tkinter import ttk, messagebox

from assets.styles.estilos import estilizar_tabla


class ClienteView(ctk.CTkFrame):

    def __init__(self, master, cliente_controller):
        super().__init__(master, fg_color="transparent")

        self.cliente_controller = cliente_controller

        self._crear_header()
        self._crear_busqueda()
        self._crear_tabla()
        self._crear_botones()

        self._cargar_clientes()

    # ============================================================
    # HEADER
    # ============================================================

    def _crear_header(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=25,
            pady=(20, 10)
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Gestión de Clientes",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        ctk.CTkButton(
            header,
            text="+ Nuevo Cliente",
            width=150,
            height=34,
            command=self._abrir_formulario
        ).grid(
            row=0,
            column=1,
            sticky="e"
        )

    # ============================================================
    # BUSQUEDA
    # ============================================================

    def _crear_busqueda(self):

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 10)
        )

        frame.grid_columnconfigure(0, weight=1)

        self.entry_busqueda = ctk.CTkEntry(
            frame,
            placeholder_text="Buscar por RUC o razón social...",
            height=36
        )

        self.entry_busqueda.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 8)
        )

        self.entry_busqueda.bind(
            "<Return>",
            lambda event: self._buscar_clientes()
        )

        ctk.CTkButton(
            frame,
            text="Buscar",
            width=100,
            height=36,
            command=self._buscar_clientes
        ).grid(
            row=0,
            column=1,
            padx=(0, 8)
        )

        ctk.CTkButton(
            frame,
            text="Mostrar todos",
            width=120,
            height=36,
            command=self._cargar_clientes
        ).grid(
            row=0,
            column=2
        )

    # ============================================================
    # TABLA
    # ============================================================

    def _crear_tabla(self):

        estilizar_tabla()

        tabla_frame = ctk.CTkFrame(self)

        tabla_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=25,
            pady=(0, 12)
        )

        tabla_frame.grid_columnconfigure(0, weight=1)
        tabla_frame.grid_rowconfigure(0, weight=1)

        columnas = (
            "id",
            "ruc",
            "razon_social",
            "estado"
        )

        self.tree = ttk.Treeview(
            tabla_frame,
            columns=columnas,
            show="headings"
        )

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "ruc",
            text="RUC"
        )

        self.tree.heading(
            "razon_social",
            text="Razón Social",
            anchor="w"
        )

        self.tree.heading(
            "estado",
            text="Estado"
        )

        self.tree.column(
            "id",
            width=60,
            anchor="center"
        )

        self.tree.column(
            "ruc",
            width=140,
            anchor="center"
        )

        self.tree.column(
            "razon_social",
            width=400,
            anchor="w"
        )

        self.tree.column(
            "estado",
            width=120,
            anchor="center"
        )

        scrollbar = ctk.CTkScrollbar(
            tabla_frame,
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(8, 0),
            pady=8
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns",
            padx=(0, 5),
            pady=8
        )

        self.tree.bind(
            "<Double-1>",
            lambda event: self._editar_cliente()
        )

    # ============================================================
    # BOTONES
    # ============================================================

    def _crear_botones(self):

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 18)
        )

        ctk.CTkButton(
            frame,
            text="Editar",
            width=120,
            height=34,
            command=self._editar_cliente
        ).grid(
            row=0,
            column=0,
            padx=(0, 6)
        )

        ctk.CTkButton(
            frame,
            text="Activar",
            width=120,
            height=34,
            fg_color="#2FA572",
            hover_color="#288F62",
            command=lambda: self._cambiar_estado("ACTIVO")
        ).grid(
            row=0,
            column=1,
            padx=(0, 6)
        )

        ctk.CTkButton(
            frame,
            text="Desactivar",
            width=120,
            height=34,
            fg_color="#C0392B",
            hover_color="#A93226",
            command=lambda: self._cambiar_estado("INACTIVO")
        ).grid(
            row=0,
            column=2,
            padx=(0, 6)
        )

        ctk.CTkButton(
            frame,
            text="Refrescar",
            width=120,
            height=34,
            fg_color="gray",
            hover_color="gray30",
            command=self._cargar_clientes
        ).grid(
            row=0,
            column=3
        )

    # ============================================================
    # CARGAR CLIENTES
    # ============================================================

    def _cargar_clientes(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        clientes = self.cliente_controller.obtener_todos()

        self._llenar_tabla(clientes)

    # ============================================================
    # BUSCAR CLIENTES
    # ============================================================

    def _buscar_clientes(self):

        texto = self.entry_busqueda.get().strip()

        if not texto:
            self._cargar_clientes()
            return

        clientes = self.cliente_controller.buscar(texto)

        self._llenar_tabla(clientes)

    # ============================================================
    # LLENAR TABLA
    # ============================================================

    def _llenar_tabla(self, clientes):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for cliente in clientes:

            estado = cliente.estado.capitalize()

            self.tree.insert(
                "",
                "end",
                values=(
                    cliente.id,
                    cliente.ruc,
                    cliente.razon_social,
                    estado
                )
            )

    # ============================================================
    # FORMULARIO NUEVO CLIENTE
    # ============================================================

    def _abrir_formulario(self):

        dialogo = ctk.CTkToplevel(self)

        dialogo.title("Registrar Cliente")
        dialogo.geometry("450x330")
        dialogo.resizable(False, False)

        dialogo.transient(
            self.winfo_toplevel()
        )

        dialogo.grab_set()

        dialogo.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            dialogo,
            text="Nuevo Cliente",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            pady=(25, 20)
        )

        entry_ruc = ctk.CTkEntry(
            dialogo,
            placeholder_text="RUC",
            width=300,
            height=36
        )

        entry_ruc.grid(
            row=1,
            column=0,
            pady=(0, 10)
        )

        entry_razon_social = ctk.CTkEntry(
            dialogo,
            placeholder_text="Razón social",
            width=300,
            height=36
        )

        entry_razon_social.grid(
            row=2,
            column=0,
            pady=(0, 10)
        )

        combo_estado = ctk.CTkComboBox(
            dialogo,
            values=[
                "ACTIVO",
                "INACTIVO"
            ],
            width=300,
            height=36,
            state="readonly"
        )

        combo_estado.set("ACTIVO")

        combo_estado.grid(
            row=3,
            column=0,
            pady=(0, 20)
        )

        def registrar():

            try:

                self.cliente_controller.registrar_cliente(
                    entry_ruc.get(),
                    entry_razon_social.get(),
                    combo_estado.get()
                )

                messagebox.showinfo(
                    "Éxito",
                    "Cliente registrado correctamente."
                )

                dialogo.destroy()

                self._cargar_clientes()

            except ValueError as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"No se pudo registrar el cliente:\n{e}"
                )

        ctk.CTkButton(
            dialogo,
            text="Registrar",
            width=300,
            height=38,
            command=registrar
        ).grid(
            row=4,
            column=0,
            pady=(0, 10)
        )

    # ============================================================
    # EDITAR CLIENTE
    # ============================================================

    def _editar_cliente(self):

        seleccion = self.tree.selection()

        if not seleccion:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un cliente."
            )

            return

        valores = self.tree.item(
            seleccion[0]
        )["values"]

        cliente_id = valores[0]

        cliente = self.cliente_controller.buscar_por_ruc(
            valores[1]
        )

        if not cliente:

            messagebox.showerror(
                "Error",
                "No se encontró el cliente."
            )

            return

        dialogo = ctk.CTkToplevel(self)

        dialogo.title("Editar Cliente")
        dialogo.geometry("450x330")
        dialogo.resizable(False, False)

        dialogo.transient(
            self.winfo_toplevel()
        )

        dialogo.grab_set()

        dialogo.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            dialogo,
            text="Editar Cliente",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            pady=(25, 20)
        )

        entry_ruc = ctk.CTkEntry(
            dialogo,
            width=300,
            height=36
        )

        entry_ruc.insert(
            0,
            cliente.ruc
        )

        entry_ruc.grid(
            row=1,
            column=0,
            pady=(0, 10)
        )

        entry_razon_social = ctk.CTkEntry(
            dialogo,
            width=300,
            height=36
        )

        entry_razon_social.insert(
            0,
            cliente.razon_social
        )

        entry_razon_social.grid(
            row=2,
            column=0,
            pady=(0, 10)
        )

        combo_estado = ctk.CTkComboBox(
            dialogo,
            values=[
                "ACTIVO",
                "INACTIVO"
            ],
            width=300,
            height=36,
            state="readonly"
        )

        combo_estado.set(
            cliente.estado
        )

        combo_estado.grid(
            row=3,
            column=0,
            pady=(0, 20)
        )

        def guardar():

            try:

                self.cliente_controller.actualizar_cliente(
                    cliente_id,
                    entry_ruc.get(),
                    entry_razon_social.get(),
                    combo_estado.get()
                )

                messagebox.showinfo(
                    "Éxito",
                    "Cliente actualizado correctamente."
                )

                dialogo.destroy()

                self._cargar_clientes()

            except ValueError as e:

                messagebox.showerror(
                    "Error",
                    str(e)
                )

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"No se pudo actualizar el cliente:\n{e}"
                )

        ctk.CTkButton(
            dialogo,
            text="Guardar cambios",
            width=300,
            height=38,
            command=guardar
        ).grid(
            row=4,
            column=0
        )

    # ============================================================
    # CAMBIAR ESTADO
    # ============================================================

    def _cambiar_estado(self, estado):

        seleccion = self.tree.selection()

        if not seleccion:

            messagebox.showwarning(
                "Aviso",
                "Seleccione un cliente."
            )

            return

        valores = self.tree.item(
            seleccion[0]
        )["values"]

        cliente_id = valores[0]

        try:

            exito = self.cliente_controller.cambiar_estado(
                cliente_id,
                estado
            )

            if exito:

                self._cargar_clientes()

                messagebox.showinfo(
                    "Éxito",
                    f"Cliente {estado.lower()} correctamente."
                )

            else:

                messagebox.showerror(
                    "Error",
                    "No se pudo actualizar el estado."
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )