import customtkinter as ctk
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tkinter import messagebox
import customtkinter as ctk
from crud.ingrediente_crud import IngredienteCRUD
from crud.cliente_crud import ClienteCRUD
# Crear la conexión a la base de datos
engine = create_engine('sqlite:///restaurant.db')
Session = sessionmaker(bind=engine)
db_session = Session()

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Restaurante")
        self.geometry("800x600")
        self.configure(fg_color="white")

        # Botones de navegación
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Opciones principales
        self.create_menu_button("Clientes", ClientePanel)
        self.create_menu_button("Ingredientes", IngredientePanel)

    def create_menu_button(self, text, panel_class):
        button = ctk.CTkButton(self.menu_frame, text=text, command=lambda: self.load_panel(panel_class))
        button.pack(pady=10)

    def load_panel(self, panel_class):
        # Limpiar el panel principal y cargar un nuevo panel
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        panel_class(self.main_frame, db_session).pack(fill="both", expand=True)

class ClientePanel(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="lightgray")

        # Título del panel
        self.label_title = ctk.CTkLabel(self, text="Gestión de Clientes", font=("Arial", 20))
        self.label_title.pack(pady=10)

        # Formulario para registrar o editar un cliente
        self.nombre_entry = self.create_form_entry("Nombre del Cliente")
        self.email_entry = self.create_form_entry("Email del Cliente")

        # Botones de acciones
        self.add_button = ctk.CTkButton(self, text="Registrar Cliente", command=self.add_cliente)
        self.add_button.pack(pady=5)

        self.update_button = ctk.CTkButton(self, text="Editar Cliente", command=self.update_cliente)
        self.update_button.pack(pady=5)

        self.delete_button = ctk.CTkButton(self, text="Eliminar Cliente", command=self.delete_cliente)
        self.delete_button.pack(pady=5)

        # Lista de clientes registrados
        self.cliente_list = ctk.CTkTextbox(self, height=300)
        self.cliente_list.pack(pady=10)
        self.cliente_list.bind("<<Modified>>", lambda e: self.on_list_modified())

        # Cargar la lista de clientes al inicio
        self.refresh_list()

    def create_form_entry(self, label_text):
        """
        Crea un campo de entrada con su etiqueta correspondiente.
        """
        frame = ctk.CTkFrame(self)
        frame.pack(pady=5, padx=10, fill="x")
        
        label = ctk.CTkLabel(frame, text=label_text, width=20)
        label.pack(side="left", padx=5)
        
        entry = ctk.CTkEntry(frame)
        entry.pack(side="right", fill="x", expand=True)
        
        return entry

    def add_cliente(self):
        """
        Lógica para añadir un nuevo cliente.
        """
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
        """
        Lógica para editar un cliente seleccionado.
        """
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
        """
        Lógica para eliminar un cliente seleccionado.
        """
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
        self.cliente_list.delete("1.0", "end")
        clientes = ClienteCRUD.get_clientes(self.db)
        for cliente in clientes:
            self.cliente_list.insert("end", f"{cliente.email} | Nombre: {cliente.nombre}\\n")

    def get_selected_email(self):
        """
        Obtiene el email del cliente seleccionado en la lista.
        """
        try:
            selection = self.cliente_list.get("sel.first", "sel.last")
            email = selection.split(" | ")[0]  # Extrae el email antes de la barra vertical
            return email.strip()
        except:
            return None

class IngredientePanel(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="lightgray")

        self.label_title = ctk.CTkLabel(self, text="Gestión de Ingredientes", font=("Arial", 20))
        self.label_title.pack(pady=10)

        # Formulario de ingreso
        self.nombre_entry = self.create_form_entry("Nombre")
        self.tipo_entry = self.create_form_entry("Tipo")
        self.cantidad_entry = self.create_form_entry("Cantidad")
        self.unidad_entry = self.create_form_entry("Unidad de Medida")

        self.add_button = ctk.CTkButton(self, text="Añadir Ingrediente", command=self.add_ingrediente)
        self.add_button.pack(pady=10)

        # Lista de ingredientes
        self.ingrediente_list = ctk.CTkTextbox(self, height=300)
        self.ingrediente_list.pack(pady=10)

        self.refresh_list()

    def create_form_entry(self, label_text):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=5, padx=10)
        label = ctk.CTkLabel(frame, text=label_text)
        label.pack(side="left", padx=5)
        entry = ctk.CTkEntry(frame)
        entry.pack(side="right", fill="x", expand=True)
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
