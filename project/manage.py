from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from . import db, create_app

app = create_app()
manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

@manager.command
def init_db():
    # import json
    # # 1. 获取数据列表
    # with open('data_list.json', 'r') as f:
    #     ship_list = json.load(f)
    # # 2. 动态创建数据库表
    # for datain data_list:
    #     data_id = data['ID']
    #     get_model(data_id)

    with app.app_context():
        db.create_all(app=app)

    # print('create table success')