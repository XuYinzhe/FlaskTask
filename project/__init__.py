from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models

HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'avata'
USERNAME = 'root'
PASSWORD = 'root'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    # engine = db.get_engine()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def get_room_cls(room_id):

    from .models import room_cls
    from .models import RoomList

    room_name = table_name = "room_" + room_id
    # room = RoomList.query.filter_by(room_name=room_name).first()

    # if not room:
    #     room_content = type(room_name, (room_cls, ), {'__tablename__': table_name})
    #     newroom = RoomList(room_name=room_name)

    #     db.session.add(newroom)
    #     db.session.commit() 
    # else:
    #     return "Room already exist"

    room_content = type(room_name, (room_cls, ), {'__tablename__': table_name}, __table_args__ = {"extend_existing": True})

    return 

def insert_room(room_id):
    # from .models import User

    # print(User.query.get(1))
    table = get_room_cls(room_id)
    # app = create_app()

    # with app.app_context():
    #     db.create_all()
    db.create_all(app=create_app())