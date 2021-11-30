from flask_login import UserMixin
from . import db

type_list = ['projector',
             'screen',
             'microphone',
             'visualizer',
             'speaker',
             'apple',
             'windows',
             'android',]

func_list = ['ON', 
             'CONNECTION', 
             'PROJECTION',]

class User(UserMixin, db.Model):
    
    __tablename__ = "User"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    authority = db.Column(db.String(100))
    # name = db.Column(db.String(1000))

class RoomList(UserMixin, db.Model):

    __tablename__ = "RoomList"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(100))
    room_img_prev = db.Column(db.String(100))
    room_img_long = db.Column(db.String(100))
    room_loc = db.Column(db.String(100))

class room_cls(UserMixin, db.Model):
     
    __abstract__ = True 
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True) 
    device  = db.Column(db.String(100))
    type = db.Column(db.String(100))
    location = db.Column(db.String(100))

    func = db.Column(db.String(100)) # "ON/P/C = 1,1,1; ON/C = 1,0,1"

    oncontrol = db.Column(db.String(1000))
    oncontrolby = db.Column(db.String(1000))
    ifon = db.Column(db.Integer) # init = False, select = True

    projectionto = db.Column(db.String(1000))
    projectionby = db.Column(db.String(1000)) 
    ifprojection = db.Column(db.Integer) # init = False, link = True

    connectionto = db.Column(db.String(1000))
    connectionby = db.Column(db.String(1000))
    ifconnection = db.Column(db.Integer) # init = False, connect = True
