from model import UserModel
from tkinter import messagebox


class Controller:
    def __init__(self, root):
        self.root = root
        self.user_model = UserModel()
        self.show_login()

    def show_login(self):
        from views import LoginView
        self.root.destroy()
        self.root = tk.Tk()
        self.view = LoginView(self.root, self)
        self.root.mainloop()

    def show_signup(self):
        from views import SignupView
        self.root.destroy()
        self.root = tk.Tk()
        self.view = SignupView(self.root, self)
        self.root.mainloop()

    def login(self, email, password):
        user = self.user_model.authenticate_user(email, password)
        if user:
            messagebox.showinfo("Success", f"Welcome, {user[2]} {user[3]} ({user[1]})")
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register_user(self, user_type, first_name, last_name, email, phone, password):
        if not (user_type and first_name and last_name and email and password):
            messagebox.showerror("Error", "All fields are required")
            return

        if self.user_model.register_user(user_type, first_name, last_name, email, phone, password):
            messagebox.showinfo("Success", "User registered successfully!")
            self.show_login()
        else:
            messagebox.showerror("Error", "Registration failed")