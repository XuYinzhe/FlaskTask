#All the objects in this project

class Device(object):
    def __init__(self,name,type,x,y):
        self.name = str(name)
        self.type = str(type)
        self.x = float(x)
        self.y = float(y) 