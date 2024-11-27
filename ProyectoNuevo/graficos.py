import matplotlib.pyplot as plt

def graficar_ventas_por_fecha():
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

def graficar_menus_mas_comprados():
    menus = ["Completos", "Hamburguesa", "Papas Fritas", "Pepsi"]
    cantidades = [30, 20, 50, 40]

    plt.figure(figsize=(8, 8))
    plt.pie(cantidades, labels=menus, autopct="%1.1f%%", startangle=140)
    plt.title("Distribución de Menús Más Comprados")
    plt.axis("equal")
    plt.show()

def graficar_uso_ingredientes():
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
