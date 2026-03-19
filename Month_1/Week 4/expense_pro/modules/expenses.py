import json

def add_expense(expenses,date,amount,category):
    expense = {
        "date": date,
        "amount": amount,
        "category": category
    }
    expenses.append(expense)
    with open('expenses.json', 'w') as file:
        json.dump(expenses, file)

def view_expenses(expenses):
    if not expenses:
        return "No expenses recorded."
    result = []
    for expense in expenses:
        result.append(f"Date: {expense['date']}, Amount: {expense['amount']}, Category: {expense['category']}")
    return result

def total_spent(expenses):
    total = sum(expense['amount'] for expense in expenses)
    return total

def delete_expense(expenses, index):
    if 0 <= index < len(expenses):
        del expenses[index]
        with open('expenses.json', 'w') as file:
            json.dump(expenses, file)
        return "Expense deleted."
    else:
        return "Invalid index."