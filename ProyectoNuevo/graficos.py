import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import Pedido, Menu, Ingrediente, MenuIngrediente

def graficar_ventas_por_fecha(db: Session, intervalo: str = "diario"):
    pedidos = db.query(Pedido).all()
    
    # Agrupar ventas por intervalo
    ventas = {}
    for pedido in pedidos:
        fecha = pedido.fecha.date()
        if intervalo == "semanal":
            fecha = fecha - timedelta(days=fecha.weekday())  # Inicio de la semana
        elif intervalo == "mensual":
            fecha = fecha.replace(day=1)  # Primer día del mes
        elif intervalo == "anual":
            fecha = fecha.replace(month=1, day=1)  # Primer día del año
        
        ventas[fecha] = ventas.get(fecha, 0) + pedido.total

    # Ordenar fechas
    fechas = sorted(ventas.keys())
    totales = [ventas[fecha] for fecha in fechas]

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.plot(fechas, totales, marker="o")
    plt.title(f"Ventas por {intervalo.capitalize()}")
    plt.xlabel("Fecha")
    plt.ylabel("Total de Ventas")
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def graficar_menus_mas_comprados(db: Session):
    # Obtener pedidos y menús
    pedidos = db.query(Pedido).all()
    menu_ventas = {}

    for pedido in pedidos:
        for menu in pedido.menus:  # Asumiendo relación Pedido -> Menus
            menu_ventas[menu.nombre] = menu_ventas.get(menu.nombre, 0) + 1

    # Ordenar por cantidad
    menus = sorted(menu_ventas.keys(), key=lambda x: menu_ventas[x], reverse=True)
    cantidades = [menu_ventas[menu] for menu in menus]

    # Graficar
    plt.figure(figsize=(8, 8))
    plt.pie(cantidades, labels=menus, autopct="%1.1f%%", startangle=140)
    plt.title("Distribución de los Menús más Comprados")
    plt.axis("equal")  # Para asegurar que sea un círculo
    plt.show()

def graficar_uso_ingredientes(db: Session):
    # Obtener ingredientes de los menús en los pedidos
    pedidos = db.query(Pedido).all()
    uso_ingredientes = {}

    for pedido in pedidos:
        for menu in pedido.menus:  # Asumiendo relación Pedido -> Menus
            for menu_ingrediente in menu.ingredientes:  # Asumiendo relación Menu -> Ingredientes
                ingrediente = menu_ingrediente.ingrediente
                cantidad = menu_ingrediente.cantidad
                uso_ingredientes[ingrediente.nombre] = uso_ingredientes.get(ingrediente.nombre, 0) + cantidad

    # Ordenar ingredientes por cantidad
    ingredientes = sorted(uso_ingredientes.keys(), key=lambda x: uso_ingredientes[x], reverse=True)
    cantidades = [uso_ingredientes[ingrediente] for ingrediente in ingredientes]

    # Graficar
    plt.figure(figsize=(12, 6))
    plt.bar(ingredientes, cantidades, color="skyblue")
    plt.title("Uso de Ingredientes Basado en Todos los Pedidos")
    plt.xlabel("Ingrediente")
    plt.ylabel("Cantidad Utilizada")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
