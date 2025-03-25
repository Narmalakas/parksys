from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'  # Explicitly define table name

    id = db.Column(db.Integer, primary_key=True)
    UserType = db.Column(db.String(20), nullable=False)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(200), nullable=False)

    vehicles = db.relationship('Vehicles', backref='user', lazy=True)


class Vehicles(db.Model):
    __tablename__ = 'vehicles'

    VehicleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # FIXED Foreign Key
    LicensePlate = db.Column(db.String(20), nullable=False, unique=True)
    Make = db.Column(db.String(50), nullable=False)
    Model = db.Column(db.String(50), nullable=False)


class ParkingSlots(db.Model):
    __tablename__ = 'parkingslots'

    ParkingSlotID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SlotNumber = db.Column(db.String(50), unique=True, nullable=False)
    IsOccupied = db.Column(db.Boolean, default=False)

    # Define relationship to ParkingTransactions
    transactions = db.relationship('ParkingTransactions', back_populates='parking_slot')


class ParkingTransactions(db.Model):
    __tablename__ = 'parkingtransactions'

    TransactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    VehicleID = db.Column(db.Integer, db.ForeignKey('vehicles.VehicleID'), nullable=False)
    ParkingSlotID = db.Column(db.Integer, db.ForeignKey('parkingslots.ParkingSlotID'), nullable=False)
    EntryTime = db.Column(db.DateTime, default=db.func.current_timestamp())
    ExitTime = db.Column(db.DateTime, nullable=True)
    PaymentAmount = db.Column(db.Numeric(10, 2), default=0.00)
    PaymentMethod = db.Column(db.String(50), nullable=True)
    DiscountRate = db.Column(db.Numeric(3, 2), default=0.00)

    # Define relationship to ParkingSlots
    parking_slot = db.relationship('ParkingSlots', back_populates='transactions')

class ParkingRecord(db.Model):
    __tablename__ = 'parking_records'

    id = db.Column(db.Integer, primary_key=True)
    VehicleID = db.Column(db.Integer, db.ForeignKey('vehicles.VehicleID'), nullable=False)  # FIXED Foreign Key
    ParkingSlotID = db.Column(db.Integer, db.ForeignKey('parking_slots.ParkingSlotID'), nullable=False)  # FIXED Foreign Key
    EntryTime = db.Column(db.DateTime, nullable=False)
    ExitTime = db.Column(db.DateTime, nullable=True)  # Allow NULL for active parking
    Amount = db.Column(db.Float, nullable=False)

    def __init__(self, VehicleID, ParkingSlotID, EntryTime, ExitTime, Amount):
        self.VehicleID = VehicleID
        self.ParkingSlotID = ParkingSlotID
        self.EntryTime = EntryTime
        self.ExitTime = ExitTime
        self.Amount = Amount
