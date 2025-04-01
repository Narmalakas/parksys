import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from database import Database
from datetime import datetime, timedelta

class AvailableSlots(tk.Frame):
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.user = user
        self.db = Database()

        tk.Label(self, text="Available Parking Slots", font=("Arial", 16)).pack(pady=10)

        # Navigation Buttons
        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=5)
        tk.Button(nav_frame, text="Home", command=lambda: master.show_home()).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="My Vehicles", command=master.show_my_vehicles).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Register Vehicle", command=self.master.show_register_vehicle).pack(side=tk.LEFT,padx=5)
        tk.Button(nav_frame, text="History", command=master.show_parking_history).pack(side=tk.LEFT, padx=5)
        tk.Button(nav_frame, text="Logout", command=master.show_login).pack(side=tk.LEFT, padx=5)

        # Parking Slots Display
        self.slot_display = tk.Frame(self)
        self.slot_display.pack(pady=10)
        self.display_slots()

    def display_slots(self):
        """Fetch and display available parking slots with Park/Park Out button"""
        for widget in self.slot_display.winfo_children():
            widget.destroy()

        # Fetch all slots and their occupancy status
        slots = self.db.fetch_all("SELECT ParkingSlotID, SlotNumber, IsOccupied FROM ParkingSlots")

        tk.Label(self.slot_display, text="Slot No | Status | Action", font=("Arial", 12, "bold")).pack()

        for slot in slots:
            frame = tk.Frame(self.slot_display)
            frame.pack(pady=2)

            # Display slot details
            slot_text = f"Slot {slot['SlotNumber']} - {'Occupied' if slot['IsOccupied'] else 'Available'}"
            color = "red" if slot["IsOccupied"] else "green"
            tk.Label(frame, text=slot_text, fg=color).pack(side=tk.LEFT, padx=10)

            # Show Park Out button only if the slot is occupied by the current user
            if slot["IsOccupied"]:
                # Query to find the user who parked in this slot and the transaction is still active
                parked_user = self.db.fetch_one("""
                    SELECT UserID 
                    FROM ParkingTransactions 
                    WHERE ParkingSlotID = %s AND ExitTime IS NULL
                """, (slot["ParkingSlotID"],))

                if parked_user and parked_user["UserID"] == self.user["UserID"]:
                    # Park Out button only if the logged-in user is the one who parked
                    tk.Button(frame, text="Park Out", command=lambda s=slot["ParkingSlotID"]: self.park_out(s)).pack(
                        side=tk.LEFT)
            else:
                # Show Park button for available slots
                tk.Button(frame, text="Park", command=lambda s=slot["ParkingSlotID"]: self.park_vehicle(s)).pack(
                    side=tk.LEFT)

    def park_vehicle(self, slot_id):
        """Popup window for parking transaction"""
        popup = tk.Toplevel(self)
        popup.title("Park Vehicle")
        popup.geometry("300x400")

        tk.Label(popup, text=f"Parking in Slot {slot_id}", font=("Arial", 12)).pack(pady=5)

        vehicles = self.db.fetch_all(""" 
        SELECT VehicleID, Make, Model, LicensePlate 
        FROM Vehicles 
        WHERE UserID = %s 
        AND VehicleID NOT IN (SELECT VehicleID FROM ParkingTransactions WHERE ExitTime IS NULL)
        """, (self.user["UserID"],))

        if not vehicles:
            tk.Label(popup, text="No available vehicles to park!", fg="red").pack()
            return

        tk.Label(popup, text="Select Vehicle:").pack()
        self.selected_vehicle = tk.StringVar()
        vehicle_options = {f"{v['Make']} {v['Model']} ({v['LicensePlate']})": v["VehicleID"] for v in vehicles}
        vehicle_dropdown = ttk.Combobox(popup, textvariable=self.selected_vehicle, values=list(vehicle_options.keys()))
        vehicle_dropdown.pack()

        tk.Label(popup, text="Entry Date & Time:").pack()
        self.entry_date = DateEntry(popup, date_pattern="yyyy-mm-dd")
        self.entry_date.pack()
        self.entry_time = ttk.Combobox(popup, values=[f"{h:02d}:00" for h in range(24)])
        self.entry_time.pack()

        tk.Label(popup, text="Exit Date & Time:").pack()
        self.exit_date = DateEntry(popup, date_pattern="yyyy-mm-dd")
        self.exit_date.pack()
        self.exit_time = ttk.Combobox(popup, values=[f"{h:02d}:00" for h in range(24)])
        self.exit_time.pack()

        tk.Label(popup, text="Select Discount:").pack()
        self.discount_var = tk.StringVar(value="None")
        discount_options = ["None", "Student", "Faculty", "PWD", "Visitor"]
        discount_dropdown = ttk.Combobox(popup, textvariable=self.discount_var, values=discount_options)
        discount_dropdown.pack()

        discount_dropdown.bind("<<ComboboxSelected>>", lambda e: self.calculate_payment())

        self.payment_label = tk.Label(popup, text="Payment: ₱0", font=("Arial", 12, "bold"))
        self.payment_label.pack(pady=5)

        tk.Label(popup, text="Payment Method:").pack()
        self.payment_method = tk.StringVar(value="Cash")
        payment_methods = ["Cash", "Online Payment", "Credit Card"]
        payment_dropdown = ttk.Combobox(popup, textvariable=self.payment_method, values=payment_methods)
        payment_dropdown.pack()

        self.entry_date.bind("<<DateEntrySelected>>", lambda e: self.calculate_payment())
        self.entry_time.bind("<<ComboboxSelected>>", lambda e: self.calculate_payment())
        self.exit_date.bind("<<DateEntrySelected>>", lambda e: self.calculate_payment())
        self.exit_time.bind("<<ComboboxSelected>>", lambda e: self.calculate_payment())

        tk.Button(popup, text="Confirm Parking", command=lambda: self.confirm_parking(slot_id, vehicle_options, popup)).pack(pady=10)

    def calculate_payment(self):
        try:
            entry_datetime = datetime.strptime(f"{self.entry_date.get()} {self.entry_time.get()}", "%Y-%m-%d %H:%M")
            exit_datetime = datetime.strptime(f"{self.exit_date.get()} {self.exit_time.get()}", "%Y-%m-%d %H:%M")

            if exit_datetime <= entry_datetime:
                self.payment_label.config(text="Payment: ₱0")
                return

            total_hours = max(1, int((exit_datetime - entry_datetime).total_seconds() / 3600))
            base_amount = total_hours * 20
            discount_rates = {"Student": 0.20, "Faculty": 0.15, "PWD": 0.30, "Visitor": 0.10, "None": 0.00}
            discount = discount_rates.get(self.discount_var.get(), 0) * base_amount
            total_amount = base_amount - discount

            self.payment_label.config(text=f"Payment: ₱{total_amount:.2f}")
        except ValueError:
            self.payment_label.config(text="Payment: ₱0")

    def confirm_parking(self, slot_id, vehicles, popup):
        if not self.selected_vehicle.get():
            messagebox.showerror("Error", "Please select a vehicle.")
            return

        try:
            vehicle_id = vehicles[self.selected_vehicle.get()]
            entry_datetime = datetime.strptime(f"{self.entry_date.get()} {self.entry_time.get()}", "%Y-%m-%d %H:%M")
            exit_datetime = datetime.strptime(f"{self.exit_date.get()} {self.exit_time.get()}", "%Y-%m-%d %H:%M")

            if exit_datetime <= entry_datetime:
                messagebox.showerror("Error", "Exit time must be later than entry time.")
                return

            # Calculate payment
            total_hours = max(1, int((exit_datetime - entry_datetime).total_seconds() / 3600))
            base_amount = total_hours * 20
            discount_rates = {"Student": 0.20, "Faculty": 0.15, "PWD": 0.30, "Visitor": 0.10, "None": 0.00}
            discount = discount_rates.get(self.discount_var.get(), 0) * base_amount
            total_amount = base_amount - discount
            discount_rate = discount_rates.get(self.discount_var.get(), 0)

            payment_method = self.payment_method.get()

            # Insert into ParkingTransactions
            query = """
            INSERT INTO ParkingTransactions (UserID, VehicleID, ParkingSlotID, EntryTime, ExitTime, PaymentAmount, PaymentMethod, DiscountRate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute(query, (
                self.user["UserID"], vehicle_id, slot_id, entry_datetime, None, total_amount, payment_method,
                discount_rate
            ))

            # Update the slot to occupied
            self.db.execute("UPDATE ParkingSlots SET IsOccupied = TRUE WHERE ParkingSlotID = %s", (slot_id,))

            messagebox.showinfo("Success", "Vehicle parked successfully!")
            popup.destroy()
            self.display_slots()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def park_out(self, slot_id):
        """Park out the vehicle and free the parking slot"""
        try:
            # Update the parking transaction with ExitTime
            exit_time = datetime.now()
            self.db.execute("""
                UPDATE ParkingTransactions 
                SET ExitTime = %s 
                WHERE ParkingSlotID = %s AND ExitTime IS NULL
            """, (exit_time, slot_id))

            # Update the slot to available
            self.db.execute("""
                UPDATE ParkingSlots 
                SET IsOccupied = FALSE 
                WHERE ParkingSlotID = %s
            """, (slot_id,))

            messagebox.showinfo("Success", "Vehicle has been parked out successfully!")
            self.display_slots()  # Refresh the slot display automatically
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
