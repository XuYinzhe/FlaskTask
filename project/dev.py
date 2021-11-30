from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, room_cls, RoomList
from . import check_room, db, insert_room

from .objects import *
from .objects_admin import *
import re

devices=devices_test
devices.chooseDevice()
devices_admin=devices_test_admin
devices_admin.chooseDevice()
devices_dict = {}

personal_devices=PersonalDevice()
personal_devices.addDevice('Shaun\'s Windowsaa','Windows')
personal_devices.addDevice('Shaun\'s Windowsaa','Windows')
personal_devices.addDevice('Shaun\'s iPhone','Apple')
personal_devices_dict={}

dev = Blueprint('dev', __name__)

@dev.route('/search')
def search():
    if current_user.authority == 'admin':
        return render_template('search_admin.html', user_name=current_user.email, user_authority=current_user.authority)
    elif current_user.authority == 'guest':
        return render_template('search.html', user_name=current_user.email, user_authority=current_user.authority)

@dev.route('/room/<room_id>')
def room(room_id):
    room_name = "room_" + room_id
    room = RoomList.query.filter_by(room_name=room_name).first()
    img_path = url_for('static', filename = 'img/' + room.room_img_prev)
    if current_user.authority == 'admin':
        return render_template('room_admin.html', 
                                room_id=room_id, 
                                user_name=current_user.email, 
                                user_authority=current_user.authority, 
                                room_name=room_id, 
                                address=room.room_loc, 
                                room_img=img_path,
                                nxt_btn="Edit")
    elif current_user.authority == 'guest':
        return render_template('room_admin.html', 
                                room_id=room_id, 
                                user_name=current_user.email, 
                                user_authority=current_user.authority, 
                                room_name=room_id, 
                                address=room.room_loc, 
                                room_img=img_path,
                                nxt_btn="Confirm")

@dev.route('/create_room')
def create_room():
    if current_user.authority == 'admin':
        return render_template('create_admin.html', user_name=current_user.email, user_authority=current_user.authority)
    elif current_user.authority == 'guest':
        flash("You are not an administrator for create room")
        return redirect(url_for('auth.authority')) 

@dev.route('/add/<room_id>')
def add(room_id):
    room_name = "room_" + room_id
    room = RoomList.query.filter_by(room_name=room_name).first()
    # img_path = url_for('static', filename = 'img/' + room.room_img_prev)
    room_locate = room.room_loc
    user_name = current_user.email
    user_authority = current_user.authority

    # room=re.findall(r"\d+",room_name)[0]
    if room_id not in personal_devices_dict.keys():
        personal_devices_dict[room_id]=PersonalDevice()

    return render_template('add.html',
        room_name=room_name,room_locate=room_locate,
        user_name=user_name,user_authority=user_authority,
        devices=personal_devices_dict[room_id].getJson())

@dev.route('/add_inter/<room_id>')
def add_inter(room_id):
    room_name = "room_" + room_id
    room = RoomList.query.filter_by(room_name=room_name).first()
    # img_path = url_for('static', filename = 'img/' + room.room_img_prev)
    room_locate = room.room_loc
    user_name = current_user.email
    user_authority = current_user.authority
    return render_template('add_inter.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority)

@dev.route('/deviceselection/<room_id>')
def device(room_id):
    room_name = "room_" + room_id
    room = RoomList.query.filter_by(room_name=room_name).first()
    return render_template('device.html',
        room_name=room_name,room_locate=room.room_loc,
        user_name=current_user.email,user_authority=current_user.authority,
        devices=devices.getJson(),img_size=devices.img,device_choose=devices.chooseDevice())

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
            return redirect(url_for('auth.authority'))
        elif logout == 'Log Out':
            return redirect(url_for('auth.logout'))
        elif create_btn == 'Create New Room':
            if check_room(room_id) == True:
                flash("Room exist! Search the room or use another name")
                return redirect(url_for('dev.search'))
            return redirect(url_for('dev.create_room', room_id=room_id))
        elif sub == '':
            if check_room(room_id) == False:
                flash("Room not exist! Please turn to an administrator to create")
                return redirect(url_for('dev.search'))
            return redirect(url_for('dev.room', room_id=room_id))
        else:
            if current_user.authority == 'admin':
                return render_template('search_admin.html', user_name=user_name, user_authority=user_authority)
            elif current_user.authority == 'guest':
                return render_template('search.html', user_name=user_name, user_authority=user_authority)

@dev.route('/room/<room_id>',methods=['POST'])
def room_post(room_id):
    if request.method=="POST":
        edit = request.form.get('room-edit-btn')
        room_id = request.form.get('search_room')
        sub=request.form.get('search_sub')
        change_user=request.form.get('search_switch_user')
        change_role=request.form.get('search_switch_role')
        logout=request.form.get('search_logout')
        home=request.form.get('search-home')

        user_name=current_user.email
        user_authority=current_user.authority

        room_name = "room_" + room_id
        room = RoomList.query.filter_by(room_name=room_name).first()
        address = room.room_loc

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return redirect(url_for('auth.authority'))
        elif logout=='Log Out':
            return redirect(url_for('auth.logup'))
        elif home=='Home':
            return redirect(url_for('dev.search'))
        elif sub=='':
            return redirect(url_for('dev.room', room=room))
        elif edit == 'Edit':
            return redirect(url_for('dev.manage_device',name=room_id,addr=address,init="n"))
        elif edit == 'Confirm':
            return redirect(url_for('dev.add', room_id=room_id))
        else:
            return render_template('room_admin.html',
                user_name=user_name, user_authority=user_authority, nxt_btn=edit) 

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
        return redirect(url_for('auth.authority'))
    elif logout=='Log Out':
        return redirect(url_for('auth.logout'))
    elif home=='Home':
        return redirect(url_for('dev.search'))
    elif conti == 'Continue' and name and addr:
        if check_room(name) == True:
            flash("Room exist! Search the room or ")
            return redirect(url_for('dev.create_room'))
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
    img_addr = request.form.get('file-uploader')

    user_name=current_user.email
    user_authority=current_user.authority
    k = name[-4:] if len(name) >= 4 else name

    room_name = "room_" + name
    room = RoomList.query.filter_by(room_name=room_name).first()

    if not room.room_img_long and img_addr:
        room.room_img_long = img_addr
        db.session.commit()            

    if init == 'p' or not room.room_img_long:
        img_path = url_for('static', filename = 'img/white.png')
    
    if room.room_img_long:
        img_path = url_for('static', filename = 'img/' + room.room_img_long)
 
    if k not in devices_dict.keys():
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
        elif logout == 'Log Out':
            return redirect(url_for('auth.logout'))
        elif save == 'Save':
            return redirect(url_for('dev.search'))

    return render_template('device_admin.html',
        name=name,addr=addr,
        user_name=user_name,user_authority=user_authority,
        devices=devices_dict[k].getJson(),img_size=devices_dict[k].img,device_choose=devices_dict[k].chooseDevice(),img_path=img_path)

@dev.route('/add/<room_id>',methods=['POST'])
def add_post(room_id):
    if request.method=="POST":
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        continu=request.form.get('add_continue')
        add=request.form.get('add_plus')

        room_name = "room_" + room_id
        room = RoomList.query.filter_by(room_name=room_name).first()
        # img_path = url_for('static', filename = 'img/' + room.room_img_prev)
        room_locate = room.room_loc
        user_name = current_user.email
        user_authority = current_user.authority

        # room=re.findall(r"\d+",room_name)[0]
        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return redirect(url_for('auth.authority'))
        elif logout=='Log Out':
            return redirect(url_for('auth.logup'))
        elif continu=='Continue':
            # return personal_devices_dict[room].getJson()
            return redirect(url_for('ins.instruction', room_id=room_id, num=1))
        elif add=='':
            return redirect(url_for('dev.add_inter', room_id=room_id))
        else:
            return render_template('add.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority,
                devices=personal_devices_dict[room_id].getJson())

@dev.route('/add_inter/<room_id>',methods=['POST'])
def add_inter_post(room_id):
    if request.method=="POST":
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        continu=request.form.get('inter_continue')
        radio=request.form.get('inter_device')
        name=request.form.get('inter_name')

        room_name = "room_" + room_id
        room = RoomList.query.filter_by(room_name=room_name).first()
        # img_path = url_for('static', filename = 'img/' + room.room_img_prev)
        room_locate = room.room_loc
        user_name = current_user.email
        user_authority = current_user.authority

        # room=re.findall(r"\d+",room_name)[0]
        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return redirect(url_for('auth.authority'))
        elif logout=='Log Out':
            return redirect(url_for('auth.logup'))
        elif continu=='Confirm':
            personal_devices_dict[room_id].addDevice(name,radio)
            return redirect(url_for('dev.add', room_id=room_id))
            
        else:
            return render_template('add_inter.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority,
                devices=personal_devices_dict[room_id].getJson())

# @dev.route('/deviceselection/<room_id>', methods=['POST'])
# def device_post(room_id):
#     if request.method=="POST":
#         change_user=request.form.get('dropdown_switch_user')
#         change_role=request.form.get('dropdown_switch_role')
#         logout=request.form.get('dropdown_logout')
#         confirm=request.form.get('device_confirm')

#         user_name='Shaun@connect.use.hk'
#         user_authority='User'

#         room_name='Room 4223'
#         room_locate='Academic Building, 4/F'

#         update_from_request(devices)

#         if change_user=='Switch User':
#             return redirect(url_for('auth.login'))
#         elif change_role=='Switch Role':
#             return render_template('authority.html',user_name=user_name)
#         elif logout=='Log Out':
#             return redirect(url_for('auth.login'))
#         elif confirm=='Confirm':
#             return devices.chooseDevice()
#         else:
#             return render_template('device.html',
#                 room_name=room_name,room_locate=room_locate,
#                 user_name=user_name,user_authority=user_authority,
#                 devices=devices.getJson(),img_size=devices.img,device_choose=devices.chooseDevice(), img_path=url_for('static', filename='img/white.png'))
