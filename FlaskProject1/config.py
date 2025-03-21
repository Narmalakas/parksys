import os

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
class Config:

    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/parkingv2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
