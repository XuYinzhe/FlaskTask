from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "User"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    # name = db.Column(db.String(1000))

class Room(db.Model):
    __tablename__ = "4223"
    __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    device_type = db.Column(db.String(100))
    control_by = db.Column(db.String(1000))
    control_with = db.Column(db.String(1000))
    link_by = db.Column(db.String(1000))
    link_with = db.Column(db.String(1000))
