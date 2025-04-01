import tkinter as tk
from tkinter import messagebox
from database import Database
from login import LoginPage
import bcrypt

class RegisterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db = Database()

        tk.Label(self, text="Register", font=("Arial", 16)).pack(pady=20)

        tk.Label(self, text="First Name:").pack()
        self.first_name_entry = tk.Entry(self)
        self.first_name_entry.pack()

        tk.Label(self, text="Last Name:").pack()
        self.last_name_entry = tk.Entry(self)
        self.last_name_entry.pack()

        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        tk.Label(self, text="Phone Number:").pack()
        self.phone_entry = tk.Entry(self)
        self.phone_entry.pack()

        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Label(self, text="User Type:").pack()
        self.user_type_var = tk.StringVar(value="Student")
        tk.OptionMenu(self, self.user_type_var, "Student", "Faculty", "Visitor").pack()

        tk.Button(self, text="Register", command=self.register).pack(pady=10)
        tk.Button(self, text="Back to Login", command=lambda: master.switch_page(LoginPage)).pack()



    def register(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type_var.get()

        if not (first_name and last_name and email and password):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Hash the password before storing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            self.db.execute(
                "INSERT INTO Users (UserType, FirstName, LastName, Email, PhoneNumber, Password) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_type, first_name, last_name, email, phone, hashed_password))
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.master.switch_page(LoginPage)
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {e}")
