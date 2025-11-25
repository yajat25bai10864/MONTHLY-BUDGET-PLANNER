import json
import os
from datetime import datetime


class BudgetPlanner:

    FILE_NAME = 'budget_data.json'

    def __init__(self):
        """Initializes the planner and attempts to load existing data."""
        self.transactions = []
        self._load_data()

    def _load_data(self):
        """Loads transaction data from the JSON file if it exists."""
        if os.path.exists(self.FILE_NAME):
            try:
                with open(self.FILE_NAME, 'r') as f:
                    self.transactions = json.load(f)
                print(f"Data loaded successfully from {self.FILE_NAME}.")
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error loading data: {e}. Starting with an empty budget.")
                self.transactions = []
        else:
            print("No existing budget file found. Starting a new budget.")

    def _save_data(self):

        try:
            with open(self.FILE_NAME, 'w') as f:
                json.dump(self.transactions, f, indent=4)
            print(f"\n[INFO] Data saved to {self.FILE_NAME}.")
        except IOError as e:
            print(f"\n[ERROR] Failed to save data: {e}")

    def add_transaction(self, type_in, description, amount):

        transaction = {
            'type': type_in,
            'description': description,
            'amount': amount,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.transactions.append(transaction)
        print(f"\n[SUCCESS] {type_in.capitalize()} of ${amount:,.2f} added.")
        self._save_data()

    def calculate_summary(self):
        """
        Calculates the total income, total expenses, and the current balance.

        Returns:
            tuple: (total_income, total_expenses, balance)
        """
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        total_expenses = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        balance = total_income - total_expenses
        return total_income, total_expenses, balance

    def display_summary(self):
        """Calculates and prints the current financial summary."""
        income, expenses, balance = self.calculate_summary()

        # Formatting for display
        income_str = f"${income:,.2f}"
        expenses_str = f"${expenses:,.2f}"
        balance_str = f"${balance:,.2f}"

        # Determine balance color/status
        balance_status = "Positive" if balance >= 0 else "Negative"

        # Generate the table-like summary
        print("\n" + "=" * 40)
        print(f"{'MONTHLY BUDGET SUMMARY':^40}")
        print("=" * 40)
        print(f"{'Total Income:':<20} {income_str:>19}")
        print(f"{'Total Expenses:':<20} -{expenses_str:>18}")
        print("-" * 40)
        print(f"{'Current Balance:':<20} {balance_str:>19}")
        print(f"{'Status:':<20} {balance_status:>19}")
        print("=" * 40)

    def display_transactions(self):
        """Prints a detailed list of all recorded transactions."""
        if not self.transactions:
            print("\n[INFO] No transactions recorded yet.")
            return

        print("\n" + "*" * 60)
        print(f"{'TRANSACTION HISTORY':^60}")
        print("*" * 60)

        # Define column widths for neat alignment
        print(f"{'DATE':<20} {'TYPE':<10} {'AMOUNT':<12} {'DESCRIPTION':<15}")
        print("-" * 60)

        # Print each transaction
        for t in sorted(self.transactions, key=lambda x: x['date'], reverse=True):
            type_display = t['type'].upper()
            amount_display = f"{t['amount']:,.2f}"
            print(f"{t['date'][:10]:<20} {type_display:<10} ${amount_display:<11} {t['description']:<15}")

        print("*" * 60)

    def run(self):
        """The main loop for the Budget Planner command-line interface."""
        while True:
            print("\n--- BUDGET PLANNER MENU ---")
            print("1. Add Income")
            print("2. Add Expense")
            print("3. View Summary")
            print("4. View All Transactions")
            print("5. Exit and Save")

            choice = input("Enter your choice (1-5): ").strip()

            if choice == '1' or choice == '2':
                # Determine transaction type
                trans_type = 'income' if choice == '1' else 'expense'

                print(f"\n--- Adding {trans_type.capitalize()} ---")
                description = input("Enter description: ").strip()

                while True:
                    try:
                        amount = float(input("Enter amount: ").strip())
                        if amount <= 0:
                            print("[ERROR] Amount must be positive.")
                            continue
                        self.add_transaction(trans_type, description, amount)
                        break
                    except ValueError:
                        print("[ERROR] Invalid amount. Please enter a number.")

            elif choice == '3':
                self.display_summary()

            elif choice == '4':
                self.display_transactions()

            elif choice == '5':
                self._save_data()
                print("\nThank you for using the Budget Planner. Goodbye!")
                break

            else:
                print("\n[ERROR] Invalid choice. Please enter a number between 1 and 5.")


# Main execution block
if __name__ == '__main__':
    planner = BudgetPlanner()
    planner.run()
