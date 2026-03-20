from modules import expenses,file_utils


def main():
    expenses_list = file_utils.load_data('expenses.json')
    
    while True:
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Spent")
        print("4. Delete Expense")
        print("5. Save and Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            expenses.add_expense(expenses_list, date, amount, category)
            file_utils.save_data('expenses.json', expenses_list)
            print("Expense added.")
        
        elif choice == '2':
            result = expenses.view_expenses(expenses_list)
            if isinstance(result, str):
                print(result)
            else:
                for item in result:
                    print(item)
        
        elif choice == '3':
            total = expenses.total_spent(expenses_list) 
            print(f"Total spent: {total}")
        
        elif choice == '4':
            try:
             index = int(input("Enter expense index to delete: ")) -1
            
             message = expenses.delete_expense(expenses_list, index)
             file_utils.save_data('expenses.json', expenses_list) 
             print(message)
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == '5':
            file_utils.save_data('expenses.json', expenses_list)
            print("Data saved. Exiting.")
            break
        
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":    main()
