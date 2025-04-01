import tkinter as tk
from database import Database  # Ensure you have a database connection


class HomePage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        # Welcome Label
        tk.Label(self, text=f"Welcome, {self.user['FirstName']} {self.user['LastName']}!", font=("Arial", 14)).pack()

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, pady=5)

        # Navigation Buttons
        tk.Button(button_frame, text="Available Slots", command=self.master.show_available_slots).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="My Vehicles", command=self.master.show_my_vehicles).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Register Vehicle", command=self.master.show_register_vehicle).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Parking History", command=self.master.show_parking_history).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Logout", command=self.master.show_login).pack(pady=5)

        # Available Slots Section
        self.slot_display = tk.Frame(self)
        self.slot_display.pack(pady=10)
        self.display_slots()

    def display_slots(self):
        """Fetch and display available slots."""
        for widget in self.slot_display.winfo_children():
            widget.destroy()  # Clear previous slots

        slots = self.db.fetch_all("SELECT SlotNumber, IsOccupied FROM ParkingSlots")

        tk.Label(self.slot_display, text="Available Parking Slots:", font=("Arial", 12, "bold")).pack()

        for slot in slots:
            slot_text = f"Slot {slot['SlotNumber']} - {'Occupied' if slot['IsOccupied'] else 'Available'}"
            color = "red" if slot["IsOccupied"] else "green"
            tk.Label(self.slot_display, text=slot_text, fg=color).pack()

