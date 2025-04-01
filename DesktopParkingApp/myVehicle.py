import tkinter as tk
from database import Database

class MyVehiclesPage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        # Navigation Buttons (Top)
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, pady=10)

        tk.Button(button_frame, text="Home", command=lambda: self.master.show_home(self.user)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Available Slots", command=self.master.show_available_slots).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Register Vehicle", command=self.master.show_register_vehicle).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Parking History", command=self.master.show_parking_history).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Logout", command=self.master.show_login).pack(side=tk.RIGHT, padx=5)

        # Title Label
        tk.Label(self, text="Your Vehicles", font=("Arial", 16, "bold")).pack(pady=10)

        # Table Frame (Centered)
        table_frame = tk.Frame(self)
        table_frame.pack(pady=10)

        # Column Headers
        headers = ["Type", "License Plate", "Make", "Model", "Color"]
        for col, text in enumerate(headers):
            tk.Label(table_frame, text=text, font=("Arial", 12, "bold"), padx=10, pady=5).grid(row=0, column=col)

        # Vehicle List Frame
        self.vehicles_frame = tk.Frame(table_frame)
        self.vehicles_frame.grid(row=1, column=0, columnspan=len(headers))

        self.load_vehicles()

    def load_vehicles(self):
        # Clear previous data
        for widget in self.vehicles_frame.winfo_children():
            widget.destroy()

        query = "SELECT VehicleType, LicensePlate, Make, Model, Color FROM Vehicles WHERE UserID = %s"
        vehicles = self.db.fetch_all(query, (self.user["UserID"],))

        if not vehicles:
            tk.Label(self.vehicles_frame, text="No vehicles found.", font=("Arial", 12)).pack(pady=10)
        else:
            for row_idx, vehicle in enumerate(vehicles, start=1):
                tk.Label(self.vehicles_frame, text=vehicle["VehicleType"], padx=10).grid(row=row_idx, column=0)
                tk.Label(self.vehicles_frame, text=vehicle["LicensePlate"], padx=10).grid(row=row_idx, column=1)
                tk.Label(self.vehicles_frame, text=vehicle["Make"], padx=10).grid(row=row_idx, column=2)
                tk.Label(self.vehicles_frame, text=vehicle["Model"], padx=10).grid(row=row_idx, column=3)
                tk.Label(self.vehicles_frame, text=vehicle["Color"], padx=10).grid(row=row_idx, column=4)
