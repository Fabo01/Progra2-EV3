from Ingredientes import Ingredientes
from PIL import Image
import customtkinter as CTk

class Menus:
    def __init__(self, nombre, precio, ingredientesnecesarios, rutaicon):
        self.nombre = nombre
        self.precio = precio
        self.ingredientesnecesarios = ingredientesnecesarios
        self.cantidaddis = 0
        self.iconomenu = CTk.CTkImage(Image.open(rutaicon))
    
    def verificardisp(self, stockdisp):
        cantidades_posibles = []
        for ingrediente, ingnecesarios in self.ingredientesnecesarios.items():
            if ingrediente in stockdisp:
                cantidad_disponible = stockdisp[ingrediente]
                max_por_ingrediente = cantidad_disponible // ingnecesarios
                cantidades_posibles.append(max_por_ingrediente)
            else:
                return 0  # Si falta un ingrediente, no se puede preparar ningún menú
        self.cantidaddis = min(cantidades_posibles)
        return self.cantidaddis  