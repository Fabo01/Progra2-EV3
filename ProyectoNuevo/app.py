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
from fpdf import FPDF
from tkinter import messagebox as CTkM
from datetime import datetime
import tkinter as tk
import matplotlib.pyplot as plt
from graficos import  graficar_menus_mas_comprados, graficar_uso_ingredientes,graficar_ventas_por_fecha

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
        self.menu_frame.grid(row=0, column=0, sticky="ns", padx=10, pady=10)

        # Contenedor principal
        self.main_frame = ctk.CTkFrame(self, fg_color="#1c1c1c", corner_radius=10, width=800, height=700)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Título del menú
        self.app_title = ctk.CTkLabel(self.menu_frame, text="Restaurante App", font=("Arial", 24, "bold"))
        self.app_title.grid(row=0, column=0, pady=20)

        # Botones de navegación
        self.create_menu_button("Clientes", ClientePanel, 1)
        self.create_menu_button("Ingredientes", IngredientePanel, 2)
        self.create_menu_button("Menu", MenuPanel, 3)
        self.create_menu_button("Panel de compra", PanelCompra, 4)
        self.create_menu_button("Pedidos", PanelPedido, 5)
        self.create_menu_button("Graficos", GraficosPanel, 6)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def create_menu_button(self, text, panel_class, row):
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
        button.grid(row=row, column=0, pady=15, padx=10, sticky="ew")

    def load_panel(self, panel_class):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        db_session = next(get_db())
        panel_class(self.main_frame, db_session).grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

class ClientePanel(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="#1c1c1c")

        # Título
        self.label_title = ctk.CTkLabel(self, text="Gestión de Clientes", font=("Arial", 22, "bold"))
        self.label_title.grid(row=0, column=0, pady=10)

        # Formulario
        self.nombre_entry = self.create_form_entry("Nombre del Cliente", 1)
        self.email_entry = self.create_form_entry("Email del Cliente", 2)
        self.rut_entry = self.create_form_entry("Rut del Cliente", 3)

        # Botones de acción
        self.add_button = ctk.CTkButton(self, text="Registrar Cliente", command=self.add_cliente, corner_radius=10)
        self.add_button.grid(row=4, column=0, pady=10)

        self.update_button = ctk.CTkButton(self, text="Editar Cliente", command=self.open_edit_window, corner_radius=10)
        self.update_button.grid(row=5, column=0, pady=10)

        self.delete_button = ctk.CTkButton(self, text="Eliminar Cliente", command=self.delete_cliente, corner_radius=10)
        self.delete_button.grid(row=6, column=0, pady=10)

        # Lista de clientes
        self.cliente_list = self.create_treeview(Cliente)
        self.cliente_list.grid(row=7, column=0, pady=20, sticky="nsew")
        self.cliente_list.bind("<<TreeviewSelect>>", self.on_select)  # Bind select event
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.refresh_list()

    def create_treeview(self, model_class):
        columns = [column.name for column in model_class.__table__.columns]
        treeview = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            treeview.heading(column, text=column.capitalize())
        return treeview

    def create_form_entry(self, label_text, row):
        frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        frame.grid(row=row, column=0, pady=10, padx=10, sticky="ew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14))
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10)
        entry.pack(side="right", fill="x", expand=True, padx=10)

        return entry

    def add_cliente(self):
        rut = self.rut_entry.get()
        email = self.email_entry.get()
        nombre = self.nombre_entry.get()
        
        if not nombre or not email:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        cliente_existente = ClienteCRUD.get_cliente_by_rut(self.db, rut)
        if cliente_existente:
            messagebox.showinfo("Error", f"El cliente con el rut'{rut}' ya existe.")
            return
        else:
            cliente = ClienteCRUD.create_cliente(self.db, rut, nombre, email)
            if cliente:
                messagebox.showinfo("Éxito", f"Cliente '{nombre}' registrado con éxito.")
            else:
                messagebox.showerror("Error", f"No se pudo registrar el cliente '{nombre}'.")
            self.refresh_list()
        self.refresh_list()

    def open_edit_window(self):
        selected_item = self.cliente_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un cliente de la lista.")
            return
        cliente_rut = self.cliente_list.item(selected_item)["values"][0]  # Cambia el índice para obtener el rut
        cliente = ClienteCRUD.get_cliente_by_rut(self.db, cliente_rut)

        if cliente:
            self.edit_window = ctk.CTkToplevel(self)
            self.edit_window.title("Editar Cliente")
            self.edit_window.geometry("400x300")
            self.edit_window.configure(fg_color="#1c1c1c")

            self.edit_nombre_entry = self.create_form_entry_in_window("Nombre del Cliente", 1, cliente.nombre)
            self.edit_email_entry = self.create_form_entry_in_window("Email del Cliente", 2, cliente.email)
            self.edit_rut_entry = self.create_form_entry_in_window("Rut del Cliente", 3, cliente.rut)
            self.edit_rut_entry.configure(state="disabled")

            self.save_button = ctk.CTkButton(self.edit_window, text="Guardar Cambios", command=lambda: self.update_cliente(cliente_rut), corner_radius=10)
            self.save_button.grid(row=5, column=0, pady=10)

    def create_form_entry_in_window(self, label_text, row, value):
        frame = ctk.CTkFrame(self.edit_window, fg_color="#2c2c2c", corner_radius=10)
        frame.grid(row=row, column=0, pady=5, padx=10, sticky="ew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14))
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10, width=200)
        entry.insert(0, value)
        entry.pack(side="right", fill="x", expand=True, padx=10)

        return entry
    
    def update_cliente(self, cliente_rut):
        nombre = self.edit_nombre_entry.get()
        email = self.edit_email_entry.get()
        rut = self.edit_rut_entry.get()

        if not nombre or not email:
            messagebox.showerror("Error", "Todos los campos son obligatorios para actualizar un cliente.")
            return

        cliente = ClienteCRUD.update_cliente(self.db, cliente_rut, nombre, email, rut)
        if cliente:
            messagebox.showinfo("Éxito", f"Cliente n°rut:'{rut}' y Nombre:'{nombre}' actualizado con éxito.")
            self.edit_window.destroy()
        else:
            messagebox.showerror("Error", f"No se pudo actualizar el cliente '{nombre}//{rut}'.")
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
            self.cliente_list.insert("", "end", values=(cliente.rut, cliente.email, cliente.nombre))  # Asegúrate de incluir el rut

    def get_selected_email(self):
        selected_item = self.cliente_list.selection()
        if selected_item:
            return self.cliente_list.item(selected_item)["values"][1]  # Cambia el índice para obtener el email
        return None

    def on_select(self, event):
        selected_item = self.cliente_list.selection()
        if selected_item:
            values = self.cliente_list.item(selected_item)["values"]
            self.rut_entry.delete(0, tk.END)
            self.rut_entry.insert(0, values[0])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[1])
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, values[2])

class IngredientePanel(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="#1c1c1c")

        self.label_title = ctk.CTkLabel(self, text="Gestión de Ingredientes", font=("Arial", 22, "bold"))
        self.label_title.grid(row=0, column=0, pady=10)

        self.nombre_entry = self.create_form_entry("Nombre", 1)
        self.tipo_entry = self.create_form_entry("Tipo", 2)
        self.cantidad_entry = self.create_form_entry("Cantidad", 3)
        self.unidad_entry = self.create_form_entry("Unidad de Medida", 4)

        self.add_button = ctk.CTkButton(self, text="Añadir Ingrediente", command=self.add_ingrediente, corner_radius=10)
        self.add_button.grid(row=5, column=0, pady=10)

        self.upgrade_button = ctk.CTkButton(self, text="Actualizar Ingrediente", command=self.open_edit_window, corner_radius=10)
        self.upgrade_button.grid(row=6, column=0, pady=10)

        self.delete_button = ctk.CTkButton(self, text="Eliminar Ingrediente", command=self.delete_ingrediente, corner_radius=10)
        self.delete_button.grid(row=7, column=0, pady=10)

        self.ingrediente_list = self.create_treeview(Ingrediente)
        self.ingrediente_list.grid(row=8, column=0, pady=10, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.refresh_list()

    def create_treeview(self, model_class):
        columns = [column.name for column in model_class.__table__.columns if column.name != 'id']
        treeview = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            treeview.heading(column, text=column.capitalize())
        return treeview

    def create_form_entry(self, label_text, row):
        frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        frame.grid(row=row, column=0, pady=5, padx=10, sticky="ew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14))
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10, width=200)
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

        ingrediente_existente = IngredienteCRUD.get_ingrediente_by_nombre(self.db, nombre)
        if ingrediente_existente:
            messagebox.showerror("Error", f"El ingrediente '{nombre}' ya existe.")
            return
        try:
            cantidad = float(cantidad)
            ingrediente = IngredienteCRUD.create_ingrediente(self.db, nombre, tipo, cantidad, unidad)
            if ingrediente:
                messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' añadido con éxito.")
            else:
                messagebox.showerror("Error", f"Error al registrar el ingrediente '{nombre}'.")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número.")
        finally:
            self.refresh_list()

    def open_edit_window(self):
        selected_item = self.ingrediente_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un ingrediente de la lista.")
            return
        
        ingrediente_nombre = self.ingrediente_list.item(selected_item)["values"][0]
        ingrediente = IngredienteCRUD.get_ingrediente_by_nombre(self.db, ingrediente_nombre)

        if ingrediente:
            self.edit_window = ctk.CTkToplevel(self)
            self.edit_window.title("Editar Ingrediente")
            self.edit_window.geometry("400x300")
            self.edit_window.configure(fg_color="#1c1c1c")
            
            self.edit_nombre_entry = self.create_form_entry_in_window("Nombre", 1, ingrediente.nombre)  # Cambia el índice
            self.edit_tipo_entry = self.create_form_entry_in_window("Tipo", 2, ingrediente.tipo)    
            self.edit_cantidad_entry = self.create_form_entry_in_window("Cantidad", 3, ingrediente.cantidad)
            self.edit_unidad_entry = self.create_form_entry_in_window("Unidad de Medida", 4, ingrediente.unidad)

            self.save_button = ctk.CTkButton(self.edit_window, text="Guardar Cambios", command=lambda: self.update_ingrediente(ingrediente.id), corner_radius=10)
            self.save_button.grid(row=5, column=0, pady=10)

    def create_form_entry_in_window(self, label_text, row, value):
        frame = ctk.CTkFrame(self.edit_window, fg_color="#2c2c2c", corner_radius=10)
        frame.grid(row=row, column=0, pady=5, padx=10, sticky="ew") 

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14))
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10, width=200)   
        entry.insert(0, value)
        entry.pack(side="right", fill="x", expand=True, padx=10)    

        return entry    
    
    def update_ingrediente(self, ingrediente_id):
        nombre = self.edit_nombre_entry.get()   
        tipo = self.edit_tipo_entry.get()
        cantidad = self.edit_cantidad_entry.get()
        unidad = self.edit_unidad_entry.get()   

        if not nombre or not tipo or not cantidad or not unidad:    
            messagebox.showerror("Error", "Todos los campos son obligatorios para actualizar un ingrediente.")
            return
        
        try:
            cantidad = float(cantidad)
            ingrediente = IngredienteCRUD.update_ingrediente(self.db, ingrediente_id, cantidad, tipo, unidad)
            if ingrediente:
                messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' actualizado con éxito.")
                self.edit_window.destroy()
            else:
                messagebox.showerror("Error", f"Error al actualizar el ingrediente '{nombre}'.")
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número.")
        finally:
            self.refresh_list()

    def delete_ingrediente(self):
        selected_item = self.ingrediente_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un ingrediente de la lista.")
            return
        
        ingrediente_id = self.ingrediente_list.item(selected_item)["values"][0]  # Cambia el índice
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el ingrediente '{ingrediente.nombre}'?")
        if confirm:
            ingrediente = IngredienteCRUD.delete_ingrediente(self.db, ingrediente_id)
            if ingrediente:
                messagebox.showinfo("Éxito", "Ingrediente eliminado con éxito.")
            else:
                messagebox.showerror("Error", "Error al eliminar el ingrediente.")
        self.refresh_list()

    def refresh_list(self):
        for item in self.ingrediente_list.get_children():
            self.ingrediente_list.delete(item)
        ingredientes = IngredienteCRUD.get_ingredientes(self.db)
        for ingrediente in ingredientes:
            self.ingrediente_list.insert("", "end", values=(ingrediente.nombre, ingrediente.tipo, ingrediente.cantidad, ingrediente.unidad))
        
    def on_select(self, event):
        selected_item = self.ingrediente_list.selection()
        if selected_item:
            values = self.ingrediente_list.item(selected_item)["values"]
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, values[0])
            self.tipo_entry.delete(0, tk.END)
            self.tipo_entry.insert(0, values[1])
            self.cantidad_entry.delete(0, tk.END)
            self.cantidad_entry.insert(0, values[2])
            self.unidad_entry.delete(0, tk.END)
            self.unidad_entry.insert(0, values[3])
            self.ingrediente_list.insert("", "end", values=())
class MenuPanel(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="#1c1c1c")

        self.label_title = ctk.CTkLabel(self, text="Gestión de Menú", font=("Arial", 22, "bold"))
        self.label_title.grid(row=0, column=0, pady=10)

        self.nombre_entry = self.create_form_entry("Nombre del Menú", 1)
        self.descripcion_entry = self.create_form_entry("Descripción del Menú", 2)

        self.add_button = ctk.CTkButton(self, text="Registrar Menú", command=self.add_menu, corner_radius=10)
        self.add_button.grid(row=3, column=0, pady=10)

        self.update_button = ctk.CTkButton(self, text="Editar Menú", command=self.open_edit_window, corner_radius=10)
        self.update_button.grid(row=4, column=0, pady=10)

        self.delete_button = ctk.CTkButton(self, text="Eliminar Menú", command=self.delete_menu, corner_radius=10)
        self.delete_button.grid(row=5, column=0, pady=10)

        # Lista de menús
        self.menu_list = self.create_treeview(Menu)
        self.menu_list.grid(row=6, column=0, pady=20, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.refresh_list()

    def create_treeview(self, model_class):
        columns = [column.name for column in model_class.__table__.columns if column.name != 'id']
        treeview = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            treeview.heading(column, text=column.capitalize())
        return treeview

    def create_form_entry(self, label_text, row):
        frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        frame.grid(row=row, column=0, pady=10, padx=10, sticky="ew")

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

        menu_existente = MenuCRUD.get_menu_by_nombre(self.db, nombre)
        if menu_existente:
            messagebox.showerror("Error", f"El menú '{nombre}' ya existe.")
            return
            

        ingredientes = []  # Asocia aquí los ingredientes que se desean al menú

        menu = MenuCRUD.create_menu(self.db, nombre, descripcion, ingredientes)
        if menu:
            messagebox.showinfo("Éxito", f"Menú '{nombre}' registrado con éxito.")
        else:
            messagebox.showerror("Error", f"Error al registrar el menú '{nombre}'.")
        self.refresh_list()

    def open_edit_window(self):
        selected_item = self.menu_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un menú de la lista.")
            return

        menu_nombre = self.menu_list.item(selected_item)["values"][0]
        menu = MenuCRUD.get_menu_by_nombre(self.db, menu_nombre)

        if menu:
            self.edit_window = ctk.CTkToplevel(self)
            self.edit_window.title("Editar Menú")
            self.edit_window.geometry("400x300")
            self.edit_window.configure(fg_color="#1c1c1c")

            self.edit_nombre_entry = self.create_form_entry_in_window("Nombre del Menú", 1, menu.nombre)
            self.edit_descripcion_entry = self.create_form_entry_in_window("Descripción del Menú", 2, menu.descripcion)

            self.save_button = ctk.CTkButton(self.edit_window, text="Guardar Cambios", command=lambda: self.update_menu(menu.id), corner_radius=10)
            self.save_button.grid(row=5, column=0, pady=10)

    def create_form_entry_in_window(self, label_text, row, value):
        frame = ctk.CTkFrame(self.edit_window, fg_color="#2c2c2c", corner_radius=10)
        frame.grid(row=row, column=0, pady=5, padx=10, sticky="ew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14))
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10, width=200)
        entry.insert(0, value)
        entry.pack(side="right", fill="x", expand=True, padx=10)

        return entry
    
    def update_menu(self, menu_id):
        nombre = self.edit_nombre_entry.get()
        descripcion = self.edit_descripcion_entry.get()

        if not nombre or not descripcion:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        ingredientes = []  # Asocia aquí los ingredientes que se desean al menú

        menu = MenuCRUD.update_menu(self.db, menu_id, nombre, descripcion, ingredientes)
        if menu:
            messagebox.showinfo("Éxito", f"Menú '{nombre}' actualizado con éxito.")
            self.edit_window.destroy()
        else:
            messagebox.showerror("Error", f"Error al actualizar el menú '{nombre}'.")
        self.refresh_list()

    def delete_menu(self):
        selected_item = self.menu_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un menú de la lista.")
            return

        menu_id = self.menu_list.item(selected_item, 'values')[0]
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el menú '{menu_id}'?")
        if confirm:
            menu = MenuCRUD.delete_menu(self.db, menu_id)
            if menu:
                messagebox.showinfo("Éxito", f"Menú eliminado con éxito.")
            else:
                messagebox.showerror("Error", f"Error al eliminar el menú.")
        self.refresh_list()

    def refresh_list(self):
        for item in self.menu_list.get_children():
            self.menu_list.delete(item)
        menus = MenuCRUD.get_menus(self.db)  # Llama al método get_menus para obtener los menús
        for menu in menus:
            self.menu_list.insert("", "end", values=(menu.nombre, menu.descripcion))

    def on_select(self, event):
        selected_item = self.menu_list.selection()
        if selected_item:
            values = self.menu_list.item(selected_item)["values"]
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, values[0])
            self.descripcion_entry.delete(0, tk.END)
            self.descripcion_entry.insert(0, values[1])

class PanelCompra(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db  
        self.configure(fg_color="#1c1c1c")

        # Título del Panel de Compra
        self.label_title = ctk.CTkLabel(self, text="Panel de Compra", font=("Arial", 24, "bold"), text_color="white")
        self.label_title.grid(row=0, column=0, pady=20, columnspan=2) 

        # Frame para la entrada de productos y cantidad
        self.entry_frame = ctk.CTkFrame(self, fg_color="#2c2c2c", corner_radius=10)
        self.entry_frame.grid(row=1, column=0, pady=10, padx=20, sticky="ew", columnspan=2)

        # Combobox para seleccionar un menú
        self.menu_combobox = ctk.CTkComboBox(self.entry_frame, values=[], width=300, corner_radius=10)
        self.menu_combobox.set("Selecciona un menú")  # Texto por defecto
        self.menu_combobox.grid(row=0, column=0, padx=10)

        # Botón para cargar los menús en el Combobox
        self.load_menus_button = ctk.CTkButton(self.entry_frame, text="Cargar Menús", command=self.load_menus, corner_radius=10)
        self.load_menus_button.grid(row=0, column=1, padx=10)

        # Entrada de cantidad
        self.cantidad_entry = self.create_form_entry("Cantidad", 0, 2)
        self.cantidad_entry.grid(row=0, column=2, padx=10)

        # Botón para agregar al carrito
        self.add_button = ctk.CTkButton(self.entry_frame, text="Agregar al carrito", command=self.add_to_cart, corner_radius=10)
        self.add_button.grid(row=0, column=3, padx=10)

        # Lista de productos en el carrito
        self.cart_list = self.create_treeview()
        self.cart_list.grid(row=2, column=0, pady=10, sticky="nsew", columnspan=2)

        # Botón para realizar compra
        self.buy_button = ctk.CTkButton(self, text="Realizar Compra", command=self.complete_purchase, corner_radius=10, fg_color="#3c99dc")
        self.buy_button.grid(row=3, column=0, pady=10, columnspan=2)

        # Label para el total
        self.total_label = ctk.CTkLabel(self, text="Total: $0.00", font=("Arial", 16, "bold"), text_color="white")
        self.total_label.grid(row=4, column=0, pady=10, columnspan=2)

        # Lista interna para almacenar los productos seleccionados
        self.cart = []  # Aquí guardaremos los productos y cantidades seleccionadas

        self.cliente_combobox = ctk.CTkComboBox(self.entry_frame, values=[], width=300, corner_radius=10)
        self.cliente_combobox.set("Selecciona un cliente")  # Texto por defecto
        self.cliente_combobox.grid(row=0, column=4, padx=10)
    def create_form_entry(self, label_text, row, column):
        frame = ctk.CTkFrame(self.entry_frame, fg_color="#2c2c2c", corner_radius=10)
        frame.grid(row=row, column=column, pady=10, padx=10, sticky="ew")

        label = ctk.CTkLabel(frame, text=label_text, font=("Arial", 14), text_color="white")
        label.pack(side="left", padx=10)

        entry = ctk.CTkEntry(frame, corner_radius=10)
        entry.pack(side="right", fill="x", expand=True, padx=10)

        return entry

    def create_treeview(self):
        columns = ["Producto", "Cantidad", "Total"]
        treeview = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            treeview.heading(column, text=column)
        return treeview
    def load_menus(self):
        # Cargar los menús desde la Base de datos
        menus = MenuCRUD.get_menus(self.db)
        menu_names = [menu.nombre for menu in menus]
        
        if not menu_names:
            messagebox.showinfo("Sin menús", "No hay menús disponibles en el sistema.")
            return

        # Actualizar el combobox con los menús cargados
        self.menu_combobox.configure(values=menu_names)

    def load_clientes(self):

        clientes = ClienteCRUD.get_clientes(self.db)
        cliente_ruts = [cliente.rut for cliente in clientes]
        if not cliente_ruts:
            messagebox.showinfo("Sin clientes", "No hay clientes disponibles en el sistema.")
            return
        self.cliente_combobox.configure(values=cliente_ruts)

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
        for item in self.cart_list.get_children():
            self.cart_list.delete(item)
        total = 0
        for item in self.cart:
            producto, cantidad, total_producto = item
            self.cart_list.insert("","end", values=(producto, cantidad, f"${total_producto:.2f}"))
            total += total_producto

        self.update_total(total)

    def update_total(self, total):
        self.total_label.configure(text=f"Total: ${total:.2f}")

    def complete_purchase(self):
        if not self.cart:
            messagebox.showerror("Error", "No hay productos en el carrito.")
            return

        cliente_rut = self.cliente_combobox.get()
        if cliente_rut == "Selecciona un cliente":
            messagebox.showerror("Error", "Por favor, selecciona un cliente.")
            return
        
        nuevo_pedido = PedidoCRUD.create_pedido(self.db, cliente_rut=cliente_rut, descripcion="Compra Realizada", total=sum(item[2] for item in self.cart), fecha=datetime.now, menus=[{"id": menu.id, "cantidad": cantidad} for menu, cantidad, _ in self.cart])

        if nuevo_pedido:
            generador_boleta = Generarboleta(nuevo_pedido)
            generador_boleta.generar_boleta()
            messagebox.showinfo("Compra Realizada", "¡Gracias por tu compra!")
            self.cart.clear()  # Limpiar el carrito después de la compra
            self.refresh_cart_list()  # Actualizar la interfaz
            self.db.add(nuevo_pedido)
            self.db.commit()

        else:
            messagebox.showerror("Error", "No se pudo realizar la compra.")

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
        self.db = db
        self.configure(fg_color="#1c1c1c")

        # Título del Panel de Pedido
        self.label_title = ctk.CTkLabel(self, text="Panel de Pedidos", font=("Arial", 24, "bold"), text_color="white")
        self.label_title.grid(row=0, column=0, pady=20, columnspan=3)

        # Treeview para mostrar los pedidos
        self.pedido_list = self.create_treeview(Pedido)
        self.pedido_list.grid(row=1, column=0, pady=20, sticky="nsew", columnspan=3)


        

        # Botones para agregar, editar y eliminar pedidos
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.grid(row=3, column=0, pady=5, columnspan=3)

        self.btn_add = ctk.CTkButton(self.btn_frame, text="Agregar Pedido", command=self.add_pedido)
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_edit = ctk.CTkButton(self.btn_frame, text="Editar Pedido", command=self.edit_pedido)
        self.btn_edit.grid(row=0, column=1, padx=5)

        self.btn_delete = ctk.CTkButton(self.btn_frame, text="Eliminar Pedido", command=self.delete_pedido)
        self.btn_delete.grid(row=0, column=2, padx=5)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.refresh_list()

    def create_treeview(self, model_class):
        columns = [column.name for column in model_class.__table__.columns]
        treeview = ttk.Treeview(self, columns=columns, show="headings")
        for column in columns:
            treeview.heading(column, text=column.capitalize())
            treeview.column(column, anchor='center')  # Centrar el texto
        return treeview

    def refresh_list(self):
        for item in self.pedido_list.get_children():
            self.pedido_list.delete(item)
        pedidos = PedidoCRUD.leer_pedidos(self.db)
        for pedido in pedidos:
            self.pedido_list.insert("", "end", values=(pedido.id, pedido.descripcion, pedido.total, pedido.fecha, pedido.cliente_email))

    def add_pedido(self):
        nuevo_pedido = self.open_pedido_form()
        if nuevo_pedido:
            try:
                PedidoCRUD.agregar_pedido(self.db, nuevo_pedido)
                self.refresh_list()
                self.show_message("Pedido agregado exitosamente.")
            except Exception as e:
                self.show_message(f"Error al agregar pedido: {e}")

    def edit_pedido(self):
        selected_item = self.pedido_list.selection()
        if selected_item:
            pedido_id = self.pedido_list.item(selected_item)['values'][0]
            pedido = PedidoCRUD.obtener_pedido_por_id(self.db, pedido_id)
            pedido_actualizado = self.open_pedido_form(pedido)
            if pedido_actualizado:
                try:
                    PedidoCRUD.editar_pedido(self.db, pedido_actualizado)
                    self.refresh_list()
                    self.show_message("Pedido editado exitosamente.")
                except Exception as e:
                    self.show_message(f"Error al editar pedido: {e}")

    def delete_pedido(self):
        selected_item = self.pedido_list.selection()
        if selected_item:
            pedido_id = self.pedido_list.item(selected_item)['values'][0]
            try:
                PedidoCRUD.eliminar_pedido(self.db, pedido_id)
                self.refresh_list()
                self.show_message("Pedido eliminado exitosamente.")
            except Exception as e:
                self.show_message(f"Error al eliminar pedido: {e}")

    def on_item_double_click(self, event):
        self.edit_pedido()

    def open_pedido_form(self, pedido=None):
        # Lógica para abrir un formulario para agregar o editar un pedido
        pass

    def show_message(self, message):
        # Método para mostrar mensajes de confirmación o error
        message_box = ctk.CTkMessageBox(title="Información", message=message)
        message_box.show()

class GraficosPanel(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="#1c1c1c")

        # Título del Panel de Gráficos
        self.label_title = ctk.CTkLabel(self, text="Panel de Gráficos", font=("Arial", 24, "bold"), text_color="white")
        self.label_title.pack(pady=20)

        # ComboBox para seleccionar el gráfico
        self.tipo_grafico = ctk.CTkComboBox(
            self, 
            values=["Ventas por Fecha", "Menús más Comprados", "Uso de Ingredientes"],
            width=300, 
            corner_radius=10
        )
        self.tipo_grafico.set("Selecciona un gráfico")  # Texto predeterminado
        self.tipo_grafico.pack(pady=10)

        # Botón para generar el gráfico
        self.bttn_generar_grafico = ctk.CTkButton(
            self,
            text="Generar Gráfico",
            command=self.generar_grafico,
            corner_radius=10
        )
        self.bttn_generar_grafico.pack(pady=20)

        # Frame donde se dibujarán los gráficos
        self.graph_frame = ctk.CTkFrame(self, fg_color="#1c1c1c")
        self.graph_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def generar_grafico(self):
        """Genera el gráfico basado en la selección del ComboBox"""
        tipo = self.tipo_grafico.get()
        
        if tipo == "Ventas por Fecha":
            self.graficar_ventas_por_fecha()
        elif tipo == "Menús más Comprados":
            self.graficar_menus_mas_comprados()
        elif tipo == "Uso de Ingredientes":
            self.graficar_uso_ingredientes()
        else:
            CTkM(title="Error", message="Seleccione un tipo de gráfico válido.", icon="cancel")

    def graficar_ventas_por_fecha(self):
        fechas = ["2024-11-20", "2024-11-21", "2024-11-22", "2024-11-23"]
        ventas = [2000, 3500, 4000, 3000]

        plt.figure(figsize=(10, 6))
        plt.plot(fechas, ventas, marker="o", color="blue", label="Ventas")
        plt.title("Ventas por Fecha")
        plt.xlabel("Fecha")
        plt.ylabel("Total de Ventas ($)")
        plt.grid()
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        
        graficar_ventas_por_fecha(self.db)  # Esta función puede estar en un archivo 'funciones.py'
        
    def graficar_menus_mas_comprados(self):
        menus = ["Completos", "Hamburguesa", "Papas Fritas", "Pepsi"]
        cantidades = [30, 20, 50, 40]

        plt.figure(figsize=(8, 8))
        plt.pie(cantidades, labels=menus, autopct="%1.1f%%", startangle=140)
        plt.title("Distribución de Menús Más Comprados")
        plt.axis("equal")
        plt.show()

        graficar_menus_mas_comprados(self.db)

    def graficar_uso_ingredientes(self):
        ingredientes = ["Tomate", "Palta", "Pan", "Vienesa"]
        cantidades = [120, 80, 150, 100]

        plt.figure(figsize=(12, 6))
        plt.bar(ingredientes, cantidades, color="skyblue")
        plt.title("Uso de Ingredientes Basado en Todos los Pedidos")
        plt.xlabel("Ingrediente")
        plt.ylabel("Cantidad Utilizada")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        graficar_uso_ingredientes(self.db)
class Generarboleta:
    def __init__(self, pedido):
        self.pedido = pedido

    def generar_boleta(self):
        if not self.pedido.listamenuspedidos:
            CTkM(title="Pedido Vacío", message="No hay menús en el pedido para generar la boleta.", icon="warning")
            return

        # Crear una instancia de FPDF
        pdf = FPDF()
        pdf.add_page()

        # Encabezado de la boleta
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Boleta Restaurante", ln=True, align="C")
        pdf.ln(10)

        # Detalles del restaurante (se pueden personalizar)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Razón Social del Negocio", ln=True)
        pdf.cell(0, 10, "RUT: 12345678-9", ln=True)
        pdf.cell(0, 10, "Dirección: Calle Falsa 123", ln=True)
        pdf.cell(0, 10, "Teléfono: +56 9 1234 5678", ln=True)
        pdf.ln(10)

        # Detalles del pedido
        pdf.set_font("Arial", "B", 12)
        pdf.cell(50, 10, "Nombre", 1)
        pdf.cell(30, 10, "Cantidad", 1)
        pdf.cell(50, 10, "Precio Unitario", 1)
        pdf.cell(50, 10, "Subtotal", 1)
        pdf.ln()

        pdf.set_font("Arial", size=12)

        menuses = {}
        
        for menu in self.pedido.listamenuspedidos:
            if Menu.nombre in menuses:
                menuses[menu.nombre]['cantidad'] += 1
                menuses[menu.nombre]['precio_total'] += menu.precio
            else:
                menuses[menu.nombre] = {'cantidad': 1, 'precio_total': menu.precio}

        for menu, datos in menuses.items():
            pdf.cell(50, 10, menu, 1)
            pdf.cell(30, 10, str(datos['cantidad']), 1)
            pdf.cell(50, 10, f"${datos['precio_total'] / datos['cantidad']:.2f}", 1)
            pdf.cell(50, 10, f"${datos['precio_total']:.2f}", 1)
            pdf.ln()

        total = self.pedido.calctotal()
        iva = total * 0.19
        total_con_iva = total + iva
        
        # Mostrar subtotales y totales
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Subtotal: ${total:.2f}", 0, 1, "R")
        pdf.cell(0, 10, f"IVA (19%): ${iva:.2f}", 0, 1, "R")
        pdf.cell(0, 10, f"Total: ${total_con_iva:.2f}", 0, 1, "R")
        pdf.ln(10)

        pdf.set_font("Arial", "I", 12)
        pdf.cell(0, 10, "Gracias por la compra", ln=True, align="C")
        pdf.cell(0, 10, "No se aceptan devoluciones", ln=True, align="C")
        pdf.cell(0, 10, "Contacto: restaurante@gmail.com", ln=True, align="C")
        pdf.ln()

        # Guardar el archivo PDF
        rutapdf = "evaluacion3/boleta.pdf" 
        pdf.output(rutapdf)

        CTkM(title="Boleta Generada", message=f"Boleta generada con éxito en la siguiente ruta: '{rutapdf}'.", icon="info")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
