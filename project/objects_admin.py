#All the objects in this project
from collections import defaultdict
from typing import List
import numpy as np
from flask import request

class Device_admin(object):
    #One device
    def __init__(self,name:str,type:str,x:float,y:float,width:int,height:int,room:str):
            self.name = name #name of this device
            self.type = type #type of this device
            self.x = x*width #Distance to the left boundary of this device (px)
            self.y = y*height #Distance to the top boundary of this device (px)
            self.img=[width,height] #The size of the image that the device belong to
            self.room=room  # the device belong to which class


class Devices_admin(object):
    #All the devices in one room
    def __init__(self, width:int=None, height:int=None, img:List[int]=None, room:str='4223'):
        #Require to give 'width' and 'height' at the same time or only give 'img'
        self.devices=[] #All the devices in the class type Device_admin
        self.devices_list=[]
        # self.__json=None #JSON of all devices
        self.img=[] #The size of the image that all the devices belong to
        self.device_choose=[] #Which devices are chose, which are not
        self.__choose_ini=False
        self.room=room
        if not img:
            if width and height:
                self.img=[width,height]
            else:
                raise ValueError('Image size must be set!')
        else:
            if len(img)!=2:
                raise ValueError('Image size must be set!')
            else:
                self.img=img

    def addDevice(self,name:str=None,type:str=None,x:float=None,y:float=None,device:Device_admin=None,room=None):
        #Add another device to this room: give all the deivce attributes or only give a initialized Deive class
        if not device:
            if name and type and x and y and room:
                name_set = set([d.name for d in self.devices])
                while name in name_set:
                    name += '_'
                self.devices.append(Device_admin(name,type,x,y,self.img[0],self.img[1],room))
                self.devices_list.append([name,type,x*self.img[0],y*self.img[1],room])
                self.device_choose.append([name, 0])
            else:
                raise ValueError('Device_admin attributes must be set!')
        else:
            self.devices.append(device)
            self.devices_list.append([device.name,device.type,device.x,device.y])
    
    def deleteDevice(self, name):
        for d in self.devices:
            if d.name==name:  # name is unique because of chooseDevice(self,name=None)
                self.devices.remove(d)
                break
        for d in self.devices_list:
            if d[0]==name:  
                self.devices_list.remove(d)
                break
        for d in self.device_choose:
            if d[0]==name:  
                self.device_choose.remove(d)
                break

    def getJson(self):
        #Get the JSON file in string type
        #self.__json={0:{'name':...,'type':...,'x':...,'y':...},1:{'name':...,'type':...,'x':...,'y':...},...}
        # if not self.__jsondone:
            self.__json={}
            i=0
            for device in self.devices:
                self.__json[i]={'name':device.name,'type':device.type,
                                'x':device.x,'y':device.y, 'room':device.room}
                i+=1
            # self.__jsondone=True
            return self.__json
        # else:
        #     return self.__json

    def emptyJson(self):
        #Clear current JSON file
        self.__json=''
        # self.__jsondone=False

    def chooseDevice(self, name=None):
        #Initial, choose or not choose one device in a room
        #self.device_choose={0:{'name':...,'choose':0 or 1},0:{'name':...,'choose':0 or 1},...}
        #self.device_choose={0:{'name':...,'choose':...,'now':0or1},0:{'name':...,'choose':...,'now':0or1},...}
        if not self.__choose_ini:
            self.device_choose=[]
            i=0
            for d in self.devices:
                self.device_choose.append([d.name, 0])  # 'now' record which device hits 
                if name==d.name:
                    self.device_choose[i][1]=1-self.device_choose[i][1]
                i+=1  
            self.__choose_ini=True
        elif name:
            i=0
            for d in self.devices:
                if name==d.name:
                    self.device_choose[i][1]=1-self.device_choose[i][1]
                else:
                    self.device_choose[i][1]=0
                i+=1

        return self.device_choose

    def chooseDevice_clear(self):
        self.device_choose=None
        self.__choose_ini=True


def update_from_admin_request(devices:Devices_admin):
    close_idx=request.form.get('point_close')
    point_name=request.form.get('point_name')
    point_delete=request.form.get('point_delete')
    point_edit=request.form.get('point_edit')
    dup_x=request.form.get('dup_x')
    dup_y=request.form.get('dup_y')
    p_name=request.form.get('p_name')
    p_type=request.form.get('p_type')
    uid=request.form.get('uid')

    # Edit the divice
    if point_edit and p_name and p_type:
        i=0
        for d in devices.devices:
            if i==int(uid):
                d.name=p_name
                d.type=p_type
                break
            i+=1

    # Delete the device
    print(1)
    print(p_name, devices.devices_list, point_delete, point_edit)
    print(1)
    if p_name and point_delete:
        devices.deleteDevice(p_name)
    
    # Duplicate the device
    print(2)
    print(point_name, p_name, dup_x, dup_y)
    print(devices.devices_list)
    print(devices.device_choose)
    print(2)
    if dup_x and dup_y:
        hit = False
        for d in devices.devices:
            if d.name==point_name:
                devices.addDevice(d.name, d.type, float(dup_x)/devices.img[0], float(dup_y)/devices.img[1],room='4223')
                hit = True
        if not hit:  # point_name="", but p_name=microphone 1
            devices.addDevice('name', 'type', float(dup_x)/devices.img[0], float(dup_y)/devices.img[1],room='4223')
    print(3)
    print(point_name,p_name, dup_x, dup_y)
    print(devices.devices_list)
    print(devices.device_choose)
    print(3)

    # Choose the devices
    i=0
    for d in devices.devices:
        cur_d=request.form.get('devices_input_'+d.name)
        if cur_d==' ':
            devices.chooseDevice(d.name)  # 
        i+=1
    
    print(4)
    print(devices.devices_list)
    print(devices.device_choose)
    print(4)
    
    # Close the open device window
    if close_idx:
        i=0
        for d in devices.devices:
            devices.device_choose[i][1] = 0
            i+=1

devices_test_admin=Devices_admin(img=[3240,720], room='4223')
devices_test_admin.addDevice('Projecter','a',0.2,0.2,room='4223')
devices_test_admin.addDevice('Screen','b',0.8,0.1,room='4223')
devices_test_admin.addDevice('Speaker','c',0.3,0.7,room='4223')
is_used = False