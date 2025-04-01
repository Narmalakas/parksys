import tkinter as tk
from tkinter import messagebox
from database import Database


class RegisterVehiclePage(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        tk.Label(self, text="Register Vehicle", font=("Arial", 16)).pack(pady=10)

        # Navigation Buttons (Aligned in One Row)
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=5)

        tk.Button(nav_frame, text="Home", command=lambda: master.show_home(master.user)).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Available Slots", command=master.show_available_slots).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="My Vehicles", command=master.show_my_vehicles).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="History", command=master.show_parking_history).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Logout", command=master.show_login).pack(side=tk.LEFT, padx=5)

        # Vehicle Type Dropdown
        tk.Label(self, text="Vehicle Type:").pack()
        self.vehicle_type_var = tk.StringVar(value="Car")
        tk.OptionMenu(self, self.vehicle_type_var, "Car", "Motorcycle").pack()

        # License Plate Entry
        tk.Label(self, text="License Plate:").pack()
        self.license_plate_entry = tk.Entry(self)
        self.license_plate_entry.pack()

        # Make Entry
        tk.Label(self, text="Make:").pack()
        self.make_entry = tk.Entry(self)
        self.make_entry.pack()

        # Model Entry
        tk.Label(self, text="Model:").pack()
        self.model_entry = tk.Entry(self)
        self.model_entry.pack()

        # Color Entry
        tk.Label(self, text="Color:").pack()
        self.color_entry = tk.Entry(self)
        self.color_entry.pack()

        # Submit Button
        tk.Button(self, text="Register Vehicle", command=self.register_vehicle).pack(pady=10)

    def register_vehicle(self):
        """Registers a vehicle for the logged-in user"""
        vehicle_type = self.vehicle_type_var.get()
        license_plate = self.license_plate_entry.get().strip()
        make = self.make_entry.get().strip()
        model = self.model_entry.get().strip()
        color = self.color_entry.get().strip()

        if not (vehicle_type and license_plate and make and model and color):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Check if license plate already exists
        query = "SELECT * FROM Vehicles WHERE LicensePlate = %s"
        existing_vehicle = self.db.fetch_one(query, (license_plate,))
        if existing_vehicle:
            messagebox.showerror("Error", "License plate already registered!")
            return

        # Insert into database
        insert_query = """
            INSERT INTO Vehicles (UserID, VehicleType, LicensePlate, Make, Model, Color)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.execute(insert_query, (self.user["UserID"], vehicle_type, license_plate, make, model, color))

        messagebox.showinfo("Success", "Vehicle registered successfully!")
        self.master.show_my_vehicles()  # Redirect to My Vehicles page after registration
