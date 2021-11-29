from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, room_cls, RoomList
from . import check_room, db, insert_room

from .objects import *
from .objects_admin import *

devices=devices_test
devices.chooseDevice()
devices_admin=devices_test_admin
devices_admin.chooseDevice()
devices_dict = {}

dev = Blueprint('dev', __name__)

@dev.route('/search')
def search():
    if current_user.authority == 'admin':
        return render_template('search_admin.html', user_name=current_user.email, user_authority=current_user.authority)
    elif current_user.authority == 'guest':
        return render_template('search.html', user_name=current_user.email, user_authority=current_user.authority)

@dev.route('/room/<room_id>')
def room(room_id):
    if current_user.authority == 'admin':
        room_name = table_name = "room_" + room_id
        room = RoomList.query.filter_by(room_name=room_name).first()
        return render_template('room_admin.html', 
                                room_id=room_id, 
                                user_name=current_user.email, 
                                user_authority=current_user.authority, 
                                room_name=room_id, 
                                address=room.room_loc, 
                                room_img=room.room_img)
    elif current_user.authority == 'guest':
        return render_template('search.html', user_name=current_user.email, user_authority=current_user.authority)

@dev.route('/create_room')
def create_room():
    if current_user.authority == 'admin':
        return render_template('create_admin.html', user_name=current_user.email, user_authority=current_user.authority)
    elif current_user.authority == 'guest':
        return redirect(url_for('auth.authority'))

@dev.route('/search',methods=['POST'])
def search_post():
    if request.method == "POST":
        room_id = request.form.get('search_room')
        sub = request.form.get('search_sub')
        change_user = request.form.get('search_switch_user')
        change_role = request.form.get('search_switch_role')
        logout = request.form.get('search_logout')

        user_name = current_user.email
        user_authority = current_user.authority

        if user_authority == 'admin':
            create_btn = request.form.get('create-btn')
        else:
            create_btn = ''

        if change_user == 'Switch User':
            return redirect(url_for('auth.login'))
        elif change_role == 'Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout == 'Log Out':
            return redirect(url_for('auth.logout'))
        elif create_btn == 'Create New Room':
            # print(room_id)
            if room_id == '':
                flash('Please input room name first!')
                return redirect(url_for('dev.search'))
            return redirect(url_for('dev.create_room', room_id=room_id))
        elif sub == '':
            return redirect(url_for('dev.room', room_id=room_id))
            # check = search_room(room)
            # if check == True:
            #     return
            # else: 
            #     flash('Please turn to an administrator to create this room!')
            #     if current_user.authority == 'admin':
            #         return render_template('search_admin.html', user_name=current_user.email, user_authority=current_user.authority)
            #     elif current_user.authority == 'guest':
            #         return render_template('search.html', user_name=current_user.email, user_authority=current_user.authority)
        else:
            if current_user.authority == 'admin':
                return render_template('search_admin.html', user_name=user_name, user_authority=user_authority)
            elif current_user.authority == 'guest':
                return render_template('search.html', user_name=user_name, user_authority=user_authority)

@dev.route('/room/<room_id>',methods=['POST'])
def room_post():
    return 

@dev.route('/create_room', methods=['POST'])
def create_room_post():
    conti = request.form.get('search-continue-btn')
    change_user = request.form.get('search_switch_user')
    change_role = request.form.get('search_switch_role')
    logout = request.form.get('search_logout')
    home = request.form.get('search-home')
    name = request.form.get('create-name-txtedit')
    addr = request.form.get('create-addr-txtedit')
    img_prev = request.form.get('file-uploader')

    user_name=current_user.email
    user_authority = current_user.authority

    if change_user=='Switch User':
        return redirect(url_for('auth.login'))
    elif change_role=='Switch Role':
        return render_template('authority.html',user_name=user_name)
    elif logout=='Log Out':
        return redirect(url_for('auth.logout'))
    elif home=='Home':
        return redirect(url_for('dev.search'))
    elif conti == 'Continue' and name and addr:
        insert_room(name, img_prev, addr)
        return redirect(url_for('dev.manage_device',name=name,addr=addr,img_addr=img_prev,init='p'))             
    else:
        return render_template('create_admin.html',
            user_name=user_name, user_authority=user_authority)

@dev.route('/manage_device', methods=['GET', 'POST'])
def manage_device(name="", addr="", img_addr="", init=""):

    name=request.args.get('name')
    addr=request.args.get('addr')
    img_addr=request.args.get('img_addr')
    init=request.args.get('init')

    img_path=url_for('static',filename='img/white.png')

        # room_name = "room_" + name
        # room = RoomList.query.filter_by(room_name=room_name).first()
        # room.room_loc = addr
        # room.room_img_prev = img_prev
        # db.session.commit() 
    
    # init: 0. if source is create room, device room is empty. Else init: 1 for edit button
    # if not name or not addr or not init:
    #     name='Room 4223'
    #     addr='Academic Building, 4/F'
    user_name=current_user.email
    user_authority=current_user.authority
    k = name[-4:] if len(name) >= 4 else name
    

    # if init == 'p':  # Create
    #     img_path=url_for('static',filename='img/white.png')
    #     img_long = request.form.get('file-uploader')
    # else:  # Edit
    #     img_path=url_for('static',filename='img/' + img_addr)
 
    if k not in devices_dict.keys():
        if k == '4223':  # Three point initalization
            global devices_test_admin
            devices_dict[k] = devices_test_admin
        else:  # Zero point initalization
            devices_admin = Devices_admin(img=[3240,720], room=k)
            devices_dict[k] = devices_admin

    
    if request.method=="POST":
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        save=request.form.get('device_save')
 
        update_from_admin_request(devices_dict[k])

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.logout'))
        elif save=='Save':
            return redirect(url_for('dev.search'))

    return render_template('device_admin.html',
        name=name,addr=addr,
        user_name=user_name,user_authority=user_authority,
        devices=devices_dict[k].getJson(),img_size=devices_dict[k].img,device_choose=devices_dict[k].chooseDevice(),img_path=img_path)


