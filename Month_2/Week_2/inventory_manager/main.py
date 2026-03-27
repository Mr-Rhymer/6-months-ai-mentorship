from product import Product

# Create three products
p1 = Product("Laptop", 1200, 2)
p2 = Product("Mouse", 25, 5)
p3 = Product("Keyboard", 80, 3)

# Print each product
print(p1)
print(p2)
print(p3)

# Optionally print total values separately
print(f"Total value of laptop: ${p1.total_value()}")