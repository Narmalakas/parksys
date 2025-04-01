import tkinter as tk
from tkinter import ttk
from database import Database

class ParkingHistoryPage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        # Navigation Bar
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, pady=5)

        tk.Button(button_frame, text="Home", command=lambda: self.master.show_home(self.user)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Available Slots", command=master.show_available_slots).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="My Vehicles", command=lambda: self.master.show_my_vehicles()).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Register Vehicle", command=lambda: self.master.show_register_vehicle()).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Logout", command=lambda: self.master.show_login()).pack(side=tk.RIGHT, padx=5)

        # Title Label
        tk.Label(self, text="Parking History", font=("Arial", 16, "bold")).pack(pady=10)

        # Parking History Table
        self.tree = ttk.Treeview(self, columns=("TransactionID", "Slot", "Entry Time", "Exit Time", "Amount"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tree.heading("TransactionID", text="Transaction ID")
        self.tree.heading("Slot", text="Slot")
        self.tree.heading("Entry Time", text="Entry Time")
        self.tree.heading("Exit Time", text="Exit Time")
        self.tree.heading("Amount", text="Amount")

        self.tree.column("TransactionID", width=100, anchor="center")
        self.tree.column("Slot", width=50, anchor="center")
        self.tree.column("Entry Time", width=150, anchor="center")
        self.tree.column("Exit Time", width=150, anchor="center")
        self.tree.column("Amount", width=80, anchor="center")

        self.show_history()

    def show_history(self):
        """Fetch and display parking history for the logged-in user."""
        self.tree.delete(*self.tree.get_children())  # Clear existing entries

        query = """
            SELECT TransactionID, ParkingSlotID, EntryTime, ExitTime, PaymentAmount 
            FROM ParkingTransactions WHERE UserID = %s
        """
        history = self.db.fetch_all(query, (self.user["UserID"],))

        if history:
            for record in history:
                exit_time = record["ExitTime"] if record["ExitTime"] else "Still Parked"
                self.tree.insert("", "end", values=(
                    record["TransactionID"],
                    record["ParkingSlotID"],
                    record["EntryTime"],
                    exit_time,
                    f"₱{record['PaymentAmount']:.2f}"
                ))
        else:
            self.tree.insert("", "end", values=("No data", "", "", "", ""))

