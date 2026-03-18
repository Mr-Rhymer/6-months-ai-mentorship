import json

expenses = []

def add_expense(amount, category):
    '''Add a new expense with the given amount and category.'''
    try:
        amount = float(amount)
        expenses.append({"amount": amount, "category": category})
        print(f"Added expense: ${amount:.2f} in category '{category}'")
    except ValueError:
        print("Invalid amount. Please enter a valid number.")

def view_all():
    '''Display all recorded expenses.'''
    if not expenses:
        print("No expenses recorded.")
    else:
        print("Expenses:")
        for idx, expense in enumerate(expenses, start=1):
            print(f"{idx}. ${expense['amount']:.2f} - {expense['category']}")

def total_spent():
    '''Calculate and display the total amount spent.'''
    if not expenses:
        print("No expenses recorded.")
    else:
        total = sum(expense['amount'] for expense in expenses)
        print(f"Total spent: ${total:.2f}")

def monthly_summary():
    '''Provide a summary of total and average expenses for the month.'''
    if not expenses:
        print("No expenses recorded.")
    else:
        total = sum(expense['amount'] for expense in expenses)
        average = total / len(expenses)
        print(f"Monthly Summary:")
        print(f"Total Spent: ${total:.2f}")
        print(f"Average Expense: ${average:.2f}")


def del_expense(index):
    '''Delete an expense by its index.'''
    try:
        index = int(index) - 1
        if 0 <= index < len(expenses):
            removed = expenses.pop(index)
            print(f"Removed expense: ${removed['amount']:.2f} from category '{removed['category']}'")
        else:
            print("Invalid index. Please enter a valid number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def save_expenses(filename):
    '''Save expenses to a JSON file.'''
    try:        
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(expenses, file, indent=4)
        print(f"Expenses saved to {filename}.")
    except IOError:
        print("Error saving expenses. Please try again.")


def view_by_category():
    '''View total expenses by category.'''
    if not expenses:
        print("No expenses recorded.")
        return
    
    from collections import defaultdict
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    
    for expense in expenses:
        category_totals[expense['category']] += expense['amount']
        category_counts[expense['category']] += 1
    
    print("Expenses by Category:")
    for category, total in category_totals.items():
        count = category_counts[category]
        average = total / count
        print(f"{category}: ${total:.2f} total ({count} expenses, avg: ${average:.2f})")

def load_expenses(filename):
    '''Load expenses from a JSON file.'''
    try:
        global expenses
        with open(filename, 'r', encoding='utf-8') as file:
            expenses = json.load(file)
        print(f"Expenses loaded from {filename}.")
    except IOError:
        print("Error loading expenses. Please try again.")
    except ValueError:
        print("Error parsing expenses file. File may be corrupted.")   


def main():
    '''Main function to run the expense tracker application.'''
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Total Spent")
        print("4. Monthly Summary")
        print("5. Delete Expense")
        print("6. Save Expenses")
        print("7. View by Category")
        print("8. Load Expenses")
        print("9. Exit")
        try:
            choice = input("Enter your choice: ")
            
            if choice == '1':
                amount = input("Enter expense amount: ")
                category = input("Enter expense category: ")
                add_expense(amount, category)
            elif choice == '2':
                view_all()
            elif choice == '3':
                total_spent()
            elif choice == '4':
                monthly_summary()
            elif choice == '5':
                index = input("Enter the index of the expense to delete: ")
                del_expense(index)
            elif choice == '6':
                filename = input("Enter filename to save expenses: ")
                save_expenses(filename)
            elif choice == '7':
                view_by_category()
            elif choice == '8':
                filename = input("Enter filename to load expenses: ")
                load_expenses(filename)
            elif choice == '9':
                print("Exiting Expense Tracker. Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()