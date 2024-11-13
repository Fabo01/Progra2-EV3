class Pedidos:
    def __init__(self):
        self.listamenuspedidos = []
        self.total = 0.0

    def agregarmenu(self, menu):
        self.listamenuspedidos.append(menu)
        self.total += menu.precio

    def eliminarmenu(self, menu):
        if menu in self.listamenuspedidos:
            self.listamenuspedidos.remove(menu)
            self.total -= menu.precio

    def calctotal(self):
        return self.total            