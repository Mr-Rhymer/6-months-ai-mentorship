import json

def add_expense(expenses,date,amount,category):
    expense = {
        "date": date,
        "amount": amount,
        "category": category
    }
    expenses.append(expense)
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
        return "Expense deleted."
    else:
        return "Invalid index."