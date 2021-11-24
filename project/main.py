from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import db
import os

main = Blueprint('main', __name__)  

@main.route('/')
def loading():
    return render_template('loading.html')

@main.route('/',methods=['POST'])
def loading_post():
    if request.method=="POST":
        return redirect(url_for('auth.login'))

@main.route('/search')
def search():
    user_name='Shaun'
    user_authority='User'
    return render_template('search.html',
                user_name=user_name, user_authority=user_authority)

@main.route('/search',methods=['POST'])
def search_post():
    if request.method=="POST":
        room=request.form.get('search_room')
        sub=request.form.get('search_sub')

        user_name='Shaun'
        user_authority='User'

        if sub=='':
            return room
        else:
            return render_template('search.html',
                user_name=user_name, user_authority=user_authority)

# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)


