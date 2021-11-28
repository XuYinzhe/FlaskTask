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
    user_name='aaabbbcccaaabbbcccaaabbb'
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

        user_name='Shaun@connect.use.hk'
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
    user_name='Shaun@connect.use.hk'
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

        user_name='Shaun@connect.use.hk'
        user_authority='Administrator'

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif sub=='':
            if room == '4223':
                return redirect(url_for('main.room_admin', room=room))
            else:
                return room
        elif btn == 'Create New Room':
            return btn
        else:
            return render_template('search.html',
                user_name=user_name, user_authority=user_authority)

@main.route('/room_admin/<room>')
def room_admin(room):
    user_name='Shaun@connect.use.hk'
    user_authority='Administrator'
    return render_template('room_admin.html', room=room, user_name=user_name, user_authority=user_authority)


@main.route('/room_admin/<room>',methods=['POST'])
def room_admin_post(room):
    if request.method=="POST":
        edit = request.form.get('room-edit-btn')
        room = request.form.get('search_room')
        sub=request.form.get('search_sub')
        change_user=request.form.get('search_switch_user')
        change_role=request.form.get('search_switch_role')
        logout=request.form.get('search_logout')
        home=request.form.get('search-home')

        user_name='Shaun@connect.use.hk'
        user_authority='Administrator'

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif home=='Home':
            return redirect(url_for('main.search_admin'))
        elif sub=='':
            if room == '4223':
                return redirect(url_for('main.room_admin', room=room))
            else:
                return room
        elif edit == 'Edit':
            return redirect(url_for('main.device_admin', room=room))
        else:
            return render_template('room_admin.html',
                user_name=user_name, user_authority=user_authority)


@main.route('/create_admin')
def create_admin():
    user_name='Shaun@connect.use.hk'
    user_authority='Administrator'
    return render_template('create_admin.html', user_name=user_name, user_authority=user_authority)

@main.route('/create_admin',methods=['POST'])
def create_admin_post():
    if request.method=="POST":
        conti = request.form.get('search-continue-btn')
        change_user=request.form.get('search_switch_user')
        change_role=request.form.get('search_switch_role')
        logout=request.form.get('search_logout')
        home=request.form.get('search-home')
        name=request.form.get('create-name-txtedit')
        addr=request.form.get('create-addr-txtedit')

        user_name='Shaun@connect.use.hk'
        user_authority='Administrator'

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif home=='Home':
            return redirect(url_for('main.search_admin'))
        elif conti == 'Continue' and name and addr:
                return redirect(url_for('main.device_admin',name=name,addr=addr,init="1"))             
        else:
            return render_template('create_admin.html',
                user_name=user_name, user_authority=user_authority)

from .objects import *

devices=devices_test
devices.chooseDevice()

@main.route('/device')
def device():
    room_name='Room 4223'
    room_locate='Academic Building, 4/F'
    user_name='Shaun@connect.use.hk'
    user_authority='User'
    return render_template('device.html',
        room_name=room_name,room_locate=room_locate,
        user_name=user_name,user_authority=user_authority,
        devices=devices.getJson(),img_size=devices.img,device_choose=devices.chooseDevice())


@main.route('/device', methods=['POST'])
def device_post():
    if request.method=="POST":
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        confirm=request.form.get('device_confirm')

        user_name='Shaun@connect.use.hk'
        user_authority='User'

        room_name='Room 4223'
        room_locate='Academic Building, 4/F'

        update_from_request(devices)

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif confirm=='Confirm':
            return devices.chooseDevice()
        else:
            return render_template('device.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority,
                devices=devices.getJson(),img_size=devices.img,device_choose=devices.chooseDevice(), img_path=url_for('static', filename='img/white.png'))


@main.route('/device_admin')
def device_admin():
    name = request.args.get('name')
    addr = request.args.get('addr')
    init = request.args.get('init')
    # if source is create room, device room is empty.
    user_name='Shaun@connect.use.hk'
    user_authority='User'
    if init:
        return render_template('device_admin.html',
                    room_name=name,room_locate=addr,
                    user_name=user_name,user_authority=user_authority,
                    devices='',img_size=devices.img,device_choose='',img_path=url_for('static',filename='img/white.png')) 
    # if source is room or search, device room remains
    else:
        room_name='Room 4223'
        room_locate='Academic Building, 4/F'
        return render_template('device_admin.html',
            room_name=room_name,room_locate=room_locate,
            user_name=user_name,user_authority=user_authority,
            devices=devices.getJson(),img_size=devices.img,device_choose=devices.chooseDevice(),img_path=url_for('static',filename='img/longimage.jpg'))


@main.route('/device_admin', methods=['POST'])
def device_post_admin():
    if request.method=="POST":
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        save=request.form.get('device_save')

        user_name='Shaun@connect.use.hk'
        user_authority='User'

        room_name='Room 4223'
        room_locate='Academic Building, 4/F'

        update_from_request(devices)

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif save=='Save':
            return save
        else:
            return render_template('device_admin.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority,
                devices=devices.getJson(),img_size=devices.img,device_choose=devices.chooseDevice())

personal_devices=personal_test

@main.route('/add')
def add():
    room_name='Room 4223'
    room_locate='Academic Building, 4/F'
    user_name='Shaun@connect.use.hk'
    user_authority='User'
    return render_template('add.html',
        room_name=room_name,room_locate=room_locate,
        user_name=user_name,user_authority=user_authority,
        devices=personal_devices.getJson())