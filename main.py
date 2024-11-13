import re
import inspect
import tkinter.messagebox
from pedidos import Pedidos
from Ingredientes import Ingredientes
from menus import Menus 
import customtkinter as CTk
import tkinter 
from tkinter import ttk
from CTkMessagebox import CTkMessagebox as CTkM
from fpdf import FPDF

class Aplicacion(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Restaurant choro")
        self.geometry("1500x600")
        
        self.tabview = CTk.CTkTabview(self, 10,10)
        self.tabview.pack()

        self.stock_ing = []

        self.pedido = Pedidos()

        self.listatarjetas = []
        self.listamenus = []
        self.crearmenus()
        self.crearpestañas()

        
    def crearmenus(self):
        ing_papas = {"Papas":5}
        ing_pepsi = {"Bebida":1}
        ing_completo = {"Vienesa":1, "Pan de completo":1, "Tomate":1, "Palta":1}
        ing_hamburguesa = {"Pan de hamburguesa":1, "Lamina de queso":1, "Churrasco de carne":1}        

        papas = Menus("Papas Fritas", 500, ing_papas, "Proyecto 1/Imagenes/icono_papas_fritas_64x64.png")
        pepsi = Menus("Pepsi", 1100, ing_pepsi, "Proyecto 1/Imagenes/icono_cola_64x64.png")
        completo = Menus("Completos", 1800, ing_completo, "Proyecto 1/Imagenes/icono_hotdog_sin_texto_64x64.png")
        hamburguesa = Menus("Hamburguesa", 3500, ing_hamburguesa, "Proyecto 1/Imagenes/icono_hamburguesa_negra_64x64.png")

        self.listamenus.append(papas)
        self.listamenus.append(pepsi)
        self.listamenus.append(completo)
        self.listamenus.append(hamburguesa)

    def crearpestañas(self):
        self.tabing = self.tabview.add("Ingreso de Ingredientes")
        self.tabped = self.tabview.add("Pedido")

        self.configpestañaing()
        self.configpestañaped()

    def configpestañaing(self):
        self.ing_frame = CTk.CTkFrame(self.tabing)
        self.ing_frame.grid(row=0, column=0)

        lbl_nombre = CTk.CTkLabel(self.ing_frame, text= "Ingrese el nombre del ingrediente.")
        lbl_nombre.pack(pady=10)
        self.entry_nombre = CTk.CTkEntry(self.ing_frame)
        self.entry_nombre.pack(pady=10)

        lbl_cantidad = CTk.CTkLabel(self.ing_frame, text= "Ingrese la cantidad.")
        lbl_cantidad.pack(pady=10)
        self.entry_cantidad = CTk.CTkEntry(self.ing_frame)
        self.entry_cantidad.pack(pady=10)

        self.bttn_ingresar = CTk.CTkButton(self.ing_frame, text="Ingresar Ingrediente", command=self.ingresaring, hover_color="purple")
        self.bttn_ingresar.pack(pady=10)

        self.tabla_frame = CTk.CTkFrame(self.tabing)
        self.tabla_frame.grid(row=0, column=1, padx=20)

        self.bttn_eliminar = CTk.CTkButton(self.tabla_frame, text="Eliminar Ingrediente.", command=self.eliminaring, hover_color="red")
        self.bttn_eliminar.grid(row=0, column=1, pady=10)

        self.bttn_menu = CTk.CTkButton(self.tabla_frame, text="Generar Menu.", command=self.generarmenus, hover_color="green")
        self.bttn_menu.grid(row=2, column=1, pady=10)

        atributos = inspect.getfullargspec(Ingredientes.__init__).args 
        atributos.remove('self')  # Remover 'self'

        self.tablalista = ttk.Treeview(self.tabla_frame, columns=atributos, show="headings")

        for atributo in atributos:
            self.tablalista.heading(atributo, text=atributo.capitalize())

        self.tablalista.grid(row=1, column=1)
    
    def configpestañaped(self):
        self.img_frame = CTk.CTkFrame(self.tabped)
        self.img_frame.grid(row=0, column=0)

        self.total_frame = CTk.CTkFrame(self.tabped)
        self.total_frame.grid(row=1, column=0, sticky="e")

    
        self.lbl_total = CTk.CTkLabel(self.total_frame, text=f"El Total del pedido es: $0")
        self.lbl_total.grid(row=0, column=0, padx=20, sticky="e")

        bttn_delete = CTk.CTkButton(self.total_frame, text="Eliminar Menu.", command=self.eliminarmenu)
        bttn_delete.grid(row=0, column=1, padx=20, sticky="e")

        self.menus_frame = CTk.CTkFrame(self.tabped)
        self.menus_frame.grid(row=2, column=0) 

        self.tablamenus = ttk.Treeview(self.menus_frame, columns=("nombre", "cantidad", "total"), show="headings")
        self.tablamenus.heading("nombre", text="Nombre del Menu")
        self.tablamenus.heading("cantidad", text="Cantidad")
        self.tablamenus.heading("total", text="Precio Total")

        self.tablamenus.grid(row=0, column=0) 

        self.bttn_pdf = CTk.CTkButton(self.menus_frame, text="Generar boleta.", command=self.generarboleta)
        self.bttn_pdf.grid(row=1, pady=25)

    def validar_nombre(self, nombre, cantidad):
            if not re.match(r"^[a-zA-Z\s]+$", nombre):
                CTkM(title="Error", message="El nombre solo puede contener letras", icon="cancel")
                return False 

            if not cantidad.isdigit() or int(cantidad) <= 0:
                CTkM(title="Error", message="La cantidad debe ser un número positivo", icon="cancel")
                return False
            
            return True

    def ingresaring(self):
        nombre = self.entry_nombre.get()
        Nombre = nombre.capitalize()
        cantidad = self.entry_cantidad.get()

        if self.validar_nombre(Nombre, cantidad):
            ing = Ingredientes(Nombre, cantidad)       
            atributos_nuevos = dict(vars(ing))
            cantidad_nueva = atributos_nuevos.pop("cantidad")
            for ingexistente in self.stock_ing:
                atributos_existentes = dict(vars(ingexistente))
                atributos_existentes.pop("cantidad")
                if atributos_existentes == atributos_nuevos:
                    ingexistente.cantidad = cantidad_nueva
                    self.actutablaing()
                    return True
            ing.cantidad = cantidad_nueva    
            self.stock_ing.append(ing)
            self.actutablaing()
            CTkM(title="Éxito", message="Ingrediente agregado correctamente", icon="check" )
            return True

    def eliminaring(self):
        ing = self.tablalista.focus()
        if not ing:
            CTkM(title="Error", message="Seleccione un ingrediente a eliminar.", icon="warning")
            return
        confirmacion = tkinter.messagebox.askyesno(title="Confirmacion", message="¿Esta seguro de eliminar la existencia de este ingrediente?")
        if confirmacion:
            Nombre = self.tablalista.item(ing, "values")[0]      
            for ing in self.stock_ing:
                if ing.nombre == Nombre:
                    self.stock_ing.remove(ing)
            self.actutablaing()
            self.actutablamenus()        
            CTkM(title="Exito", message="Ingrediente eliminado.", icon="warning") 
            return True

    def generarmenus(self):
        for tarjetas in self.listatarjetas:
            tarjetas.destroy()   

        for menu in self.listamenus:
            mcantidad = menu.verificardisp({ing.nombre: int(ing.cantidad) for ing in self.stock_ing})
            if mcantidad > 0:
                self.crear_tarjeta(menu)
            else:
                CTkM(title="Ingredientes Insuficientes", message=f"No hay suficientes ingredientes para crear el menú '{menu.nombre}'.", icon="warning")

    def eliminarmenu(self):
        menu = self.tablamenus.focus()
        if not menu:
            CTkM(title="Error", message="Seleccione un Menu a eliminar.", icon="warning")
            return
        confirmacion = tkinter.messagebox.askyesno(title="Confirmacion", message="¿Esta seguro de eliminar la existencia de este Menu?")
        if confirmacion:
            Nombre = self.tablamenus.item(menu, "values")[0]      
            for menu in self.pedido.listamenuspedidos:
                if menu.nombre == Nombre:
                    for ingnombre, ingcantidad in menu.ingredientesnecesarios.items():
                        ingstock = next((ing for ing in self.stock_ing if ing.nombre == ingnombre), None)
                        if ingstock:
                            ingstock.cantidad += ingcantidad
                        else:
                            nuevo_ing = Ingredientes(ingnombre, ingcantidad)
                            self.stock_ing.append(nuevo_ing)

                    self.pedido.eliminarmenu(menu)
                    break        
                
            self.actutablaing()
            self.actutablamenus()
            CTkM(title="Exito", message="Menu eliminado.", icon="warning")        
            return True                          

    def crear_tarjeta(self, menu):
        # Obtener el número de columnas y filas actuales
        num_tarjetas = len(self.listatarjetas) 
        fila = num_tarjetas // 2
        columna = num_tarjetas % 2

        # Crear la tarjeta con un tamaño fijo
        tarjeta = CTk.CTkFrame(self.img_frame, corner_radius=10, border_width=1, border_color="#4CAF50", width=64, height=140, fg_color="transparent")
        tarjeta.grid(row=fila, column=columna, padx=15, pady=15, )

        # Hacer que la tarjeta sea completamente clickeable 
        tarjeta.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))

        # Cambiar el color del borde cuando el mouse pasa sobre la tarjeta
        tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))  # Cambia a rojo al pasar el mouse
        tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))  # Vuelve al verde al salir

        # Verifica si hay una imagen asociada con el menú
        if menu.iconomenu:
            # Crear y empaquetar el CTkLabel con la imagen, sin texto y con fondo transparente
            imagen_label = CTk.CTkLabel(tarjeta, image=menu.iconomenu, width=64, height=64, text="", bg_color="transparent")
            imagen_label.pack(anchor="center", pady=5, padx=10)
            imagen_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))  # Asegura que el clic en la imagen funcione

            # Agregar un Label debajo de la imagen para mostrar el nombre del menú
            texto_label = CTk.CTkLabel(tarjeta, text=f"{menu.nombre}", text_color="black", font=("Helvetica", 12, "bold"), bg_color="transparent")
            texto_label.pack(anchor="center", pady=1)
            texto_label.bind("<Button-1>", lambda event: self.tarjeta_click(event, menu))  # Asegura que el clic en el texto funcione

        else:
            print(f"No se pudo cargar la imagen para el menú '{menu.nombre}'")   

        self.listatarjetas.append(tarjeta) 

    def tarjeta_click(self, event, menu):
        # Verificar si hay suficientes ingredientes en el stock para preparar el menú
        suficiente_stock = True
        if self.stock_ing==[]:
            suficiente_stock=False
        for ingnecesario, ingcantidad in menu.ingredientesnecesarios.items():
            for ingrediente_stock in self.stock_ing:
                if ingnecesario == ingrediente_stock.nombre:
                    if int(ingrediente_stock.cantidad) < int(ingcantidad):
                        suficiente_stock = False
                        break
            if not suficiente_stock:
                break
        
        if suficiente_stock:
            # Descontar los ingredientes del stock
            for ingnecesario, ingcantidad in menu.ingredientesnecesarios.items():
                for ingrediente_stock in self.stock_ing:
                    if ingnecesario == ingrediente_stock.nombre:
                        ingrediente_stock.cantidad = int(ingrediente_stock.cantidad) - int(ingcantidad)

            # Agregar el menú al pedido
            self.pedido.agregarmenu(menu)
            self.actutablaing()
            # Actualizar el Treeview
            self.actutablamenus()
            self.lbl_total.configure(text=f"El Total del pedido es: ${self.pedido.total:.2f}")
        else:
            CTkM(title="Stock Insuficiente", message=f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.", icon="warning")        

    def actutablaing(self):
        for child in self.tablalista.get_children():
            self.tablalista.delete(child)

        for ing in self.stock_ing:
            self.tablalista.insert("", "end", values=(ing.nombre, ing.cantidad))

    def actutablamenus(self):
        menuses = {}
        
        for menu in self.pedido.listamenuspedidos:
            if menu.nombre in menuses:
                menuses[menu.nombre]['cantidad'] += 1
                menuses[menu.nombre]['precio_total'] += menu.precio
            else:
                menuses[menu.nombre] = {'cantidad': 1, 'precio_total': menu.precio}

        for item in self.tablamenus.get_children():
            self.tablamenus.delete(item)

        for nombre, datos in menuses.items():
            self.tablamenus.insert("", "end", values=(nombre, datos['cantidad'], f"${datos['precio_total']:.2f}"))

    def generarboleta(self):
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
            if menu.nombre in menuses:
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
        pdf.cell(0, 10, "Gracias por la compra", ln=True, align= "C")
        pdf.cell(0, 10, "No se aceptan devoluciones", ln=True, align= "C")
        pdf.cell(0, 10, "Contacto: restaurante@gmail.com", ln=True, align= "C")
        pdf.ln()

        # Guardar el archivo PDF
        rutapdf = "Proyecto 1/boleta.pdf" 
        pdf.output(rutapdf)

        CTkM(title="Boleta Generada", message=f"Boleta generada con éxito en la siguiente ruta: '{rutapdf}'.", icon="info")            

CTk.set_appearance_mode("Dark")
app = Aplicacion()
app.mainloop()