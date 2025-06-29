import csv
import os
from datetime import datetime

# List to store expenses
expenses = []
# File name for saving/loading expenses
expense_file = 'expenses.csv'

# Global variable for monthly budgets for months
monthly_budgets = {}  # key: "YYYY-MM", value: float
# File name for saving/loading monthly budget
budget_file = 'budget.txt'

from enum import Enum

#Expense category enum
class ExpenseCategory(Enum):
    FOOD_GROCERIES = (1, "Food & Groceries")
    HOUSING_UTILITIES = (2, "Housing & Utilities")
    TRANSPORT = (3, "Transport")
    HEALTH_MEDICAL = (4, "Health & Medical")
    EDUCATION = (5, "Education")
    FAMILY_KIDS = (6, "Family & Kids")
    PERSONAL_CARE = (7, "Personal Care")
    ENTERTAINMENT_DINING = (8, "Entertainment & Dining")
    SAVINGS_INVESTMENTS = (9, "Savings & Investments")
    MISC = (10, "Miscellaneous")

    def __init__(self, code, label):
        self.code = code
        self.label = label

    @classmethod
    def from_code(cls, code):
        for item in cls:
            if item.code == code:
                return item
        return cls.MISC  # fallback

#sort expenses by date
def sort_expenses(descending=False):
    expenses.sort(key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"), reverse=descending)

# Load expenses from CSV file
def load_expenses():
    if os.path.exists(expense_file):
        with open(expense_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    expenses.append({
                        'date': row['date'],
                        'category': row['category'],  # Keep as string
                        'amount': float(row['amount']),
                        'description': row['description']
                    })
                except ValueError:
                    print("Warning: Skipping invalid expense entry:", row)


# Save expenses to CSV file
def save_expenses():
    sort_expenses(descending=False)
    with open(expense_file, mode='w', newline='') as file:
        fieldnames = ['date', 'category', 'amount', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow({
                'date': expense['date'],
                'category': expense['category'],
                'amount': expense['amount'],
                'description': expense['description']
            })
    print("Saving these expenses:", expenses)
    print("Expenses saved successfully!")

#choose expense category from a numbered list
def choose_category():
    print("\nSelect an Expense Category:")
    for category in ExpenseCategory:
        print(f"{category.code}. {category.label}")

    try:
        code = int(input("Enter category number: "))
        return ExpenseCategory.from_code(code)
    except ValueError:
        print("Invalid input. Defaulting to Miscellaneous.")
        return ExpenseCategory.MISC

# Add an expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    category_enum = choose_category()
    try:
        amount = float(input("Enter amount spent (₹): "))
    except ValueError:
        print("Invalid amount.")
        return

    description = input("Enter a brief description: ").strip()

    expense = {
        'date': date,
        'category': category_enum.label,  #Store only the label string
        'amount': amount,
        'description': description
    }

    expenses.append(expense)
    print("Expense added successfully!")

# View all expenses
def view_expenses():
    if not expenses:
        print("No expenses recorded.")
        return

    sort_expenses(descending=True)
    print("\nAll Expenses (latest first):")
    print("-" * 50)
    for exp in expenses:
        if all(k in exp for k in ('date', 'category', 'amount', 'description')):
            print(f"{exp['date']} | {exp['category']} | ₹{exp['amount']:.2f} | {exp['description']}")
        else:
            print("Incomplete entry found and skipped.")
    print("-" * 50)

# Save monthly budget to budget text file
def save_budget():
    with open(budget_file, mode='w') as file:
        for month, amount in monthly_budgets.items():
            file.write(f"{month},{amount}\n")

# Load monthly budget from budget text file
def load_budget():
    if os.path.exists(budget_file):
        with open(budget_file, mode='r') as file:
            for line in file:
                try:
                    month, amount = line.strip().split(",")
                    monthly_budgets[month] = float(amount)
                except ValueError:
                    continue

# Set and track the budget
def track_budget():
    selected_month = input("Enter month to track (YYYY-MM): ").strip()
    try:
        datetime.strptime(selected_month + "-01", "%Y-%m-%d")
    except ValueError:
        print("Invalid month format. Please use YYYY-MM (e.g., 2025-06).")
        return

    # Show current budget if exists
    current_budget = monthly_budgets.get(selected_month, 0)
    print(f"Current budget for {selected_month}: ₹{current_budget:.2f}")

    # Ask if user wants to update
    update = input("Do you want to edit the monthly budget? (y/n): ").strip().lower()
    if update == 'y':
        try:
            new_budget = float(input("Enter new monthly budget: "))
            monthly_budgets[selected_month] = new_budget
            save_budget()
            print(f"✅ Budget for {selected_month} updated to ₹{new_budget:.2f}")
        except ValueError:
            print("Invalid budget input.")
            return

    # Re-fetch in case it was just updated
    budget = monthly_budgets.get(selected_month, 0)

    # Calculate total spent in that month
    total_spent = sum(
        exp['amount'] for exp in expenses
        if exp['date'].startswith(selected_month)
    )
    remaining = budget - total_spent

    print(f"\nMonth: {selected_month}")
    print(f"Total spent: ₹{total_spent:.2f}")
    print(f"Monthly Budget: ₹{budget:.2f}")
    if remaining < 0:
        print(f"⚠️ You have exceeded your budget by ₹{abs(remaining):.2f}!")
    else:
        print(f"✅ You have ₹{remaining:.2f} left for the month.")

# Show menu and handle options
def show_menu():
    while True:
        print("\n--- Personal Expense Tracker ---")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Track budget")
        print("4. Save expenses")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            track_budget()
        elif choice == '4':
            save_expenses()
        elif choice == '5':
            save_expenses()
            save_budget()
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


# Program entry point
if __name__ == '__main__':
    load_expenses()
    load_budget()
    show_menu()