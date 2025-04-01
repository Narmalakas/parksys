import tkinter as tk
from tkinter import messagebox
import bcrypt
from database import Database
from home import HomePage

class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = Database()

        tk.Label(self, text="Login", font=("Arial", 16)).pack(pady=20)

        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Register", command=lambda: master.switch_page(RegisterPage)).pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        # Fetch stored hashed password from the database
        query = "SELECT UserID, UserType, FirstName, LastName, Email, Password FROM Users WHERE Email = %s"
        user = self.db.fetch_one(query, (email,))

        if user and bcrypt.checkpw(password.encode('utf-8'), user["Password"].encode('utf-8')):
            self.master.show_home(user)  # Login successful
        else:
            messagebox.showerror("Error", "Wrong email or password")


# Import at the bottom to avoid circular import
from register import RegisterPage
