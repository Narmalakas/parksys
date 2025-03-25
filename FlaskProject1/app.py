
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from datetime import datetime
from forms import VehicleForm, LoginForm, RegisterForm
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import datetime
from flask_login import login_required
from datetime import timedelta
from flask_login import current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change if using another MySQL user
app.config['MYSQL_PASSWORD'] = '123456'  # Your MySQL password
app.config['MYSQL_DB'] = 'parkingv2'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Ensures dictionary-like cursor output

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/parkingv2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)


mysql = MySQL(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Database Models
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    UserType = db.Column(db.Enum('Student', 'Faculty', 'Visitor'), nullable=False)
    FirstName = db.Column(db.String(255), nullable=False)
    LastName = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(20), unique=True)
    Password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.UserID)


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



class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    VehicleID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID', ondelete="CASCADE"), nullable=False)
    VehicleType = db.Column(db.String(50), nullable=False)
    LicensePlate = db.Column(db.String(20), unique=True, nullable=False)
    Make = db.Column(db.String(255), nullable=False)
    Model = db.Column(db.String(255), nullable=False)
    Color = db.Column(db.String(50), nullable=False)

    user = db.relationship('Users', backref=db.backref('vehicles', lazy=True, cascade="all, delete"))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Home Route
@app.route('/')
@login_required  # Ensures only authenticated users can access the home page
def home():
    # Fetch available parking slots
    available_slots = ParkingSlots.query.with_entities(ParkingSlots.SlotNumber).filter_by(IsOccupied=False).all()

    return render_template('index.html', available_slots=available_slots)



# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = Users(
            UserType=form.user_type.data,
            FirstName=form.first_name.data,
            LastName=form.last_name.data,
            Email=form.email.data,
            PhoneNumber=form.phone_number.data,
            Password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(Email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.password.data):
            login_user(user, remember=False)
            session['user_id'] = user.UserID  # Store user ID in session
            return redirect(url_for('home'))
        else:
            flash('Email or password is incorrect', 'danger')

    return render_template('login.html', form=form)


# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

# History Route
@app.route('/history')
@login_required
def history():
    try:
        user_id = current_user.UserID  # Correct way to get user ID
        transactions = ParkingTransactions.query.filter_by(UserID=user_id).order_by(ParkingTransactions.EntryTime.desc()).all()

        return render_template('history.html', transactions=transactions)
    except Exception as e:
        print(f"Error fetching history: {e}")  # Log error for debugging
        return "An error occurred while retrieving parking history.", 500


@app.route('/register_vehicle', methods=['GET', 'POST'])
@login_required
def register_vehicle():
    form = VehicleForm()
    if form.validate_on_submit():
        # Check if the license plate already exists in the database
        existing_vehicle = Vehicles.query.filter_by(LicensePlate=form.license_plate.data).first()
        if existing_vehicle:
            flash('This license plate is already registered. Please use a different one.', 'danger')
            return redirect(url_for('register_vehicle'))

        # If it's a new plate, register the vehicle
        new_vehicle = Vehicles(
            UserID=current_user.UserID,
            VehicleType=form.vehicle_type.data,
            LicensePlate=form.license_plate.data,
            Make=form.make.data,
            Model=form.model.data,
            Color=form.color.data
        )
        db.session.add(new_vehicle)
        db.session.commit()
        flash('Vehicle registered successfully!', 'success')
        return redirect(url_for('view_vehicles'))

    return render_template('register_vehicle.html', form=form)



@app.route('/vehicles')
@login_required
def view_vehicles():
    vehicles = Vehicles.query.filter_by(UserID=current_user.UserID).all()
    return render_template('vehicles.html', vehicles=vehicles)

@app.route('/parking')
@login_required
def parking():
    slots = ParkingSlots.query.all()  # Fetch all parking slots
    vehicles = Vehicles.query.filter_by(UserID=current_user.UserID).all()  # Fetch user's vehicles
    return render_template('available_slots.html', slots=slots, vehicles=vehicles)


@app.route('/available_slots')
@login_required
def available_slots():
    slots = ParkingSlots.query.all()  # Fetch all parking slots
    vehicles = Vehicles.query.filter_by(UserID=current_user.UserID).all()  # Fetch user's vehicles

    # Fetch transactions for the current user
    active_transactions = {t.ParkingSlotID: t for t in ParkingTransactions.query.filter_by(UserID=current_user.UserID, ExitTime=None).all()}

    return render_template('available_slots.html', slots=slots, vehicles=vehicles, active_transactions=active_transactions)

@app.route('/park_vehicle', methods=['POST'])
@login_required
def park_vehicle():
    try:
        vehicle_id = request.form.get('vehicle_id')
        slot_id = request.form.get('slot_id')
        entry_time = request.form.get('entry_time') or datetime.datetime.now()
        discount = request.form.get('discount', 0.00)
        payment_amount = request.form.get('payment_amount', "0.00").replace("₱", "")
        payment_method = request.form.get('payment_method', None)

        # Ensure valid data
        if not vehicle_id or not slot_id:
            flash('Please select a vehicle and parking slot.', 'danger')
            return redirect(url_for('available_slots'))

        # Check if the vehicle is already parked
        existing_transaction = ParkingTransactions.query.filter_by(VehicleID=vehicle_id, ExitTime=None).first()
        if existing_transaction:
            flash('This vehicle is already parked. Please park out before parking again.', 'danger')
            return redirect(url_for('available_slots'))

        # Check if the parking slot is available
        slot = ParkingSlots.query.get(slot_id)
        if not slot or slot.IsOccupied:
            flash('Selected parking slot is unavailable.', 'danger')
            return redirect(url_for('available_slots'))

        # Create a new parking transaction
        new_transaction = ParkingTransactions(
            UserID=current_user.UserID,
            VehicleID=vehicle_id,
            ParkingSlotID=slot_id,
            EntryTime=entry_time,
            DiscountRate=float(discount),
            PaymentAmount=float(payment_amount),
            PaymentMethod=payment_method
        )
        db.session.add(new_transaction)

        # Mark the parking slot as occupied
        slot.IsOccupied = True
        db.session.commit()

        flash('Parking confirmed successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('available_slots'))


@app.route('/park_out/<int:slot_id>', methods=['POST'])
@login_required
def park_out(slot_id):
    try:
        transaction = ParkingTransactions.query.filter_by(ParkingSlotID=slot_id, ExitTime=None).first()
        if transaction:
            transaction.ExitTime = datetime.datetime.now()
            db.session.commit()

        # Update the slot status back to "Available"
        slot = ParkingSlots.query.get(slot_id)
        if slot:
            slot.IsOccupied = False
            db.session.commit()

        flash('You have successfully parked out!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')

    return redirect(url_for('available_slots'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
