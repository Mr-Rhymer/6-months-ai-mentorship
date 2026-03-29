class Product:
    def __init__(self, name, price, quantity , category=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def total_value(self):
        return self.price * self.quantity

    def __str__(self):
        if self.category:
            return f"{self.name} ({self.category}): ${self.price} x {self.quantity} = ${self.total_value()}"
        else:  
          return f"{self.name}: ${self.price} x {self.quantity} = ${self.total_value()}"