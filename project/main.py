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
            return redirect(url_for('main.create_admin', room=room))
        else:
            return render_template('search.html',
                user_name=user_name, user_authority=user_authority)

@main.route('/room_admin/<room>')
def room_admin(room):
    user_name='Shaun@connect.use.hk'
    user_authority='Administrator'
    room_name='Room 4223'
    address='Academic Building, 4/F'
    room_img=url_for('static',filename='img/classroom.jpg')
    return render_template('room_admin.html', room=room, user_name=user_name, user_authority=user_authority,room_name=room_name,address=address,room_img=room_img)


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

        room_name='Room 4223'
        address='Academic Building, 4/F'

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
            return redirect(url_for('main.device_admin',name=room_name,addr=address,init="n"))
        else:
            return render_template('room_admin.html',
                user_name=user_name, user_authority=user_authority)

room_select_set={}#save all device setting of all room

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

        #room_select_set[len(room_select_set)]={'room_name':re.findall(r"\d+",name)[0],'room_addr':addr}

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
            return redirect(url_for('main.device_admin',name=name,addr=addr,init="y"))             
        else:
            return render_template('create_admin.html',
                user_name=user_name, user_authority=user_authority)

from .objects import *
from .objects_admin import *
import re

#devices=devices_test
#devices.chooseDevice()
devices_admin=devices_test_admin
devices_admin.chooseDevice()
devices_dict = {}
personal_devices_dict={}


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

        room=re.findall(r"\d+",room_name)[0]
        devices=devices_dict[room]
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



@main.route('/device_admin', methods=['GET', 'POST'])
def device_admin(name="", addr="", init=""):
    name=request.args.get('name')
    addr=request.args.get('addr')
    init=request.args.get('init')
    
    # init: 0. if source is create room, device room is empty. Else init: 1 for edit button
    if not name or not addr or not init:
        name='Room 4223'
        addr='Academic Building, 4/F'
    user_name='Shaun@connect.use.hk'
    user_authority='User'
    k = name[-4:] if len(name) >= 4 else name
    

    if init == 'y':  # Create
        img_path=url_for('static',filename='img/white.png')
    else:  # Edit
        img_path=url_for('static',filename='img/longimage.jpg')
 
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
            return redirect(url_for('auth.login'))
        elif save=='Save':
            return redirect(url_for('main.search_admin'))

    return render_template('device_admin.html',
        name=name,addr=addr,
        user_name=user_name,user_authority=user_authority,
        devices=devices_dict[k].getJson(),img_size=devices_dict[k].img,device_choose=devices_dict[k].chooseDevice(),img_path=img_path)


#personal_devices=personal_test
personal_devices=PersonalDevice()
personal_devices.addDevice('Shaun\'s Windowsaa','Windows')
personal_devices.addDevice('Shaun\'s Windowsaa','Windows')
personal_devices.addDevice('Shaun\'s iPhone','Apple')

@main.route('/add')
def add():
    room_name='Room 4223'
    room_locate='Academic Building, 4/F'
    user_name='Shaun@connect.use.hk'
    user_authority='User'

    room=re.findall(r"\d+",room_name)[0]
    if room not in personal_devices_dict.keys():
        personal_devices_dict[room]=PersonalDevice()

    return render_template('add.html',
        room_name=room_name,room_locate=room_locate,
        user_name=user_name,user_authority=user_authority,
        devices=personal_devices_dict[room].getJson())

@main.route('/add',methods=['POST'])
def add_post():
    if request.method=="POST":
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        continu=request.form.get('add_continue')
        add=request.form.get('add_plus')

        room_name='Room 4223'
        room_locate='Academic Building, 4/F'
        user_name='Shaun@connect.use.hk'
        user_authority='User'

        room=re.findall(r"\d+",room_name)[0]
        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif continu=='Continue':
            return personal_devices_dict[room].getJson()
        elif add=='':
            return redirect(url_for('main.add_inter'))
        else:
            return render_template('add.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority,
                devices=personal_devices_dict[room].getJson())

@main.route('/add_inter')
def add_inter():
    room_name='Room 4223'
    room_locate='Academic Building, 4/F'
    user_name='Shaun@connect.use.hk'
    user_authority='User'
    return render_template('add_inter.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority)

@main.route('/add_inter',methods=['POST'])
def add_inter_post():
    if request.method=="POST":
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        continu=request.form.get('inter_continue')
        radio=request.form.get('inter_device')
        name=request.form.get('inter_name')

        room_name='Room 4223'
        room_locate='Academic Building, 4/F'
        user_name='Shaun@connect.use.hk'
        user_authority='User'

        room=re.findall(r"\d+",room_name)[0]
        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif continu=='Confirm':
            personal_devices_dict[room].addDevice(name,radio)
            return redirect(url_for('main.add'))
            
        else:
            return render_template('add_inter.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority,
                devices=personal_devices_dict[room].getJson())


@main.route('/instruction/<num>')
def instruction(num=1):
    room_name='Room 4223'
    room_locate='Academic Building, 4/F'
    user_name='Shaun@connect.use.hk'
    user_authority='User'
    ins_img=url_for('static',filename='img/classroom.jpg')
    ins1=num
    ins2=num

    return render_template('instruction.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority,ins_img=ins_img,ins1=ins1,ins2=ins2,num=num)

@main.route('/instruction/<num>',methods=['POST'])
def instruction_post(num):
    if request.method=="POST":
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        ins_left=request.form.get('ins-left')
        ins_right=request.form.get('ins-right')

        room_name='Room 4223'
        room_locate='Academic Building, 4/F'
        user_name='Shaun@connect.use.hk'
        user_authority='User'
        ins_img=url_for('static',filename='img/classroom.jpg')
        ins1=num
        ins2=num

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif ins_left:
            return redirect(url_for('main.instruction_post',num=int(num)-1))
        elif ins_right:
            return redirect(url_for('main.instruction_post',num=int(num)+1))
        else:
            return render_template('instruction.html',
                room_name=room_name,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority,
                ins_img=ins_img,ins1=ins1,ins2=ins2,num=num)
'''
room_select_set={
    0:{
        'room_name':...,
        'room_addr':...,
        'select':{
            0:{
                'device_name':...,
                'controller':{
                    0:{

                    },
                    1:{...}
                }
            },
            1:{...},
        }
    },
    1:{...},
}
'''
room_select_set[0]={'room_name':'room1','room_addr':'addr1'}
room_select_set[0]['select']={'device_name':'device1','controller':{}}

select_dict={
    'devices':[
        'Projector 1',
        'Projector 2',
        'Projection Screen 1',
        'Projection Screen 2',
        'Microphone 1',
        'Microphone 2',
        'Speaker',
        'Camera'
    ],
    'attributes':[
        'Controller',
        'ControlBy',
        'Function',
        'LinkTo',
        'LinkBy',
        'IfLink'
    ]
}

@main.route('/select')
def select():
    room_name='Room 4223'
    room_locate='Academic Building, 4/F'
    user_name='Shaun@connect.use.hk'
    user_authority='User'
    return render_template('select.html',
        room_name=room_name,room_locate=room_locate,
        user_name=user_name,user_authority=user_authority,dict=select_dict)

read_input=[]
@main.route('/select',methods=['POST'])
def select_post():
    if request.method=='POST':
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        sub=request.form.get('select_confirm')

        room_name='Room 4223'
        room_locate='Academic Building, 4/F'
        user_name='Shaun@connect.use.hk'
        user_authority='User'

        if sub=='Confirm':
            for d in select_dict['devices']:
                read_input_row=[]
                for i in range(len(select_dict['attributes'])):
                    read_input_row.append(request.form.get('cell'+str(i)+'_'+d))
                    #print('cell'+str(i)+'_'+d)
                    #print(select_dict['attributes'])
                read_input.append(read_input_row)
        print(read_input)
                

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        else:
            return render_template('select.html',
            room_name=room_name,room_locate=room_locate,
            user_name=user_name,user_authority=user_authority,dict=select_dict)
        
#@main.route('/select')