from inventory import Inventory

def run_pipeline():
    inv = Inventory()
    inv.load_from_file("inventory.json")   

    input_file = input("CSV file to import: ")
    
    
    try:
        inv.import_from_csv(input_file)
    except FileNotFoundError:
        print("Error: File not found.")
    
    try:
        inv.generate_report("pipeline_report.txt")
    except Exception as e:
        print(f"Error generating report: {e}")
    
    try:
        inv.export_to_csv("pipeline_export.csv")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
    
    try:
        inv.save_to_file("inventory.json")
    except Exception as e:
        print(f"Error saving inventory: {e}")
    
    def print_summary():
        print(f"Total products: {len(inv.products)}")
        print(f"Total categories: {len(inv.categories)}")
    print_summary()

if __name__ == "__main__":
    run_pipeline()