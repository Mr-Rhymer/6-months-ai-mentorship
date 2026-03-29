from product import Product
from inventory import Inventory
from category import Category

def main():
    inv = Inventory()
    inv.load_from_file("inventory.json")

    while True:
        print("\nInventory Manager")
        print("1. Add product")
        print("2. Remove product")
        print("3. Update quantity")
        print("4. Display all products")
        print("5. Show total value")
        print("6. Add category")
        print("7. List categories")
        print("8. Save and exit")
        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Name: ")
            try:
                price = float(input("Price: "))
                quantity = int(input("Quantity: "))
            except ValueError:
                print("Invalid number.")
                continue
            p = Product(name, price, quantity)
            inv.add_product(p)
            print("Product added.")
        elif choice == '2':
            name = input("Name of product to remove: ")
            if inv.remove_product(name):
                print("Product removed.")
            else:
                print("Product not found.")
        elif choice == '3':
            name = input("Name of product to update: ")
            try:
                new_qty = int(input("New quantity: "))
            except ValueError:
                print("Invalid quantity.")
                continue
            if inv.update_quantity(name, new_qty):
                print("Quantity updated.")
            else:
                print("Product not found.")
        elif choice == '4':
            inv.display_all()
        elif choice == '5':
            print(f"Total inventory value: ${inv.total_value():.2f}")
        elif choice == '6':
            cat_name = input("Category name: ")
            cat_desc = input("Category description (optional): ")
            category = Category(cat_name, cat_desc)
            inv.add_category(category)
            print("Category added.")
        elif choice == '7':
            print("Categories:")
            for category in inv.categories.values():
                print(f" - {category}")
        elif choice == '8':
            inv.save_to_file("inventory.json")
            print("Data saved. Exiting.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main() 