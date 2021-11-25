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
        change_user=request.form.get('search_switch_user')
        change_role=request.form.get('search_switch_role')
        logout=request.form.get('search_logout')

        user_name='Shaun'
        user_authority='User'

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif sub=='':
            return room
        else:
            return render_template('search.html',
                user_name=user_name, user_authority=user_authority)

@main.route('/search_admin')
def search_admin():
    user_name='Shaun'
    user_authority='Administrator'
    return render_template('search_admin.html',
        user_name=user_name, user_authority=user_authority)

@main.route('/search_admin',methods=['POST'])
def search_admin_post():
    if request.method=="POST":
        btn = request.form.get('create-btn')
        room = request.form.get('search_room')
        sub=request.form.get('search_sub')
        change_user=request.form.get('search_switch_user')
        change_role=request.form.get('search_switch_role')
        logout=request.form.get('search_logout')

        user_name='Shaun'
        user_authority='Administrator'

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif sub=='':
            return room
        elif btn == 'Create New Room':
            return btn
        else:
            return render_template('search.html',
                user_name=user_name, user_authority=user_authority)

# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)


