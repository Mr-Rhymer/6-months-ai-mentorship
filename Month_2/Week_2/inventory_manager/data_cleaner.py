import csv
from category import Category
from product import Product

def data_cleaner(filename):
    cleaned_products = []  # list, not dict
    corrections = {"price": 0, "quantity": 0, "category": 0}
    categories_found = set()

    try:
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clean name
                name = row.get("name", "").strip()
                if not name:
                    continue  # skip rows without a name

                # Clean price
                try:
                    price = float(row.get("price", ""))
                    if price < 0:
                        price = 0.0
                        corrections["price"] += 1
                except (ValueError, TypeError):
                    price = 0.0
                    corrections["price"] += 1

                # Clean quantity
                try:
                    quantity = int(row.get("quantity", ""))
                    if quantity < 0:
                        quantity = 0
                        corrections["quantity"] += 1
                except (ValueError, TypeError):
                    quantity = 0
                    corrections["quantity"] += 1

                # Clean category
                category_name = row.get("category", "").strip()
                if not category_name:
                    category_name = "Uncategorized"
                    corrections["category"] += 1
                categories_found.add(category_name)
                category = Category(category_name, "")

                product = Product(name, price, quantity, category)
                cleaned_products.append(product)

    except FileNotFoundError:
        print(f"File {filename} not found.")
        return

    # Write cleaned CSV
    with open("cleaned_data.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "price", "quantity", "category"])
        writer.writeheader()
        for p in cleaned_products:
            writer.writerow({
                "name": p.name,
                "price": p.price,
                "quantity": p.quantity,
                "category": p.category.name if p.category else ""
            })

    # Write report
    with open("cleaning_report.txt", "w") as f:
        f.write("DATA CLEANING REPORT\n")
        f.write("====================\n")
        f.write(f"Total rows processed: {len(cleaned_products)}\n")
        f.write(f"Price corrections: {corrections['price']}\n")
        f.write(f"Quantity corrections: {corrections['quantity']}\n")
        f.write(f"Category filled: {corrections['category']}\n")
        f.write(f"Unique categories: {', '.join(sorted(categories_found))}\n")

    print("Cleaning completed. Files: cleaned_data.csv, cleaning_report.txt")

if __name__ == "__main__":
    filename = input("Enter the CSV file to clean: ")
    data_cleaner(filename)