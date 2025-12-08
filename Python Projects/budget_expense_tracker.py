import csv
import os
from datetime import datetime

class BudgetTracker:
    def __init__(self, filename="budget_expenses.csv"):
        self.filename = filename
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.isfile(self.filename):
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Type", "Category", "Amount", "Description"])

    def add_transaction(self, transaction_type, category, amount, description):
        """Add income or expense"""
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d'),
                transaction_type,
                category,
                amount,
                description
            ])
        print(f"✓ {transaction_type} of ${amount} added to {category}")
   
    def get_summary(self):
        """Display overall summary"""
        income = 0
        expenses = 0

        if not os.path.exists(self.filename):   
            print("No transactions yet.")
            return
       
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Type'] == 'Income':
                    income += float(row['Amount'])
                else:
                    expenses += float(row['Amount'])

        print("\n--- Budget Summary ---")
        print(f"Total Income: ${income:.2f}")
        print(f"Total Expenses: ${expenses:.2f}")
        print(f"Net: ${income - expenses:.2f}")
    
    def get_category_breakdown(self):
        """Display expenses by category"""
        categories = {}
       
        with open(self.filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Type'] == 'Expense':
                    cat = row['Category']
                    amount = float(row['Amount'])
                    categories[cat] = categories.get(cat, 0) + amount
       
        if not categories:
            print("No expenses recorded.")
            return
       
        print("\n=== Expenses By Category ===")
        for cat, amount in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"{cat}: ${amount:.2f}")

def main():
    tracker = BudgetTracker()
   
    while True:
        print("\n1. Add Expense\n2. Add Income\n3. View Summary\n4. View by Category\n5. Exit")
        choice = input("Choose: ").strip()
       
        if choice == '1':
            cat = input("Category: ").strip()
            amt = float(input("Amount: "))
            desc = input("Description: ").strip()
            tracker.add_transaction("Expense", cat, amt, desc)
        elif choice == '2':
            cat = input("Source: ").strip()
            amt = float(input("Amount: "))
            desc = input("Description: ").strip()
            tracker.add_transaction("Income", cat, amt, desc)
        elif choice == '3':
            tracker.get_summary()
        elif choice == '4':
            tracker.get_category_breakdown()
        elif choice == '5':
            break

if __name__ == "__main__":
    main()


    
    