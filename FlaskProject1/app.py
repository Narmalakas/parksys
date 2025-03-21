from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from datetime import datetime
import os

from forms import LoginForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/parkingv2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# Database Models
class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    UserType = db.Column(db.Enum('Student', 'Faculty', 'Visitor'), nullable=False)
    FirstName = db.Column(db.String(255))
    LastName = db.Column(db.String(255))
    Email = db.Column(db.String(255), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(20))
    Password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.UserID)


class ParkingSlot(db.Model):
    __tablename__ = 'parkingslots'
    ParkingSlotID = db.Column(db.Integer, primary_key=True)
    SlotNumber = db.Column(db.String(50), unique=True, nullable=False)
    IsOccupied = db.Column(db.Boolean, default=False)


class ParkingTransaction(db.Model):
    __tablename__ = 'parkingtransactions'
    TransactionID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    ParkingSlotID = db.Column(db.Integer, db.ForeignKey('parkingslots.ParkingSlotID'))
    EntryTime = db.Column(db.DateTime, default=datetime.utcnow)
    ExitTime = db.Column(db.DateTime, nullable=True)
    PaymentAmount = db.Column(db.Numeric(10, 2), default=0.00)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Home Route
@app.route('/')
def home():
    if current_user.is_authenticated:
        active_park = ParkingTransaction.query.filter_by(UserID=current_user.UserID, ExitTime=None).first()
        return render_template('index.html', active_park=active_park)
    return redirect(url_for('login'))


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
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html', form=form)


# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# History Route
@app.route('/history')
@login_required
def history():
    transactions = ParkingTransaction.query.filter_by(UserID=current_user.UserID).all()
    return render_template('history.html', transactions=transactions)


# Parking Slot Selection
@app.route('/park/<int:slot_id>', methods=['GET'])
@login_required
def park(slot_id):
    active_park = ParkingTransaction.query.filter_by(UserID=current_user.UserID, ExitTime=None).first()
    if active_park:
        flash('You already have an active parking session.', 'warning')
        return redirect(url_for('home'))

    slot = ParkingSlot.query.get(slot_id)
    if not slot or slot.IsOccupied:
        flash('Selected parking slot is not available.', 'danger')
        return redirect(url_for('home'))

    new_transaction = ParkingTransaction(
        UserID=current_user.UserID,
        ParkingSlotID=slot.ParkingSlotID,
        EntryTime=datetime.utcnow()
    )
    db.session.add(new_transaction)
    slot.IsOccupied = True
    db.session.commit()

    flash('You have successfully parked.', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
