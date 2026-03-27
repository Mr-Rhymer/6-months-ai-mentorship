import json
from product import Product

class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, name):
        for p in self.products:
            if p.name.lower() == name.lower():
                self.products.remove(p)
                return True
        return False

    def update_quantity(self, name, new_quantity):
        for p in self.products:
            if p.name.lower() == name.lower():
                p.quantity = new_quantity
                return True
        return False

    def display_all(self):
        if not self.products:
            print("No products in inventory.")
        for p in self.products:
            print(p)

    def total_value(self):
        return sum(p.total_value() for p in self.products)

    def save_to_file(self, filename):
        data = []
        for p in self.products:
            data.append({
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            return
        self.products = []
        for item in data:
            p = Product(item["name"], item["price"], item["quantity"])
            self.products.append(p)