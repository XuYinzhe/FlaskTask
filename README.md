## 1. Open COMMAND with administration
## 2. Variable Settings
```
set FLASK_APP=project
set FLASK_DEBUG=1
set FLASK_env=development
```
## 3. Database Configuration
```python
python
>>> from project import db, create_app
>>> db.create_all(app=create_app()) # create database
```
## 4. Run Flask
```
flask run
```