from pandac.PandaModules import *
from math import *
class CameraHandler():
    def __init__(self):
        self.cameradegrees = 270
    def motion(self):
        x = base.camera.getX()
        y = base.camera.getY()
        self.cameradegrees += .5
        base.camera.setPos(40*cos(radians(self.cameradegrees)), 40*sin(radians(self.cameradegrees)),20)
        table = render.find("**\table")
        base.camera.lookAt(0,0,4)
