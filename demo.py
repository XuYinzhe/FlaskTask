from flask import Flask
from flask import render_template
from flask import request

app=Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def _login():
    if request.method == "POST":
       email = request.form.get("email")
       password = request.form.get("pass") 
       return email + password

@app.route('/signin')
def signin():
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)