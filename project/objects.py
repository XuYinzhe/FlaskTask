#All the objects in this project
from typing import List
import numpy as np
from flask import request

class Device(object):
    #One device
    def __init__(self,name:str,type:str,x:float,y:float,width:int,height:int):
            self.name = name #name of this device
            self.type = type #type of this device
            self.x = x*width #Distance to the left boundary of this device (px)
            self.y = y*height #Distance to the top boundary of this device (px)
            self.img=[width,height] #The size of the image that the device belong to


class Devices(object):
    #All the devices in one room (used in device.html page)
    def __init__(self, width:int=None, height:int=None, img:List[int]=None):
        #Require to give 'width' and 'height' at the same time or only give 'img'
        self.devices=[] #All the devices in the class type Device
        self.devices_list=[] #All the deivces directly save in list
        self.__json=None #JSON of all devices
        self.__jsondone=False #Whether the json is filled
        self.img=[] #The size of the image that all the devices belong to
        self.device_choose=None #Which devices are chose, which are not
        self.__choose_ini=False #Whether the choose list is filled
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

    def addDevice(self,name:str=None,type:str=None,x:float=None,y:float=None,device:Device=None):
        #Add another device to this room: give all the deivce attributes or only give a initialized Deive class
        if not device:
            if name and type and x and y:
                self.devices.append(Device(name,type,x,y,self.img[0],self.img[1]))
                self.devices_list.append([name,type,x*self.img[0],y*self.img[1]])
            else:
                raise ValueError('Device attributes must be set!')
        else:
            self.devices.append(device)
            self.devices_list.append(device.name,device.type,device.x,device.y)

    def deleteDevice_name(self,name):
        index=-1
        for i in range(len(self.devices)):
            if self.devices[i].name==name:
                index=i
        del self.devices[index]

    def getJson(self):
        #Get the JSON file in string type
        #self.__json={0:{'name':...,'type':...,'x':...,'y':...},1:{'name':...,'type':...,'x':...,'y':...},...}
        if not self.__jsondone:
            self.__json={}
            i=0
            for device in self.devices:
                self.__json[i]={'name':device.name,'type':device.type,
                                'x':device.x,'y':device.y}
                i+=1
            self.__jsondone=True
            return self.__json
        else:
            return self.__json

    def emptyJson(self):
        #Clear current JSON file
        self.__json=''
        self.__jsondone=False

    def chooseDevice(self,name=None):
        #Initial, choose or not choose one device in a room
        #self.device_choose={0:{'name':...,'choose':0 or 1},0:{'name':...,'choose':0 or 1},...}
        if not self.__choose_ini:
            self.device_choose={}
            i=0
            for d in self.devices:
                self.device_choose[i]={'name':d.name,'choose':0}
                if name==d.name:
                    self.device_choose[i]['choose']=1-self.device_choose[i]['choose']
                i+=1  
            self.__choose_ini=True
        elif name:
            i=0
            for d in self.devices:
                if name==d.name:
                    self.device_choose[i]['choose']=1-self.device_choose[i]['choose']
                i+=1

        return self.device_choose

    def chooseDevice_clear(self):
        self.device_choose=None
        self.__choose_ini=True

    '''
    def computeDevicesPosition(self):
        _w=[1,1,0,0,0.05,0.09,0.117,0.13,0.155,0.17,0.155,0.13,0.117,0.09,0.05,0,0]
        _h=[0,1,1,0.75,0.74,0.72,0.6925,0.665,0.61,0.5,0.39,0.335,0.3075,0.28,0.26,0.255,0]
        w=self.img[0]*np.array(_w)
        h=self.img[1]*np.array(_h)
    '''

def update_from_request(devices:Devices):
    i=0
    for d in devices.devices:
        cur_d=request.form.get('devices_input_'+d.name)
        if cur_d==' ':
            devices.chooseDevice(d.name)
        i+=1

class PersonalDevice(object):
    #All personal devices in a room (used in add.html page)
    def __init__(self):
        self.device=[] #List of deivces: [[name1,type1],[name2,type2],...]
        self.__json=None #Json of all devices: {0:{'name':...,'type':...}, 1:{'name':...,'type':...},...}
    
    def addDevice(self,name,type):
        #Add new personal device, only name and type
        self.device.append([name,type])

    def deleteDevice(self,name):
        #Delete a deivce with a specific name
        i=0
        index=-1
        for d in self.device:
            if d[0]==name:
                index=i
            i+=1
        if not index==-1:
            del self.device[index]
    
    def getJson(self):
        #Change the list of deivces into json
        self.__json={}
        i=0
        for d in self.device:
            self.__json[i]={'name':d[0],'type':d[1]}
            i+=1
        return self.__json



devices_test=Devices(img=[3240,720])
devices_test.addDevice('Projecter','a',0.2,0.2)
devices_test.addDevice('Screen','b',0.8,0.1)
devices_test.addDevice('Speaker','c',0.3,0.7)

personal_test=PersonalDevice()
personal_test.addDevice('Shaun\'s Windows','Windows')
personal_test.addDevice('Shaun\'s iPhone','Apple')