from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, RoomList, room_cls, func_list
from . import db

ins = Blueprint('ins', __name__)
setup_instruction = {}

def setup_instruction_generation(room_id):
    # print("QAQ")
    cnt = 0
    room_name = table_name = "room_" + room_id
    room_content = type(room_name, (room_cls, ), {'__tablename__': table_name})
    devices = room_content.query.all()
    # device_list = (i for i in devices if i.ifon == '0') ###!!!!!

    for i in range(3): # ON,PROJECTION,CONNECTION
        for dev in devices:
            if dev.ifon == 0: ## shoule be 0
                continue
            dev_func_list = dev.func.split(',')
            # print(i)
            if dev_func_list[i] == '1':
                # print(dev.device)
                out = {}
                out[0] = str(i)
                out[1] = dev.device
                if i == 0: # ON
                    out[2] = ''
                    out[3] = ''
                    dev_oncontrol_list = dev.oncontrol.split(',')
                    dev_oncontrolby_list = dev.oncontrolby.split(',')
                    size = len(dev_oncontrol_list)
                    for t in range(size):
                        out[2] = out[2] + dev_oncontrol_list[t] + ','
                        out[3] = out[3] + dev_oncontrolby_list[t] + ','
                        # print(out)
                    setup_instruction[cnt] = ''
                    for k in range(4):
                        setup_instruction[cnt] = setup_instruction[cnt] + out[k] + '+'
                    cnt = cnt + 1
                elif i == 1: # PROJECTION
                    if dev.ifprojection == 1:
                        continue
                    # print(out[0])
                    dev_projectionto_list = dev.projectionto.split(',')
                    dev_projectionby_list = dev.projectionby.split(',')
                    # print(dev.ifprojection)
                    size = len(dev_projectionto_list)
                    out[2] = ''
                    out[3] = ''
                    for t in range(size):
                        pt = dev_projectionto_list[t]
                        pb = dev_projectionby_list[t]
                        todevice = room_content.query.filter_by(device=pt).first()
                        if todevice.ifon == 1: ## should be 1
                            dev.ifprojection = 1
                            # todevice.ifprojection = 1
                            out[2] = out[2] + pt + ','
                            out[3] = out[3] + pb + ','
                            db.session.commit()
                        else:
                            continue

                    if "null" in out[2]:
                        break

                    if "null" in out[3]:
                        break

                    setup_instruction[cnt] = ''
                    for k in range(4):
                        setup_instruction[cnt] = setup_instruction[cnt] + out[k] + '+'
                    cnt = cnt + 1
                    
                elif i == 2: # CONNECTION
                    if dev.ifconnection == 1:
                        continue
                    # print(out[0], dev.device)
                    dev_connectionto_list = dev.connectionto.split(',')
                    dev_connectionby_list = dev.connectionby.split(',')
                    size = len(dev_connectionto_list)
                    out[2] = ''
                    out[3] = ''
                    for t in range(size):
                        ct = dev_connectionto_list[t]
                        cb = dev_connectionby_list[t]
                        todevice = room_content.query.filter_by(device=ct).first()
                        if todevice.ifon == 1: ## should be 1 
                            dev.ifconnection = 1
                            # todevice.ifconnection = 1
                            out[2] = out[2] + ct + ','
                            out[3] = out[3] + cb + ','
                            db.session.commit()
                        else:
                            continue
                    if "null" in out[2]:
                        break

                    if "null" in out[3]:
                        break
                    setup_instruction[cnt] = ''
                    for k in range(4):
                        setup_instruction[cnt] = setup_instruction[cnt] + out[k] + '+'
                    cnt = cnt + 1
            else:
                continue

    # for i in range(cnt):
    #     print(setup_instruction[i].split('+'))

@ins.route('/instruction/<room_id>/<num>')
def instruction(room_id, num=1):
    room_name = "room_" + room_id
    room = RoomList.query.filter_by(room_name=room_name).first()
    room_locate = room.room_loc
    user_name = current_user.email
    user_authority = current_user.authority

    setup_instruction_generation(room_id)
    tmp = ''
    tmp = setup_instruction[int(num)-1].split('+')
    ins_len = len(setup_instruction) - 1
    ins_len=str(ins_len)
    print(ins_len)
    
    if (tmp[0] == '0'):
        ins1 = "To set up: "
        way = tmp[2].split(',')
        img = tmp[3].split(',')
        print(way[0], img[0])
        ins2 = "Please turn on {} using {}!".format(tmp[1], way[0])
        ins_img = url_for('static',filename='img/room_' + room_id + '/' + img[0])
    elif (tmp[0] == '1'):
        ins1 = "For Projection:"
        way = tmp[2].split(',')
        img = tmp[3].split(',')
        print(way[0], img[0])
        ins2 = "Please turn on {} using {}!".format(tmp[1], way[0])
        ins_img = url_for('static',filename='img/room_' + room_id + '/' + img[0])
    elif (tmp[0] == '2'):
        ins1 = "For Zoom Use"
        way = tmp[2].split(',')
        img = tmp[3].split(',')
        print(way[0], img[0])
        ins2 = "Please turn on {} using {}!".format(tmp[1], way[0])
        ins_img = url_for('static',filename='img/room_' + room_id + '/' + img[0])

    return render_template('instruction.html',
                room_name=room_id,room_locate=room_locate,
                user_name=user_name,user_authority=user_authority,ins_img=ins_img,ins1=ins1,ins2=ins2,num=num,ins_len=ins_len)

@ins.route('/instruction/<room_id>/<num>',methods=['POST'])
def instruction_post(room_id, num):
    if request.method=="POST":
        change_user=request.form.get('dropdown_switch_user')
        change_role=request.form.get('dropdown_switch_role')
        logout=request.form.get('dropdown_logout')
        ins_left=request.form.get('ins-left')
        ins_right=request.form.get('ins-right')

        room_name = "room_" + room_id
        room = RoomList.query.filter_by(room_name=room_name).first()
        room_locate = room.room_loc
        user_name = current_user.email
        user_authority = current_user.authority
        
        setup_instruction_generation(room_id)
        tmp = ''
        tmp = setup_instruction[int(num)-1].split('+')
        ins_len = len(setup_instruction) - 1
        ins_len=str(ins_len)
        
        if (tmp[0] == '0'):
            ins1 = "To set up: "
            way = tmp[2].split(',')
            img = tmp[3].split(',')
            print(way[0], img[0])
            ins2 = "Please turn on {} using {}!".format(tmp[1], way[0])
            ins_img = url_for('static',filename='img/room_' + room_id + '/' + img[0])
        elif (tmp[0] == '1'):
            ins1 = "For Projection:"
            way = tmp[2].split(',')
            img = tmp[3].split(',')
            print(way[0], img[0])
            ins2 = "Please turn on {} using {}!".format(tmp[1], way[0])
            ins_img = url_for('static',filename='img/room_' + room_id + '/' + img[0])
        elif (tmp[0] == '2'):
            ins1 = "For Zoom Use"
            way = tmp[2].split(',')
            img = tmp[3].split(',')
            print(way[0], img[0])
            ins2 = "Please turn on {} using {}!".format(tmp[1], way[0])
            ins_img = url_for('static',filename='img/room_' + room_id + '/' + img[0])

        if change_user=='Switch User':
            return redirect(url_for('auth.login'))
        elif change_role=='Switch Role':
            return render_template('authority.html',user_name=user_name)
        elif logout=='Log Out':
            return redirect(url_for('auth.login'))
        elif ins_left:
            return redirect(url_for('ins.instruction_post',room_id=room_id,num=int(num)-1))
        elif ins_right:
            return redirect(url_for('ins.instruction_post',room_id=room_id,num=int(num)+1))
        else:
            return render_template('instruction.html',
                    room_name=room_id,room_locate=room_locate,
                    user_name=user_name,user_authority=user_authority,ins_img=ins_img,ins1=ins1,ins2=ins2,num=num,ins_len=ins_len)
