# !/usr/bin/bash
import sys, os

accounts = {
    "1234567890": {"pin": "1234", "balance": 1000.0},
}

current_user = None

def login():
    global current_user
    print("=== Welcome to the ATM ===")
    account_number = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    if account_number in accounts and accounts[account_number]["pin"] == pin:
        current_user = account_number
        print("Login successful.")
        return True
    else:
        print("Invalid account number or PIN.")
        return False
    

def show_menu():
    print("\n===== ATM Menu =====")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("0. Exit")


def check_balance():
    balance = accounts[current_user]["balance"]
    print(f"\nYour current balance is: ${balance:.2f}")


def deposit_money():
    amount = input("Enter amount to deposit: $")
    if amount.replace('.', '', 1).isdigit():
        amount = float(amount)
        if amount > 0:
            accounts[current_user]["balance"] += amount
            print(f"${amount:.2f} deposited successfully.")
        else:
            print("Please enter a positive amount.")
    else:
        print("Invalid amount entered.")


def withdraw_money():
    amount = input("Enter amount to withdraw: $")
    if amount.replace('.', '', 1).isdigit():
        amount = float(amount)
        balance = accounts[current_user]["balance"]
        if amount <= balance and amount > 0:
            accounts[current_user]["balance"] -= amount
            print(f"${amount:.2f} withdrawn successfully.")
        elif amount > balance:
            print("Insufficient balance.")
        else:
            print("Please enter a positive amount.")
    else:
        print("Invalid amount entered.")

if login():
    while True:
        show_menu()
        option = input("Choose an option (1-4): ")

        if option == '1':
            check_balance()
        elif option == '2':
            deposit_money()
        elif option == '3':
            withdraw_money()
        elif option == '0':
            print("Thank you for using the ATM. Goodbye.")
            break
        else:
            print("Invalid option. Please try again.")
