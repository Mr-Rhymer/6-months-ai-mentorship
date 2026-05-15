import sqlite3
import csv
import datetime 

try:
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
except sqlite3.Error as e:
    print("Error connecting to database:", e)

def init_db():
    try: 
       cursor.execute(
        '''CREATE TABLE IF NOT EXISTS expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT
);'''
    )
    except Exception as e:
        print("Error initializing database:", e)


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

def valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def export_to_csv():
    try:
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()
        if not rows:
            print("No expenses to export.")
            return
        filename = f"expenses_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['expense_id', 'date', 'amount', 'category', 'description'])
            writer.writerows(rows)
        print(f"Exported {len(rows)} rows to {filename}")
    except (sqlite3.Error, IOError, OSError) as e:
        print(f"Export failed: {e}")

def main():
    try:
        init_db()
    
        while True:
            print("\nExpense Tracker Menu:")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Delete Expense")
            print("4. Total Spent")
            print("5. Expenses by Category")
            print("6. Export to CSV")
            print("7. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                while True:
                    date = input("Enter date (YYYY-MM-DD): ")
                    if valid_date(date):
                        break
                    else:
                        print("Invalid date format. Please enter in YYYY-MM-DD format.")
                while True:
                    try:

                       amount = float(input("Enter amount: "))
                       if amount > 0:
                            break
                       else:                            
                           print("Amount must be positive. Please try again.")
                    except ValueError:
                        print("Invalid amount. Please enter a number.")
                while True:
                  category = input("Enter category: ")
                  if category:
                    break
                  else:
                    print("Category cannot be empty. Please try again.")
                description = input("Enter description (optional): ")
                add_expense(date, amount, category, description)
            elif choice == "2":
                view_expenses()
            elif choice == "3": 
               try:
                expense_id = int(input("Enter expense ID to delete: "))
                answer = input(f"Are you sure you want to delete expense with ID {expense_id}? (y/n): ")
                if answer.lower() == 'y':
                    delete_expense(expense_id)
                
               except ValueError:
                  print("Invalid expense ID. Please enter a number.")
            elif choice == "4":
               total_spent()
            elif choice == "5":
                category = input("Enter category: ")
                expenses_by_category(category)
            elif choice == "6":
               export_to_csv()
            elif choice == "7":
               break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()
    conn.close()
    print("Database connection closed.")