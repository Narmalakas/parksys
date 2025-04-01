import tkinter as tk
from tkinter import messagebox

from home import HomePage
from availableSlot import AvailableSlots
from myVehicle import MyVehiclesPage
from registerVehicle import RegisterVehiclePage
from history import ParkingHistoryPage
from login import LoginPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Parking System")
        self.geometry("600x400")
        self.current_page = None
        self.show_login()

    def show_login(self):
        """ Show login page """
        self.switch_page(LoginPage)

    def show_home(self, user):
        self.user = user  # Store user for later use
        self.switch_page(HomePage, user)

    def show_available_slots(self):
        if hasattr(self, "user"):
            self.switch_page(AvailableSlots, self.user)
        else:
            messagebox.showerror("Error", "User not found. Please log in again.")

    def show_my_vehicles(self):
        if hasattr(self, "user"):  # Ensure user exists
            self.switch_page(MyVehiclesPage, self.user)
        else:
            messagebox.showerror("Error", "User not found. Please log in again.")

    def show_register_vehicle(self):
        """ Show register vehicle page """
        if hasattr(self, "user"):  # Ensure user exists
            self.switch_page(RegisterVehiclePage, self.user)
        else:
            messagebox.showerror("Error", "User not found. Please log in again.")

    def show_parking_history(self):
        """ Show parking history page """
        if hasattr(self, "user"):  # Ensure user exists
            self.switch_page(ParkingHistoryPage, self.user)
        else:
            messagebox.showerror("Error", "User not found. Please log in again.")

    def switch_page(self, page_class, *args):
        """ Switch pages inside the main window """
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = page_class(self, *args)
        self.current_page.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
