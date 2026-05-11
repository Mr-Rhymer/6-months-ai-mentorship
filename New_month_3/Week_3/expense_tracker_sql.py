import sqlite3

conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

def init_db():
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT
);'''
    )

def add_expense(date, amount, category, description):
    try:
        cursor.execute(
            "INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
            (date, amount, category, description)
        )
        conn.commit()
        print("Expense added. ID:", cursor.lastrowid)
    except sqlite3.Error as e:
        print("Error adding expense:", e)
       

def view_expenses():
    try:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        for expense in expenses:
            print(f'''ID: {expense[0]} | Date: {expense[1]} 
| Amount: {expense[2]} | Category: {expense[3]} 
| Description: {expense[4]}''')
    except sqlite3.Error as e:
        print("Error viewing expenses:", e)

def delete_expense(expense_id):
    try:
        cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
        conn.commit()
        print("Expense deleted. ID:", expense_id)
      
    except sqlite3.Error as e:
        print("Error deleting expense:", e)
   

def total_spent():
    try:
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total = cursor.fetchone()[0]
        if total is None:
           total = 0
        print(f"Total spent: {total}")
        
    except sqlite3.Error as e:
        print("Error calculating total spent:", e)

def expenses_by_category(category):
    try:
        cursor.execute("SELECT * FROM expenses WHERE category = ? ", (category,))
        category_expenses = cursor.fetchall()
        for expense in category_expenses:
            print(f'''ID: {expense[0]} | Date: {expense[1]}| Amount: {expense[2]} | Category: {expense[3]} | Description: {expense[4]}''')
    except sqlite3.Error as e:
        print("Error calculating expenses by category:", e)

def main():
    init_db()
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Total Spent")
        print("5. Expenses by Category")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            description = input("Enter description (optional): ")
            add_expense(date, amount, category, description)
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            expense_id = int(input("Enter expense ID to delete: "))
            delete_expense(expense_id)
        elif choice == "4":
            total_spent()
        elif choice == "5":
            category = input("Enter category: ")
            expenses_by_category(category)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    conn.close()
    