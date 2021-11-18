from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask.helpers import url_for
from flask import flash, get_flashed_messages

app=Flask(__name__)

@app.route('/')
def loading():
    return render_template('loading.html')

@app.route('/',methods=['POST'])
def _loading():
    if request.method=="POST":
        return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST'])
def _login():
    if request.method == "POST":
        email = request.form.get("login_email")
        password = request.form.get("login_pass") 
        if email=='':
            flash('Email is empty!')
            return render_template('login.html')
        elif password=='':
            flash('Password is empty!')
            return render_template('login.html')
        else:
            return redirect(url_for('signin'))#just test

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signin',methods=['POST'])
def _signin():
    if request.method == "POST":
        email=request.form.get("signin_email")
        password=request.form.get('signin-pass')
        repeat_password=request.form.get('signin-repass')
        if email=='':
            flash('Email is empty!')
            return render_template('signin.html')
        elif password=='':
            flash('Password is empty!')
            return render_template('sigin.html')
        elif password==repeat_password:
            flash('Passwords you entered are different!')
            return render_template('signin.html')
        else:
            #flash('Passwords you entered are different!')
            return render_template('signin.html')#just test

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)