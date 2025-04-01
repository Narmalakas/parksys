import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Login System")
        self.root.geometry("300x250")

        tk.Label(root, text="Email").pack()
        self.email_entry = tk.Entry(root)
        self.email_entry.pack()

        tk.Label(root, text="Password").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login).pack()
        tk.Button(root, text="Sign Up", command=self.controller.show_signup).pack()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        self.controller.login(email, password)


class SignupView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Sign Up")
        self.root.geometry("300x350")

        tk.Label(root, text="User Type").pack()
        self.user_type_var = tk.StringVar()
        self.user_type_dropdown = ttk.Combobox(root, textvariable=self.user_type_var,
                                               values=["Student", "Faculty", "Visitor", "Admin"])
        self.user_type_dropdown.pack()

        tk.Label(root, text="First Name").pack()
        self.first_name_entry = tk.Entry(root)
        self.first_name_entry.pack()

        tk.Label(root, text="Last Name").pack()
        self.last_name_entry = tk.Entry(root)
        self.last_name_entry.pack()

        tk.Label(root, text="Email").pack()
        self.email_entry = tk.Entry(root)
        self.email_entry.pack()

        tk.Label(root, text="Phone Number").pack()
        self.phone_entry = tk.Entry(root)
        self.phone_entry.pack()

        tk.Label(root, text="Password").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Register", command=self.register).pack()

    def register(self):
        self.controller.register_user(
            self.user_type_var.get(),
            self.first_name_entry.get(),
            self.last_name_entry.get(),
            self.email_entry.get(),
            self.phone_entry.get(),
            self.password_entry.get(),
        )