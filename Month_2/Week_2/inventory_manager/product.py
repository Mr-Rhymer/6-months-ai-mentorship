class Product:
    def __init__(self, name, price, quantity , category):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def total_value(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name} (Category:{self.category if self.category else 'None'}): ${self.price} x {self.quantity} = ${self.total_value()}"