from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RegisterForm, LoginForm
from datetime import datetime
from models import db, Users, ParkingTransactions, ParkingSlots, Vehicles  # Import Vehicle model
from flask import render_template
from flask_login import login_required, current_user


app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        active_park = ParkingTransactions.query.filter_by(UserID=current_user.UserID, ExitTime=None).first()
        return render_template('index.html', active_park=active_park)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.Password.data).decode('utf-8')
        user = Users(UserType=form.UserType.data, FirstName=form.FirstName.data, LastName=form.LastName.data, Email=form.Email.data, Password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(Email=form.Email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.Password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/history')
@login_required
def history():
    transactions = ParkingTransactions.query.filter_by(UserID=current_user.UserID).all()
    return render_template('history.html', transactions=transactions)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
