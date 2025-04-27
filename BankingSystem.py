import json
import os
import csv
import datetime
import requests

FILE_NAME = "users.json"

# Load accounts
def load_accounts():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}

# Save accounts
def save_accounts(accounts):
    with open(FILE_NAME, "w") as file:
        json.dump(accounts, file, indent=4)

# Register a new user
def register(accounts):
    username = input("Enter a new username: ")
    if username in accounts:
        print("⚠️ Username already exists.")
        return None
    password = input("Enter a password: ")
    accounts[username] = {"password": password, "balance": 0.0}
    save_accounts(accounts)
    print("✅ Registration successful. Please login.")
    return None

# Authenticate a user
def login(accounts):
    username = input("Username: ")
    password = input("Password: ")
    if username in accounts and accounts[username]["password"] == password:
        print(f"✅ Welcome, {username}!")
        return username
    else:
        print("❌ Incorrect username or password.")
        return None

# Deposit
def deposit(accounts, username):
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount > 0:
            accounts[username]["balance"] += amount
            print(f"✅ Deposited ${amount:.2f}")
        else:
            print("⚠️ Invalid amount.")
    except ValueError:
        print("⚠️ Please enter a valid number.")
    save_accounts(accounts)

# Withdraw
def withdraw(accounts, username):
    try:
        amount = float(input("Enter amount to withdraw: "))
        if 0 < amount <= accounts[username]["balance"]:
            accounts[username]["balance"] -= amount
            print(f"✅ Withdrawn ${amount:.2f}")
        else:
            print("⚠️ Insufficient funds or invalid amount.")
    except ValueError:
        print("⚠️ Please enter a valid number.")
    save_accounts(accounts)

# Check balance
def check_balance(accounts, username):
    print(f"💰 Your balance: ${accounts[username]['balance']:.2f}")

# Transfer money
def transfer(accounts, username):
    recipient = input("Enter recipient username: ")
    if recipient not in accounts:
        print("⚠️ Recipient not found.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
        if 0 < amount <= accounts[username]["balance"]:
            accounts[username]["balance"] -= amount
            accounts[recipient]["balance"] += amount
            print(f"✅ Transferred ${amount:.2f} to {recipient}")
            save_accounts(accounts)
        else:
            print("⚠️ Insufficient funds or invalid amount.")
    except ValueError:
        print("⚠️ Invalid amount entered.")

# Generate monthly bank statement (CSV)
def generate_statement(accounts, username):
    filename = f"{username}_statement.csv"
    now = datetime.datetime.now()
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Balance", "Date"])
        writer.writerow([username, f"${accounts[username]['balance']:.2f}", now.strftime("%Y-%m-%d %H:%M:%S")])
    print(f"✅ Statement saved as {filename}")

# Currency Converter
def currency_converter(accounts, username):
    try:
        # Ask user for the base currency
        base_currency = input("Enter base currency code (e.g., USD, EUR, GBP): ").upper()
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base_currency}')
        data = response.json()

        # Check if the base currency data is available
        if base_currency not in data['rates']:
            print("⚠️ Base currency not supported.")
            return
        
        print("Available currencies:", ", ".join(data['rates'].keys()))
        target_currency = input("Enter target currency code (e.g., EUR, GBP, INR): ").upper()

        if target_currency in data['rates']:
            # Ask user for the amount they want to convert
            amount_to_convert = float(input(f"Enter amount in {base_currency} to convert: "))
            
            # Check if the user enters a valid amount
            if amount_to_convert <= 0:
                print("⚠️ Please enter a valid amount greater than 0.")
                return

            # Perform the conversion
            converted_amount = amount_to_convert * data['rates'][target_currency]
            print(f"💱 {amount_to_convert:.2f} {base_currency} = {converted_amount:.2f} {target_currency}")
        else:
            print("⚠️ Currency not found.")
    except Exception as e:
        print(f"⚠️ Error fetching currency data: {e}")

# Simple Chatbot Assistant
def chatbot():
    print("\n🤖 Chatbot: Ask me anything! (type 'exit' to go back)")
    faq = {
        "how to deposit": "To deposit, select option 1 from the banking menu.",
        "how to withdraw": "To withdraw, select option 2 from the banking menu.",
        "how to transfer": "To transfer money, choose option 4 after logging in.",
        "how to check balance": "Your balance can be viewed by selecting option 3."
    }

    while True:
        question = input("You: ").lower()
        if question == "exit":
            break
        answer = faq.get(question, "🤖 Sorry, I don't understand that yet.")
        print("Chatbot:", answer)

# Main app loop
def main():
    accounts = load_accounts()
    user = None

    while True:
        print("\n=== Welcome to Secure Banking ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1-3): ")

        if choice == "1":
            register(accounts)
        elif choice == "2":
            user = login(accounts)
            if user:
                while True:
                    print("\n--- Banking Menu ---")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check Balance")
                    print("4. Transfer Money")
                    print("5. Generate Monthly Statement")
                    print("6. Currency Converter")
                    print("7. Chatbot Assistant")
                    print("8. Logout")
                    option = input("Select an option (1-8): ")

                    if option == "1":
                        deposit(accounts, user)
                    elif option == "2":
                        withdraw(accounts, user)
                    elif option == "3":
                        check_balance(accounts, user)
                    elif option == "4":
                        transfer(accounts, user)
                    elif option == "5":
                        generate_statement(accounts, user)
                    elif option == "6":
                        currency_converter(accounts, user)
                    elif option == "7":
                        chatbot()
                    elif option == "8":
                        print("🔒 Logged out.")
                        break
                    else:
                        print("⚠️ Invalid choice.")
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid option.")

if __name__ == "__main__":
    main()
