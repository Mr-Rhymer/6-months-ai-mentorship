import json
from product import Product
from category import Category
class Inventory:
    def __init__(self):
        self.products = []
        self.categories = {}

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
    
    def add_category(self, category):
        self.categories[category.name] = category
    
    def get_category(self, name):
        return self.categories.get(name, None)

    def save_to_file(self, filename):
        data = {
    "categories": [{"name": c.name, "description": c.description} for c in self.categories.values()],
    "products": []
}

        for p in self.products:
            data["products"].append({
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity,
                "category": p.category.name if p.category else None
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return
        self.categories = {c["name"]: Category(c["name"], c.get("description", "")) for c in data.get("categories", [])}
        self.products = []
        for item in data.get("products", []):
            category = self.categories.get(item.get("category")) if item.get("category") else None
            p = Product(item["name"], item["price"], item["quantity"], category)
            self.products.append(p)