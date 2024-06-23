import tkinter as tk
from tkinter import messagebox

class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = []

    def add_transaction(self, transaction):
        self.transaction_history.append(transaction)

class AuthScreen(tk.Frame):
    def __init__(self, atm):
        super().__init__(atm.root, bg="#8E9AAF")
        self.atm = atm
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="User ID", bg="#8E9AAF", fg="white", font=("Times New Roman", 14)).pack(pady=10)
        self.user_id_entry = tk.Entry(self, font=("Times New Roman", 14))
        self.user_id_entry.pack(pady=5)

        tk.Label(self, text="PIN", bg="#8E9AAF", fg="white", font=("Times New Roman", 14)).pack(pady=10)
        self.pin_entry = tk.Entry(self, show="*", font=("Times New Roman", 14))
        self.pin_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.login, width=20, height=2, font=("Times New Roman", 14)).pack(pady=20)

    def login(self):
        user_id = self.user_id_entry.get()
        pin = self.pin_entry.get()
        self.atm.authenticate_user(user_id, pin)

class MainMenuScreen(tk.Frame):
    def __init__(self, atm):
        super().__init__(atm.root, bg="#8E9AAF")
        self.atm = atm
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Octanet Bank", bg="#8E9AAF", fg="white", font=("Times New Roman", 22)).pack(pady=10)
        tk.Label(self, text="ATM Main Menu", bg="#8E9AAF", fg="white", font=("Times New Roman", 24, "bold")).pack(pady=10)
        tk.Label(self, text="Welcome to Octanet Bank", bg="#8E9AAF", fg="white", font=("Times New Roman", 14)).pack(pady=10)

        button_frame = tk.Frame(self, bg="#8E9AAF")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="View Transaction History", command=self.view_transaction_history, width=20, height=2, font=("Times New Roman", 14)).pack(pady=10)
        tk.Button(button_frame, text="Withdraw", command=self.withdraw, width=20, height=2, font=("Times New Roman", 14)).pack(pady=10)
        tk.Button(button_frame, text="Deposit", command=self.deposit, width=20, height=2, font=("Times New Roman", 14)).pack(pady=10)
        tk.Button(button_frame, text="Transfer", command=self.transfer, width=20, height=2, font=("Times New Roman", 14)).pack(pady=10)
        tk.Button(button_frame, text="Check Balance", command=self.check_balance, width=20, height=2, font=("Times New Roman", 14)).pack(pady=10)
        tk.Button(button_frame, text="Logout", command=self.logout, width=20, height=2, font=("Times New Roman", 14)).pack(pady=10)

    def view_transaction_history(self):
        self.atm.show_transaction_screen()
        self.atm.transaction_screen.show_transaction_history()

    def withdraw(self):
        self.atm.show_transaction_screen()
        self.atm.transaction_screen.show_withdraw()

    def deposit(self):
        self.atm.show_transaction_screen()
        self.atm.transaction_screen.show_deposit()

    def transfer(self):
        self.atm.show_transaction_screen()
        self.atm.transaction_screen.show_transfer_user()

    def check_balance(self):
        self.atm.show_transaction_screen()
        self.atm.transaction_screen.show_balance()

    def logout(self):
        self.atm.logout()

class TransactionScreen(tk.Frame):
    def __init__(self, atm):
        super().__init__(atm.root, bg="#8E9AAF")
        self.atm = atm
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="", bg="#8E9AAF", fg="white", font=("Times New Roman", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(self, font=("Times New Roman", 14))
        self.entry.pack(pady=5)

        self.button = tk.Button(self, text="Submit", command=self.submit, width=20, height=2, font=("Times New Roman", 14))
        self.button.pack(pady=20)

        self.back_button = tk.Button(self, text="Back", command=self.back_to_main_menu, width=20, height=2, font=("Times New Roman", 14))
        self.back_button.pack(pady=20)

    def show_transaction_history(self):
        self.label.config(text="Transaction History")
        self.entry.pack_forget()
        self.button.pack_forget()

        if self.atm.current_user.transaction_history:
            history = "\n".join(self.atm.current_user.transaction_history)
        else:
            history = "No transactions yet."
        messagebox.showinfo("Transaction History", history)

    def show_withdraw(self):
        self.label.config(text="Enter amount to withdraw")
        self.entry.pack()
        self.button.pack()

    def show_deposit(self):
        self.label.config(text="Enter amount to deposit")
        self.entry.pack()
        self.button.pack()

    def show_transfer_user(self):
        self.label.config(text="Enter user ID to transfer to")
        self.entry.pack()
        self.button.config(command=self.submit_transfer_user)
        self.button.pack()

    def show_transfer_amount(self):
        self.label.config(text="Enter amount to transfer")
        self.entry.pack()
        self.button.config(command=self.submit_transfer_amount)
        self.button.pack()

    def show_balance(self):
        self.label.config(text="Balance")
        self.entry.pack_forget()
        self.button.pack_forget()
        balance = self.atm.current_user.balance
        messagebox.showinfo("Balance", f"Your balance is: ${balance}")

    def submit_transfer_user(self):
        self.transfer_user_id = self.entry.get()
        self.entry.delete(0, tk.END)
        self.show_transfer_amount()

    def submit_transfer_amount(self):
        amount = int(self.entry.get())
        recipient = self.atm.users.get(self.transfer_user_id)
        if recipient and self.atm.current_user.balance >= amount:
            self.atm.current_user.balance -= amount
            recipient.balance += amount
            self.atm.current_user.add_transaction(f"Transfer to {self.transfer_user_id}: {amount}")
            recipient.add_transaction(f"Transfer from {self.atm.current_user.user_id}: {amount}")
            messagebox.showinfo("Success", "Transfer successful")
        elif not recipient:
            messagebox.showerror("Error", "Recipient not found")
        else:
            messagebox.showerror("Error", "Insufficient funds")
        self.entry.delete(0, tk.END)

    def submit(self):
        action = self.label.cget("text")
        if action == "Enter amount to withdraw":
            amount = int(self.entry.get())
            if self.atm.current_user.balance >= amount:
                self.atm.current_user.balance -= amount
                self.atm.current_user.add_transaction(f"Withdraw: {amount}")
                messagebox.showinfo("Success", "Withdrawal successful")
            else:
                messagebox.showerror("Error", "Insufficient funds")
        elif action == "Enter amount to deposit":
            amount = int(self.entry.get())
            self.atm.current_user.balance += amount
            self.atm.current_user.add_transaction(f"Deposit: {amount}")
            messagebox.showinfo("Success", "Deposit successful")
        self.entry.delete(0, tk.END)

    def back_to_main_menu(self):
        self.atm.show_main_menu_screen()

class ATM:
    def __init__(self, root):
        self.root = root
        self.root.title("Octanet Bank")
        self.root.configure(bg="#8E9AAF")
        self.users = self.load_users()
        self.current_user = None

        self.auth_screen = AuthScreen(self)
        self.main_menu_screen = MainMenuScreen(self)
        self.transaction_screen = TransactionScreen(self)

        self.auth_screen.pack()

    def load_users(self):
        return {
            'aruna': User('aruna', '1234', 5000),
            'ravi': User('ravi', '4567', 10000),
            'saipriya': User('saipriya', '9999', 15000),
        }

    def authenticate_user(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.pin == pin:
            self.current_user = user
            self.show_main_menu_screen()
        else:
            messagebox.showerror("Error", "Invalid user ID or PIN")

    def show_auth_screen(self):
        self.auth_screen.pack()
        self.main_menu_screen.pack_forget()
        self.transaction_screen.pack_forget()

    def show_main_menu_screen(self):
        self.auth_screen.pack_forget()
        self.main_menu_screen.pack()
        self.transaction_screen.pack_forget()

    def show_transaction_screen(self):
        self.auth_screen.pack_forget()
        self.main_menu_screen.pack_forget()
        self.transaction_screen.pack()

    def logout(self):
        self.current_user = None
        self.show_auth_screen()

if __name__ == "__main__":
    root = tk.Tk()
    atm = ATM(root)
    root.mainloop()
