from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    authority = db.Column(db.String(100))
    # name = db.Column(db.String(1000))

class RoomList(UserMixin, db.Model):

    __tablename__ = "RoomList"
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100))

class room_cls(UserMixin, db.Model):
     
    __abstract__ = True  # 关键语句,定义所有数据库表对应的父类
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True) 