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
from models import Pedido,Ingrediente,Cliente,MenuIngrediente,Pedido,Menu
from tkinter import ttk


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
        self.create_menu_button("Menu", MenuPanel)
        self.create_menu_button("Panel de compra", PanelCompra)
        self.create_menu_button("Pedidos", PanelPedido)
        self.create_menu_button("Graficos", IngredientePanel)

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

        # Título
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
        self.cliente_list = self.create_treeview(Cliente)
        self.cliente_list.pack(pady=20)
        self.refresh_list()

    def create_treeview(self, model_class):
        columns = [column.name for column in model_class.__table__.columns]
        treeview = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            treeview.heading(column, text=column.capitalize())
        return treeview

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
        else:
            messagebox.showerror("Error", f"El cliente con el email '{email}' ya existe.")
        self.refresh_list()

    def update_cliente(self):
        email_actual = self.get_selected_email()
        if not email_actual:
            messagebox.showerror("Error", "Selecciona un cliente de la lista.")
            return

        nuevo_nombre = self.nombre_entry.get()
        nuevo_email = self.email_entry.get()

        if not nuevo_nombre or not nuevo_email:
            messagebox.showerror("Error", "Todos los campos son obligatorios para actualizar un cliente.")
            return

        cliente = ClienteCRUD.update_cliente(self.db, email_actual, nuevo_nombre, nuevo_email)
        if cliente:
            messagebox.showinfo("Éxito", f"Cliente '{email_actual}' actualizado con éxito.")
        else:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente '{email_actual}'.")
        self.refresh_list()

    def delete_cliente(self):
        email_actual = self.get_selected_email()
        if not email_actual:
            messagebox.showerror("Error", "Selecciona un cliente de la lista.")
            return

        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar al cliente '{email_actual}'?")
        if confirm:
            cliente = ClienteCRUD.delete_cliente(self.db, email_actual)
            if cliente:
                messagebox.showinfo("Éxito", f"Cliente '{email_actual}' eliminado con éxito.")
            else:
                messagebox.showerror("Error", f"No se pudo eliminar el cliente '{email_actual}'.")
        self.refresh_list()

    def refresh_list(self):
        for item in self.cliente_list.get_children():
            self.cliente_list.delete(item)
        clientes = ClienteCRUD.get_clientes(self.db)
        for cliente in clientes:
            self.cliente_list.insert("", "end", values=(cliente.email, cliente.nombre))

    def get_selected_email(self):
        selected_item = self.cliente_list.selection()
        if selected_item:
            return self.cliente_list.item(selected_item)["values"][0]
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

        self.ingrediente_list = self.create_treeview(Ingrediente)
        self.ingrediente_list.pack(pady=10)
        self.refresh_list()

    def create_treeview(self, model_class):
        columns = [column.name for column in model_class.__table__.columns]
        treeview = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            treeview.heading(column, text=column.capitalize())
        return treeview

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
        for item in self.ingrediente_list.get_children():
            self.ingrediente_list.delete(item)
        ingredientes = IngredienteCRUD.get_ingredientes(self.db)
        for ingrediente in ingredientes:
            self.ingrediente_list.insert("", "end", values=(ingrediente.nombre, ingrediente.tipo, ingrediente.cantidad, ingrediente.unidad))


class MenuPanel(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="#1c1c1c")

        self.label_title = ctk.CTkLabel(self, text="Gestión de Menú", font=("Arial", 22, "bold"))
        self.label_title.pack(pady=10)

        self.nombre_entry = self.create_form_entry("Nombre del Menú")
        self.descripcion_entry = self.create_form_entry("Descripción del Menú")

        self.add_button = ctk.CTkButton(self, text="Registrar Menú", command=self.add_menu, corner_radius=10)
        self.add_button.pack(pady=10)

        self.update_button = ctk.CTkButton(self, text="Editar Menú", command=self.update_menu, corner_radius=10)
        self.update_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(self, text="Eliminar Menú", command=self.delete_menu, corner_radius=10)
        self.delete_button.pack(pady=10)

        # Lista de menús
        self.menu_list = self.create_treeview(Menu)
        self.menu_list.pack(pady=20)
        self.refresh_list()

    def create_treeview(self, model_class):
        columns = [column.name for column in model_class.__table__.columns]
        treeview = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            treeview.heading(column, text=column.capitalize())
        return treeview

    def create_form_entry(self, label_text):
        frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        frame.pack(pady=10, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14))
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10)
        entry.pack(side="right", fill="x", expand=True, padx=10)

        return entry

    def add_menu(self):
        nombre = self.nombre_entry.get()
        descripcion = self.descripcion_entry.get()

        if not nombre or not descripcion:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Aquí deberías pasar una lista de ingredientes para asociar al menú
        ingredientes = []  # Asocia aquí los ingredientes que se desean al menú

        menu = MenuCRUD.create_menu(self.db, nombre, descripcion, ingredientes)
        if menu:
            messagebox.showinfo("Éxito", f"Menú '{nombre}' registrado con éxito.")
        else:
            messagebox.showerror("Error", f"Error al registrar el menú '{nombre}'.")
        self.refresh_list()

    def update_menu(self):
        # Aquí deberías implementar la lógica para actualizar un menú seleccionado
        pass

    def delete_menu(self):
        # Aquí deberías implementar la lógica para eliminar un menú seleccionado
        pass

    def refresh_list(self):
        for item in self.menu_list.get_children():
            self.menu_list.delete(item)
        menus = MenuCRUD.get_menus(self.db)  # Llama al método get_menus para obtener los menús
        for menu in menus:
            self.menu_list.insert("", "end", values=(menu.nombre, menu.descripcion))


class PanelCompra(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db  
        self.configure(fg_color="#1c1c1c")

        # Título del Panel de Compra
        self.label_title = ctk.CTkLabel(self, text="Panel de Compra", font=("Arial", 24, "bold"), text_color="white")
        self.label_title.pack(pady=20)

        # Frame para la entrada de productos y cantidad
        self.entry_frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        self.entry_frame.pack(pady=10, fill="x", padx=20)

        # Combobox para seleccionar un menú
        self.menu_combobox = ctk.CTkComboBox(self.entry_frame, values=[], width=300, corner_radius=10)
        self.menu_combobox.set("Selecciona un menú")  # Texto por defecto
        self.menu_combobox.pack(side="left", padx=10)

        # Botón para cargar los menús en el Combobox
        self.load_menus_button = ctk.CTkButton(self.entry_frame, text="Cargar Menús", command=self.load_menus, corner_radius=10)
        self.load_menus_button.pack(side="left", padx=10)

        # Entrada de cantidad
        self.cantidad_entry = self.create_form_entry("Cantidad", width=150)
        self.cantidad_entry.pack(side="left", padx=10)

        # Botón para agregar al carrito
        self.add_button = ctk.CTkButton(self.entry_frame, text="Agregar al carrito", command=self.add_to_cart, corner_radius=10)
        self.add_button.pack(side="left", padx=10)

        # Lista de productos en el carrito
        self.cart_list = ctk.CTkTextbox(self, height=200, width=500, corner_radius=10, wrap="word", state="disabled", font=("Arial", 14))
        self.cart_list.pack(pady=10)
        self.cart_list.configure(state="disabled")

        # Botón para realizar compra
        self.buy_button = ctk.CTkButton(self, text="Realizar Compra", command=self.complete_purchase, corner_radius=10, fg_color="#3c99dc")
        self.buy_button.pack(pady=10)

        # Label para el total
        self.total_label = ctk.CTkLabel(self, text="Total: $0.00", font=("Arial", 16, "bold"), text_color="white")
        self.total_label.pack(pady=10)

        # Lista interna para almacenar los productos seleccionados
        self.cart = []  # Aquí guardaremos los productos y cantidades seleccionadas

    def create_form_entry(self, label_text, width=200):
        frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        frame.pack(pady=10, padx=10, fill="x")

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14), text_color="white")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10, width=width)
        entry.pack(side="right", fill="x", expand=True, padx=10)

        return entry

    def load_menus(self):
        # Cargar los menús desde la Base de datos
        menus = MenuCRUD.get_menus(self.db)
        menu_names = [menu.nombre for menu in menus]
        
        if not menu_names:
            messagebox.showinfo("Sin menús", "No hay menús disponibles en el sistema.")
            return

        # Actualizar el combobox con los menús cargados
        self.menu_combobox.configure(values=menu_names)

    def add_to_cart(self):
        # Obtener el menú seleccionado del combobox
        selected_menu = self.menu_combobox.get()
        cantidad = self.cantidad_entry.get()

        if selected_menu == "Selecciona un menú":
            messagebox.showerror("Error", "Por favor, selecciona un menú.")
            return

        if not cantidad:
            messagebox.showerror("Error", "La cantidad es obligatoria.")
            return

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor que cero.")
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        # Simular la obtención del precio del menú desde la Base de datos
        menu = next((menu for menu in MenuCRUD.get_menus(self.db) if menu.nombre == selected_menu), None)
        if menu:
            # Puedes añadir detalles adicionales si es necesario (como los ingredientes y sus precios)
            precio = self.calculate_menu_price(menu)  # Obtener el precio total del menú

            total_producto = precio * cantidad
            self.cart.append((selected_menu, cantidad, total_producto))

            self.refresh_cart_list()
            self.cantidad_entry.delete(0, "end")  # Limpiar la cantidad

        else:
            messagebox.showerror("Error", "No se pudo encontrar el menú seleccionado.")

    def refresh_cart_list(self):
        self.cart_list.configure(state="normal")
        self.cart_list.delete("1.0", "end")

        total = 0
        for item in self.cart:
            producto, cantidad, total_producto = item
            self.cart_list.insert("end", f"{producto} x{cantidad} - ${total_producto:.2f}\n")
            total += total_producto

        self.cart_list.configure(state="disabled")
        self.update_total(total)

    def update_total(self, total):
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def complete_purchase(self):
        if not self.cart:
            messagebox.showerror("Error", "No hay productos en el carrito.")
            return

        # Aquí puedes agregar la lógica para guardar la compra en la Base de datos
        # Por ejemplo, crear un registro de compra y asociar los productos.

        messagebox.showinfo("Compra Realizada", "¡Gracias por tu compra!")
        self.cart.clear()
        self.refresh_cart_list()

    def calculate_menu_price(self, menu):
        # Simular la obtención del precio de un menú
        # Puedes calcular el precio total del menú sumando el precio de los ingredientes
        precio_total = 0
        for item in menu.ingredientes:
            precio_total += item.ingrediente.precio * item.cantidad
        return precio_total



class PanelPedido(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db  # Recibe la sesión de la Base de datos
        self.configure(fg_color="#1c1c1c")

        # Título del Panel de Pedido
        self.label_title = ctk.CTkLabel(self, text="Panel de Pedidos", font=("Arial", 24, "bold"), text_color="white")
        self.label_title.pack(pady=20)

        self.pedido_list = self.create_treeview(Pedido)
        self.pedido_list.pack(pady=20)
        self.refresh_list()

    def create_treeview(self, model_class):
        columns = [column.name for column in model_class.__table__.columns]
        treeview = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            treeview.heading(column, text=column.capitalize())
        return treeview

    def refresh_list(self):
        for item in self.pedido_list.get_children():
            self.pedido_list.delete(item)
        pedidos = PedidoCRUD.leer_pedidos(self.db)
        for pedido in pedidos:
            self.pedido_list.insert("", "end", values=(pedido.id, pedido.descripcion, pedido.total, pedido.fecha, pedido.cliente_email))


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
