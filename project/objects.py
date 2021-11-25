#All the objects in this project
from typing import List

class Device(object):
    #One device
    def __init__(self,name:str,type:str,x:float,y:float,width:int,height:int):
            self.name = name #name of this device
            self.type = type #type of this device
            self.x = x*width #Distance to the left boundary of this device (px)
            self.y = y*height #Distance to the top boundary of this device (px)
            self.img=[width,height] #The size of the image that the device belong to


class Devices(object):
    #All the __devices in one room
    def __init__(self, width:int=None, height:int=None, img:List[int]=None):
        #Require to give 'width' and 'height' at the same time or only give 'img'
        self.__devices=[] #All the __devices in the class type Device
        self.__json='' #JSON of all __devices
        self.__jsondone=False #Whether the json is filled
        self.img=[] #The size of the image that all the __devices belong to
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

    def numDevice(self):
        return len(self.__devices)

    def clearDevice(self):
        self.__devices=[]

    def addDevice(self,name:str=None,type:str=None,x:float=None,y:float=None,device:Device=None):
        #Add another device to this room: give all the deivce attributes or only give a initialized Deive class
        if not device:
            if name and type and x and y:
                self.__devices.append(Device(name,type,x,y,self.img[0],self.img[1]))
            else:
                raise ValueError('Device attributes must be set!')
        else:
            self.__devices.append(device)

    def deleteDevice_name(self,name):
        index=-1
        for i in range(len(self.__devices)):
            if self.__devices[i].name==name:
                index=i
        del self.__devices[i]

    def getJson(self):
        #Get the JSON file in string type
        if not self.__jsondone:
            self.__json='{ "__devices" : ['
            for device in self.__devices:
                self.__json+='{ "name":"'+device.name+'" , "type":"'+\
                    device.type+'" , "x":"'+str(device.x)+'px" , "y":"'+str(device.y)+'px" },'
            self.__json+=']}'
            self.__jsondone=True
            return self.__json
        else:
            return self.__json

    def emptyJson(self):
        #Clear current JSON file
        self.__json=''
        self.__jsondone=False



devices_test=Devices(img=[2880,720])
devices_test.addDevice('a','a',0.2,0.2)
devices_test.addDevice('b','b',0.8,0.1)
devices_test.addDevice('c','c',0.3,0.7)