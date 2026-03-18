shopping_list = []
action = input("Would you like to (a)dd, (r)emove, (v)iew, (s)ort, (t)otal, (m)erge duplicates or (e)xit? ").lower()
while True:
    if action == 'a':
        item = {}
        item['name'] = input("Enter the item name: ").title()
        item['quantity'] = int(input("Enter the quantity: "))
        shopping_list.append(item)
    elif action == 'r':
        try:
            item_name = input("Enter the name of the item to remove: ").title()
            shopping_list = [item for item in shopping_list if item['name'].lower() != item_name.lower()]
        except Exception as e:
            print(f"An error occurred: {e}") 
    elif action == 'v':
        if shopping_list:
            print("\nShopping List:")
            for item in shopping_list:
                print(f"  - {item['name']} (Quantity: {item['quantity']})")
        else:
            print("\nYour shopping list is empty.")  
    elif action == 's':
        shopping_list.sort(key=lambda x: x['name'])
        print("\nSorted Shopping List:")
        for item in shopping_list:
            print(f"  - {item['name']} (Quantity: {item['quantity']})")
    elif action == 't':
        total_items = sum(item['quantity'] for item in shopping_list)
        print(f"\nTotal number of items: {total_items}")
    elif action == 'm':
        from collections import defaultdict
        merged = defaultdict(lambda: {'name': '', 'quantity': 0})
        for item in shopping_list:
            key = item['name'].lower()
            merged[key]['quantity'] += item['quantity']
            if not merged[key]['name']:
                merged[key]['name'] = item['name']
        shopping_list = list(merged.values())
        print("\nDuplicates merged. Shopping list updated.")
    elif action == 'e':
        print("Exiting the shopping list manager. Goodbye!")
        break
    else:    
        print("Invalid action. Please choose (a)dd, (r)emove, (v)iew, (s)ort, (t)otal, (m)erge duplicates or (e)xit.")
    action = input("\nWould you like to (a)dd, (r)emove, (v)iew, (s)ort, (t)otal, (m)erge duplicates or (e)xit? ").lower()