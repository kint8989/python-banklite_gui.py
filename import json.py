import json
import os
from datetime import datetime


class Account:
    def __init__(self, acc_id, name, balance=0.0, transactions=None):
        self.id = acc_id
        self.name = name
        self.balance = balance
        self.transactions = transactions if transactions else []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append(
            f"{datetime.now()} - Deposited ₹{amount}"
        )

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount
        self.transactions.append(
            f"{datetime.now()} - Withdrew ₹{amount}"
        )

    def get_balance(self):
        return self.balance

    def get_history(self):
        return self.transactions

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "balance": self.balance,
            "transactions": self.transactions
        }

    @staticmethod
    def from_dict(data):
        return Account(
            data["id"],
            data["name"],
            data["balance"],
            data["transactions"]
        )


class Bank:
    
    def __init__(self):
        self.accounts = []
        self.load_from_file()

        

    def create_account(self, name, initial_balance=0.0):
        acc_id = len(self.accounts) + 1
        account = Account(acc_id, name, initial_balance)
        account.transactions.append(
            f"{datetime.now()} - Account created with ₹{initial_balance}"
        )
        self.accounts.append(account)
        self.save_to_file()
        return account

    def find_account_by_id(self, acc_id):
        for account in self.accounts:
            if account.id == acc_id:
                return account
        return None

    def deposit_to_account(self, acc_id, amount):
        account = self.find_account_by_id(acc_id)
        if not account:
            raise ValueError("Account not found.")
        account.deposit(amount)
        self.save_to_file()

    def withdraw_from_account(self, acc_id, amount):
        account = self.find_account_by_id(acc_id)
        if not account:
            raise ValueError("Account not found.")
        account.withdraw(amount)
        self.save_to_file()

    def transfer(self, from_id, to_id, amount):
        sender = self.find_account_by_id(from_id)
        receiver = self.find_account_by_id(to_id)
        if not sender or not receiver:
            raise ValueError("Invalid account ID.")

        if amount <= 0:
         raise ValueError("Transfer amount must be positive.")

        if sender.balance < amount:
         raise ValueError("Insufficient balance.")

        sender.balance -= amount
        receiver.balance += amount

        sender.transactions.append(
        f"{datetime.now()} - Transferred ₹{amount} to Account {to_id}"
    )

        receiver.transactions.append(
        f"{datetime.now()} - Received ₹{amount} from Account {from_id}"
    )

        self.save_to_file()

    def show_account_details(self, acc_id):
        account = self.find_account_by_id(acc_id)
        if not account:
            raise ValueError("Account not found.")
        return account

    def save_to_file(self):
        with open("bank.json", "w") as file:
            json.dump([acc.to_dict() for acc in self.accounts], file, indent=4)

    def load_from_file(self):
        if os.path.exists("bank.json"):
            with open("bank.json", "r") as file:
                data = json.load(file)
                self.accounts = [Account.from_dict(acc) for acc in data]


# -------------------------
# Console Interface
# -------------------------

def main():
    bank = Bank()

    while True:
        print("\n==== BankLite System ====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View Balance")
        print("5. View Transaction History")
        print("6. Exit")
        print("7. Transfer Money")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                name = input("Enter account holder name: ")
                initial = float(input("Enter initial balance: "))
                acc = bank.create_account(name, initial)
                print(f"Account created successfully! ID: {acc.id}")

            elif choice == "2":
                acc_id = int(input("Enter account ID: "))
                amount = float(input("Enter deposit amount: "))
                bank.deposit_to_account(acc_id, amount)
                print("Deposit successful.")

            elif choice == "3":
                acc_id = int(input("Enter account ID: "))
                amount = float(input("Enter withdrawal amount: "))
                bank.withdraw_from_account(acc_id, amount)
                print("Withdrawal successful.")

            elif choice == "4":
                acc_id = int(input("Enter account ID: "))
                acc = bank.show_account_details(acc_id)
                print(f"Current Balance: ₹{acc.get_balance()}")

            elif choice == "5":
                acc_id = int(input("Enter account ID: "))
                acc = bank.show_account_details(acc_id)
                print("Transaction History:")
                for t in acc.get_history():
                    print(t)

            elif choice == "7":
                from_id = int(input("Enter sender account ID: "))
                to_id = int(input("Enter receiver account ID: "))
                amount = float(input("Enter transfer amount: "))
                bank.transfer(from_id, to_id, amount)
                print("Transfer successful.")        

            elif choice == "6":
                print("Exiting BankLite. Goodbye!")
                break

            else:
                print("Invalid choice.")

        except ValueError as e:
            print("Error:", e)


if __name__ == "__main__":
    main()