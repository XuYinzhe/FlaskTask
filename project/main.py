from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import db, insert_room
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
    return render_template('search.html',
                user_name=current_user.email, user_authority=current_user.authority)

@main.route('/search',methods=['POST'])
def search_post():
    if request.method=="POST":
        room=request.form.get('search_room')
        sub=request.form.get('search_sub')
        change_user=request.form.get('search_switch_user')
        change_role=request.form.get('search_switch_role')
        logout=request.form.get('search_logout')

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=current_user.email)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif sub=='':
            return insert_room(room)
        else:
            return render_template('search.html',
                user_name=current_user.email, user_authority=current_user.authority)

# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)


