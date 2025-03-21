from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    UserType = db.Column(db.String(20), nullable=False)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(200), nullable=False)

class Vehicle(db.Model):
    VehicleID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID', ondelete='CASCADE'))
    VehicleType = db.Column(db.String(50))
    LicensePlate = db.Column(db.String(20), unique=True)
    Make = db.Column(db.String(255))
    Model = db.Column(db.String(255))
    Color = db.Column(db.String(50))

class ParkingSlot(db.Model):
    ParkingSlotID = db.Column(db.Integer, primary_key=True)
    SlotNumber = db.Column(db.String(50), unique=True, nullable=False)
    IsOccupied = db.Column(db.Boolean, default=False)
    VehicleID = db.Column(db.Integer, db.ForeignKey('vehicle.VehicleID', ondelete='SET NULL'))

class ParkingTransaction(db.Model):
    TransactionID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'))
    VehicleID = db.Column(db.Integer, db.ForeignKey('vehicle.VehicleID'))
    ParkingSlotID = db.Column(db.Integer, db.ForeignKey('parking_slot.ParkingSlotID'))
    EntryTime = db.Column(db.DateTime)
    ExitTime = db.Column(db.DateTime)
    PaymentAmount = db.Column(db.Numeric(10, 2), default=0.00)
    PaymentMethod = db.Column(db.String(50))
    DiscountRate = db.Column(db.Numeric(3, 2), default=0.00)
