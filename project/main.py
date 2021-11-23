from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)  

@main.route('/')
def loading():
    return render_template('loading.html')

@main.route('/',methods=['POST'])
def _loading():
    if request.method=="POST":
        return redirect(url_for('login'))

# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)