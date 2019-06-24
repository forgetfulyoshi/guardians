import direct.directbase.DirectStart
from direct.task import Task
from pandac.PandaModules import Quat
from pandac.PandaModules import VBase3 
import pygame
from math import *

class JoystickTest():
    def __init__(self):
        self.X = 0
        self.Y = 1
        self.Throttle = 2
        self.RotateAxis = 3

        pygame.init()

        self.testModel = loader.loadModel("Art/cockpit_1.bam")
        self.testModel.setPos(0, 45, 20)
        self.testModel.reparentTo(render)

        self.environ = loader.loadModel("models/environment")
        self.environ.reparentTo(render)

        base.camera.reparentTo(self.testModel)
        base.camera.setPos(0, -4.5, 1)

        base.disableMouse()
            
        self.speed = 0
        self.newR = 0
        self.newP = 0
        self.newH = 0
        self.currentJoystick = pygame.joystick.Joystick(0)
        self.currentJoystick.init()
        self.changeQuat = Quat()
        
##        This is not a quaternion tutorial, just an explanation my implementation.
##        First I created a quaternion which will describe how I want to rotate.
##        Note: quaternions are only used to rotate, not move.

    def moveStick(self,task):
        
        for e in pygame.event.get(): 
            self.newR = self.currentJoystick.get_axis(self.X)
            self.newP = self.currentJoystick.get_axis(self.Y)
            self.newH = -self.currentJoystick.get_axis(self.RotateAxis)
            self.speed = -(self.currentJoystick.get_axis(self.Throttle) - 1)

##      set the change quaternion based on the desired change in HPR
##      this is an awesome Panda function

##      It is important to note that while it is possible to create a quat
##      that can gimbal lock using this method, it is impossible with the joystick
##      as it only gives values between -1 and 1

        self.changeQuat.setHpr(VBase3(self.newH, self.newP, self.newR))
        
##      set the model's quaternion by multiplying it's current quat by the change quat
        self.testModel.setQuat(self.changeQuat * self.testModel.getQuat())
        
##      Panda's quats have a function called getForwar() which returns a vector
##      representation of the forward direction of the model
        forwardVector = self.testModel.getQuat().getForward()
        
##      use the forward vector and speed to set position (no spherical coords)
        self.testModel.setPos(self.speed * forwardVector[0] + self.testModel.getX(), 
                              self.speed * forwardVector[1] + self.testModel.getY(), 
                              self.speed * forwardVector[2] + self.testModel.getZ())
            
##        print "HEADING: ", self.testModel.getH()
##        print "PITCH: ", self.testModel.getP()
##        print "THROTTLE: ", self.speed

       
        
        
##        self.testModel.setR(self.testModel, self.newR)
##        self.testModel.setP(self.testModel, self.newP)
##        self.testModel.setH(self.testModel, self.newH)
##        
##
##        self.testModel.setPos(self.testModel, 
##            self.speed * cos(radians(self.testModel.getP(self.testModel))) * sin(radians(self.testModel.getH(self.testModel))),
##            self.speed * cos(radians(self.testModel.getP(self.testModel))) * cos(radians(self.testModel.getH(self.testModel))),
##            self.speed * sin(radians(self.testModel.getP(self.testModel))))
                            
        
        return task.cont



test = JoystickTest()
taskMgr.doMethodLater(0.03, test.moveStick, 'function name')
run()
pygame.quit()