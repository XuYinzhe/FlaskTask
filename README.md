## 1. Open COMMAND with administration
## 2. Variable Settings
```
set FLASK_APP=project
set FLASK_DEBUG=1
set FLASK_env=development
```
## 3. Database Configuration
```python
from project import db, create_app, get_table_model_cls, insert_room
db.create_all(app=create_app()) # create database
insert_room('') # create new room table
```
## 4. Run Flask
```
flask run
```