from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/authority')
def authority():
    return render_template('authority.html')        

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('login_email')
    password = request.form.get('login_pass')
    goto_signup=request.form.get('login_sign')
    goto_login=request.form.get('login_sub')
    # remember = True if request.form.get('remember') else False
    if goto_login=='LOG IN':
        user = User.query.filter_by(email=email).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            flash(f'Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

        login_user(user) #, remember=remember)
        return redirect(url_for('auth.authority'))
        
    elif goto_signup=='SIGN UP':
            return redirect(url_for('auth.signup'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    email=request.form.get("signup_email")
    password=request.form.get('signup_pass')
    repeat_password=request.form.get('signup_repass')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    if not password == repeat_password:
        flash('Passwords you entered are different!')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/authority',methods=['POST'])
def authority_post():
    if request.method=="POST":
        admin=request.form.get('authority_admin')
        guest=request.form.get('authority_guest')
        if admin=='Administrator':
            return admin
        elif guest=='Guest':
            return guest
        else:
            return render_template('authority.html')