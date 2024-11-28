import customtkinter as ctk
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tkinter import messagebox
import customtkinter as ctk
from crud.ingrediente_crud import IngredienteCRUD
from crud.cliente_crud import ClienteCRUD
from crud.menu_crud import MenuCRUD
from crud.pedido_crud import PedidoCRUD
from database import get_db, engine, Base

# Configuración global de estilos
ctk.set_appearance_mode("dark")  # Opciones: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Opciones: "blue", "green", "dark-blue"

Base.metadata.create_all(bind=engine)

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("1000x700")
        self.configure(fg_color="#1c1c1c")  # Fondo oscuro

        # Menú lateral
        self.menu_frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)

        # Contenedor principal
        self.main_frame = ctk.CTkFrame(self, fg_color="#1c1c1c", corner_radius=10)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Título del menú
        self.app_title = ctk.CTkLabel(self.menu_frame, text="Restaurante App", font=("Arial", 24, "bold"))
        self.app_title.pack(pady=20)

        # Botones de navegación
        self.create_menu_button("Clientes", ClientePanel)
        self.create_menu_button("Ingredientes", IngredientePanel)

    def create_menu_button(self, text, panel_class):
        button = ctk.CTkButton(
            self.menu_frame,
            text=text,
            command=lambda: self.load_panel(panel_class),
            font=("Arial", 16, "bold"),
            corner_radius=10,
            height=40,
            fg_color="#3c99dc",
            hover_color="#4da9eb",
        )
        button.pack(pady=15, padx=10)

    def load_panel(self, panel_class):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        db_session = next(get_db())
        panel_class(self.main_frame, db_session).pack(fill="both", expand=True)

class ClientePanel(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="#1c1c1c")

        self.label_title = ctk.CTkLabel(self, text="Gestión de Clientes", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=10)

        # Formulario
        self.nombre_entry = self.create_form_entry("Nombre del Cliente")
        self.email_entry = self.create_form_entry("Email del Cliente")

        # Botones de acción
        self.add_button = ctk.CTkButton(self, text="Registrar Cliente", command=self.add_cliente, corner_radius=10)
        self.add_button.pack(pady=10)

        self.update_button = ctk.CTkButton(self, text="Editar Cliente", command=self.update_cliente, corner_radius=10)
        self.update_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self, text="Eliminar Cliente", command=self.delete_cliente, corner_radius=10)
        self.delete_button.pack(pady=10)

        # Lista de clientes
        self.cliente_list = ctk.CTkTextbox(self, height=450, width=300, corner_radius=10)  
        self.cliente_list.pack(pady=10)
        self.cliente_list.configure(state="disabled")

        # Actualizar lista al inicio
        self.refresh_list()
        

    def create_form_entry(self, label_text):
        frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        frame.pack(pady=10, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14))
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10)
        entry.pack(side="right", fill="x", expand=True, padx=10)

        return entry

    def add_cliente(self):
        nombre = self.nombre_entry.get()
        email = self.email_entry.get()

        if not nombre or not email:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        cliente = ClienteCRUD.create_cliente(self.db, nombre, email)
        if cliente:
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' registrado con éxito.")
            self.refresh_list()
        else:
            messagebox.showerror("Error", f"El cliente con el email '{email}' ya existe.")

    def update_cliente(self):
        email_actual = self.get_selected_email()
        if not email_actual:
            messagebox.showerror("Error", "Debes seleccionar un cliente de la lista.")
            return

        nuevo_nombre = self.nombre_entry.get()
        nuevo_email = self.email_entry.get()

        if not nuevo_nombre or not nuevo_email:
            messagebox.showerror("Error", "Todos los campos son obligatorios para actualizar un cliente.")
            return

        cliente = ClienteCRUD.update_cliente(self.db, email_actual, nuevo_nombre, nuevo_email)
        if cliente:
            messagebox.showinfo("Éxito", f"Cliente '{email_actual}' actualizado con éxito.")
            self.refresh_list()
        else:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente '{email_actual}'.")

    def delete_cliente(self):
        cliente_email = self.get_selected_email()
        if not cliente_email:
            messagebox.showerror("Error", "Debes seleccionar un cliente de la lista.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar al cliente '{cliente_email}'?")
        if confirm:
            cliente = ClienteCRUD.delete_cliente(self.db, cliente_email)
            if cliente:
                messagebox.showinfo("Éxito", f"Cliente '{cliente_email}' eliminado con éxito.")
                self.refresh_list()
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente '{cliente_email}'.")

    def refresh_list(self):
        """
        Actualiza la lista de clientes mostrada en la interfaz.
        """
    # Habilitar temporalmente el TextBox para modificar su contenido
        self.cliente_list.configure(state="normal")  
        self.cliente_list.delete("1.0", "end")  # Limpiar el contenido actual

    # Obtener la lista de clientes desde la base de datos
        clientes = ClienteCRUD.get_clientes(self.db)
        if clientes:
            for cliente in clientes:
                self.cliente_list.insert("end", f"{cliente.email} | Nombre: {cliente.nombre}\n")
        else:
            self.cliente_list.insert("end", "No hay clientes registrados.\n")

        # Volver a deshabilitar el TextBox para evitar interacción
        self.cliente_list.configure(state="disabled")

    def get_selected_email(self):
        try:
            selection = self.cliente_list.get("sel.first", "sel.last")
            email = selection.split(" | ")[0]
            return email.strip()
        except:
            return None


class IngredientePanel(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="#1c1c1c")

        self.label_title = ctk.CTkLabel(self, text="Gestión de Ingredientes", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=10)

        self.nombre_entry = self.create_form_entry("Nombre")
        self.tipo_entry = self.create_form_entry("Tipo")
        self.cantidad_entry = self.create_form_entry("Cantidad")
        self.unidad_entry = self.create_form_entry("Unidad de Medida")

        self.add_button = ctk.CTkButton(self, text="Añadir Ingrediente", command=self.add_ingrediente, corner_radius=10)
        self.add_button.pack(pady=10)

        self.ingrediente_list = ctk.CTkTextbox(self, height=300, corner_radius=10)
        self.ingrediente_list.pack(pady=10)
        self.ingrediente_list.configure(state="disabled")

        self.refresh_list()

    def create_form_entry(self, label_text):
        frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        frame.pack(pady=5, padx=10)

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14))
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10)
        entry.pack(side="right", fill="x", expand=True, padx=10)

        return entry

    def add_ingrediente(self):
        nombre = self.nombre_entry.get()
        tipo = self.tipo_entry.get()
        cantidad = self.cantidad_entry.get()
        unidad = self.unidad_entry.get()

        if not nombre or not tipo or not cantidad or not unidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            cantidad = float(cantidad)
            ingrediente = IngredienteCRUD.create_ingrediente(self.db, nombre, tipo, cantidad, unidad)
            if ingrediente:
                messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' añadido con éxito.")
            else:
                messagebox.showerror("Error", f"El ingrediente '{nombre}' ya existe.")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número.")
        finally:
            self.refresh_list()

    def refresh_list(self):
        self.ingrediente_list.delete("1.0", "end")
        ingredientes = IngredienteCRUD.get_ingredientes(self.db)
        for ingrediente in ingredientes:
            self.ingrediente_list.insert("end", f"{ingrediente.nombre} ({ingrediente.tipo}) - {ingrediente.cantidad} {ingrediente.unidad}\n")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
