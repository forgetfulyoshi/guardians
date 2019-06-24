
from direct.task import Task

from Player import *
from math import *
import pygame
from pygame.locals import *
from pandac.PandaModules import WindowProperties
from direct.showbase import DirectObject

#Stuff imported for particles
from direct.particles.ForceGroup import ForceGroup
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from pandac.PandaModules import *
import threading
#my stuffs
from WeaponsHandler import *

class FlightHandler(DirectObject.DirectObject):
    def __init__(self, passedModel, passedShip):

        #Set up access to ship and model
        self.model = passedModel
        self.ship  = passedShip

        #Enumerate the Axis
        self.XAxis          = 0
        self.YAxis          = 1
        self.ThrottleAxis   = 2
        self.RotateAxis     = 3

        #Enumerate buttons
        self.gunButton      = 1
        self.thrusterButton = 2
        self.missileButton  = 3

        self.canShootGun        = True
        self.canShootMissile    = True
        self.thrusting          = False
        self.inertialMode       = False
        self.manualControl      = True
        self.mouseLocked        = False
        self.rollRight          = False
        self.rollLeft           = False


        self.acceleration = self.ship.getAccelRate()
        self.maxSpeed = self.ship.getMaxSpeed()

        self.changeQuat = Quat()

        self.velocityVector = Vec3(0,0,0)
        #self.changeVector = Vec3(0,0,0)

        self.throttleValue = 0.0
        self.speedHack = 0.0


        ###
        #Particles
        ###
        base.enableParticles()
        self.particles = Particles('Flight Particles')
        self.particleEffect = ParticleEffect()
        self.initializeParticles()
        self.particleEffect.start(render)
        self.particleEffect.setPos(self.model, 0,0,0)

        self.particleEffect.setBin("fixed", 10)
        self.particleEffect.setDepthTest(False)
        self.particleEffect.setDepthWrite(False)

        #----------------------------------------------
        #Possible Movement Modes:
        #Mode 0 == Keyboard/Mouse
        #Mode 1 == 2 Axis Joystick
        #Mode 2 == 3 Axis Joystick
        #----------------------------------------------
        self.controlType = 0; #keyboard to start with

        self.accept('youdied', self.stopShip)
        self.accept('stopship', self.stopShip)
        self.accept('i', self.toggleInertialMode)
        self.accept("space", self.toggleThrust)
        self.accept("space-up", self.toggleThrust)
        self.acceptOnce(",", self.toggleRollLeft)
        #self.accept(",-up", self.toggleRollLeft)
        self.acceptOnce(".", self.toggleRollRight)
        #self.accept(".-up", self.toggleRollRight)
        self.accept("escape", self.inGameMenu)

        #Make sure Comp has a joystick to turn on Joystick Mode
        joystickCount = pygame.joystick.get_count()
        if  joystickCount > 0: #pygame says 1 joystick == USB Gaming Keyboard (on vista)...
            for x in range(joystickCount):
                self.currentJoystick = pygame.joystick.Joystick(x)
                self.currentJoystick.init()
                numAxes = self.currentJoystick.get_numaxes()
                #print numAxes
                if numAxes >= 4: #temp fix to small problem
                    self.controlType = 2#3 axis
                    break
                else:
                    self.currentJoystick.quit()
                    self.currentJoystick = None
                    self.controlType = 0 #default to keyboard and mouse
                    self.setupMouseControls()
        else:
            self.setupMouseControls()

        #Create the weapons handler
        self.weaponsHandler = WeaponsHandler(self, self.ship, self.model,self.controlType)

    def runMovement(self, task):
        if self.manualControl:
            if self.controlType == 0:
                self.mouseMove()
            else: #3 axis joystick
                self.joystickMove()

        return task.again

    def mouseMove(self):
        self.constrainMouse()

        #Set up all the mouse percentages and hoopla
        ###
        SQUARERADIUS = .7
        if not base.mouseWatcherNode.hasMouse():
            return

        x = base.mouseWatcherNode.getMouseX()
        y = base.mouseWatcherNode.getMouseY()

        percentX = x / SQUARERADIUS
        percentY = y / SQUARERADIUS

        if percentX > 1:
            percentX = 1
        if percentY > 1:
            percentY = 1
        if percentX < -1:
            percentX = -1
        if percentY < -1:
            percentY = -1
            
        if self.rollLeft:
            changeR = -1
        elif self.rollRight:
            changeR = 1
        else:
            changeR = 0

        changeP = percentY
        changeH = -percentX

        #Calculate the ship's new HPR and position
        self.calculateMovement(changeH, changeP, changeR)

        #Keep the particle sphere centered on the ship
        self.particleEffect.setPos(self.model, 0, 0, 0)
        #Set the particles to move in the opposite direction of the ship
        self.particles.emitter.setExplicitLaunchVector(Vec3(-self.velocityVector) * 4)




    def joystickMove(self):
        #Set up the Joystick info for axes percentages

        for e in pygame.event.get():
            changeR = self.currentJoystick.get_axis(self.XAxis)*2
            changeP = self.currentJoystick.get_axis(self.YAxis)*2
            changeH = -self.currentJoystick.get_axis(self.RotateAxis)
            self.throttleValue = (1 -self.currentJoystick.get_axis(self.ThrottleAxis)) / 2
            self.thrusting = self.currentJoystick.get_button(self.thrusterButton) == 1


        if self.currentJoystick.get_button(self.gunButton) == 1 and self.canShootGun:
            t = threading.Timer(.2, self.setCanShootGun).start()
            self.canShootGun = False
            self.eventFire()

        if self.currentJoystick.get_button(self.missileButton) == 1 and self.canShootMissile:
            t = threading.Timer(.2, self.setCanShootMissile).start()
            self.canShootMissile = False
            self.eventMissile()

        #Calculate the ship's new position
        self.calculateMovement(changeH, changeP, changeR)

        #Keep the particle sphere centered on the ship
        self.particleEffect.setPos(self.model, 0, 0, 0)

        #Set the particles to move in the opposite direction of the ship
        self.particles.emitter.setExplicitLaunchVector(Vec3(-self.velocityVector) * 2)

    def calculateMovement(self, h, p, r):
        if not self.inertialMode:
            self.changeQuat.setHpr(VBase3(h, p, r))
            self.model.setQuat(self.changeQuat * self.model.getQuat())
            self.velocityVector = self.model.getQuat().getForward()
            self.velocityVector.normalize()
            self.velocityVector *= (self.throttleValue * self.maxSpeed)
        else:
            if self.thrusting:

                #Set the HPR of the changeQuat
                self.changeQuat.setHpr(VBase3(h, p, r))
                self.model.setQuat(self.changeQuat * self.model.getQuat())

                #Create thrustVector by normalizing the forward vector and multiplying by accel
                thrustVector = self.model.getQuat().getForward()
                thrustVector.normalize()
                thrustVector = thrustVector * self.acceleration
                newVelocityVector = self.velocityVector + thrustVector

                #Cap velocityVector's length at the ship's max speed
                if newVelocityVector.length() > self.maxSpeed:
                    newVelocityVector.normalize()
                    newVelocityVector *= self.maxSpeed

                self.velocityVector = newVelocityVector

            else:
                self.changeQuat.setHpr(VBase3(h, p, r))
                self.model.setQuat(self.changeQuat * self.model.getQuat())


        self.model.setPos(  self.velocityVector[0] + self.model.getX(),
                            self.velocityVector[1] + self.model.getY(),
                            self.velocityVector[2] + self.model.getZ())


    def setupMouseControls(self):
        self.accept('`', self.toggleMouseMode)
        self.accept('1', self.setThrottle, [1])
        self.accept('2', self.setThrottle, [2])
        self.accept('3', self.setThrottle, [3])
        self.accept('4', self.setThrottle, [4])
        self.accept('5', self.setThrottle, [5])
        self.accept('6', self.setThrottle, [6])
        self.accept('7', self.setThrottle, [7])
        self.accept('8', self.setThrottle, [8])
        self.accept('9', self.setThrottle, [9])
        self.accept('0', self.setThrottle, [0])
        self.accept('-', self.startThrottle, ['-'])
        self.accept('--up', self.stopThrottle, ['-'])
        self.accept('=', self.startThrottle, ['+'])
        self.accept('=-up', self.stopThrottle, ['+'])
        self.accept('mouse1', self.eventFire)
        self.accept('mouse1-up', self.eventFire)
        self.accept('mouse3', self.eventMissile)
        props = WindowProperties()
        props.setCursorHidden(False)
        base.win.requestProperties(props)

    def setThrottle(self, arg):
        if arg == '-':
            if self.throttleValue > 0:
                self.throttleValue -= .1
        elif arg == '+':
            if self.throttleValue <= .9:
                self.throttleValue += .1
        else:
            #self.throttleValue = arg / 10.0
            self.speedHack = arg / 10.0
            taskMgr.doMethodLater(0.05, self.smoothSpeedAdjust, "speedAdjust")
            
    def toggleRollRight(self):
        if self.rollRight == False:
            self.acceptOnce(".-up", self.toggleRollRight)
        else:
            self.acceptOnce(".", self.toggleRollRight)
        self.rollRight = not self.rollRight
        #self.acceptOnce(".-up", self.toggleRollRight)
        
    def toggleRollLeft(self):
        if self.rollLeft == False:
            self.acceptOnce(",-up", self.toggleRollLeft)
        else:
            self.acceptOnce(",", self.toggleRollLeft)
        self.rollLeft = not self.rollLeft
        #self.acceptOnce(",-up", self.toggleRollLeft)

    #Code to enable using the plus and minus button to smoothly increase and decrease speed
    #----------------------------------------------------------------------------------------
    def startThrottle(self, arg):
        if arg == '-':
            if self.throttleValue > 0:
                self.throttleValue -= .1
            taskMgr.doMethodLater(.05, self.decreaseThrottle, 'Decrease Throttle')
        elif arg == '+':
            if self.throttleValue <= .9:
                self.throttleValue += .1
            taskMgr.doMethodLater(.05, self.increaseThrottle, 'Increase Throttle')

    def stopThrottle(self, arg):
        if arg == '-':
            taskMgr.remove('Decrease Throttle')
        if arg == '+':
            taskMgr.remove('Increase Throttle')

    def increaseThrottle(self, task):
        if self.throttleValue <= .9:
            self.throttleValue += .1
        return task.again

    def decreaseThrottle(self, task):
        if self.throttleValue >= .1:
            self.throttleValue -= .1
        return task.again

    def smoothSpeedAdjust(self, task):
        if self.throttleValue < (self.speedHack - 0.1):
            self.throttleValue += .1
            return task.again
        elif self.throttleValue > (self.speedHack + 0.1):
            self.throttleValue -= .1
            return task.again
        else:
            return task.done
    #------------------------------------------------------------------------------------

    def toggleMouseMode(self):
        if self.mouseLocked == True:
            props = WindowProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
        else:
            props = WindowProperties()
            props.setCursorHidden(True)
            base.win.requestProperties(props)
        self.mouseLocked = not self.mouseLocked

    #The following are used to smoothly trasistion between inertail and stabilized modes
    #-----------------------------------------------------------------------------------------------
    def toggleInertialMode(self):
        if self.inertialMode:
            self.manualControl = False
            self.currentVector = self.model.getQuat().getForward()
            self.currentVector.normalize()
            self.currentVector *= (self.throttleValue * self.maxSpeed)

            #Create a changeVector to assist in changing the velocityVector
            #doing this because I can't get parameters to work properly when passed through a task
            self.changeVector = self.currentVector - self.velocityVector
            taskMgr.doMethodLater(0.05, self.adjustFromInertial, 'adjustFromInertial')

        self.inertialMode = not self.inertialMode

    def adjustFromInertial(self, task):
        if self.velocityVector.almostEqual(self.currentVector, 0.01):
            self.manualControl = True
            return task.done
        else:
            self.velocityVector += self.changeVector * 0.05
            self.model.setPos(  self.velocityVector[0] + self.model.getX(),
                                self.velocityVector[1] + self.model.getY(),
                                self.velocityVector[2] + self.model.getZ())

            #Keep the particle sphere centered on the ship
            self.particleEffect.setPos(self.model, 0, 0, 0)

            #Set the particles to move in the opposite direction of the ship
            self.particles.emitter.setExplicitLaunchVector(Vec3(-self.velocityVector) * 2)
            return task.again
    #------------------------------------------------------------------------------------------------



    def constrainMouse(self):
        if self.mouseLocked == True:#constraining the mosue into the window
            width = base.win.getProperties().getXSize()
            height = base.win.getProperties().getYSize()

            widthMin = .15 * width
            widthMax = width - (widthMin)

            heightMin = .15 * height
            heightMax = height - (heightMin)

            mousex = base.win.getPointer(0).getX() #in pixels
            mousey = base.win.getPointer(0).getY()

            if mousex > widthMax:
                base.win.movePointer(0, widthMax, mousey)
            elif mousex < widthMin:
                base.win.movePointer(0, widthMin, mousey)
            else:
                pass

            newxpos = base.win.getPointer(0).getX()
            if mousey > heightMax:
                base.win.movePointer(0, newxpos, heightMax)
            elif mousey < heightMin:
                base.win.movePointer(0, newxpos, heightMin)
            else:
                pass


    #Helper functions
    #------------------------------------------
    #def toggleThrust(self):
    #    self.thrusting = True

    def toggleThrust(self):
        self.thrusting = not self.thrusting

    def setCanShootGun(self):
        self.canShootGun = True

    def setCanShootMissile(self):
        self.canShootMissile = True

    def eventFire(self):
        messenger.send("fireGun")
        #print self.ship.energy
        #self.ship.energy -= 1

    def eventMissile(self):
        #self.ship.missiles -= 1
        messenger.send("fireMissile")

    def inGameMenu(self):
        messenger.send('ingamemenu')
        self.mouseLocked = True
        
    def stopShip(self):
        self.throttleValue = 0.2
        self.particleEffect.hide()
    #------------------------------------------


    def initializeParticles(self):
        # Particles parameters
        self.particles.setFactory("ZSpinParticleFactory")
        self.particles.setRenderer("LineParticleRenderer")
        self.particles.setEmitter("SphereVolumeEmitter")
        self.particles.setPoolSize(600)
        self.particles.setBirthRate(0.002)
        self.particles.setLitterSize(1)
        self.particles.setLitterSpread(0)
        self.particles.setSystemLifespan(0.0000)
        self.particles.setLocalVelocityFlag(1)
        self.particles.setSystemGrowsOlderFlag(0)
        # Factory parameters
        self.particles.factory.setLifespanBase(0.7000)
        self.particles.factory.setLifespanSpread(.3000)
        self.particles.factory.setMassBase(1.0000)
        self.particles.factory.setMassSpread(0.0000)
        self.particles.factory.setTerminalVelocityBase(400.0000)
        self.particles.factory.setTerminalVelocitySpread(0.0000)
        # Z Spin factory parameters
        self.particles.factory.setInitialAngle(0.0000)
        self.particles.factory.setInitialAngleSpread(0.0000)
        self.particles.factory.enableAngularVelocity(0)
        self.particles.factory.setFinalAngle(360.0000)
        self.particles.factory.setFinalAngleSpread(0.0000)
        # Renderer parameters
        self.particles.renderer.setAlphaMode(BaseParticleRenderer.PRALPHANONE)
        self.particles.renderer.setUserAlpha(1.00)
        # Line parameters
        self.particles.renderer.setHeadColor(Vec4(0.84, 1.00, 1.00, 1.00))
        self.particles.renderer.setTailColor(Vec4(0.840, 1.00, 1.00, 1.00))
        self.particles.renderer.setLineScaleFactor(1.25)
        # Emitter parameters
        self.particles.emitter.setEmissionType(BaseParticleEmitter.ETEXPLICIT)
        self.particles.emitter.setAmplitude(1.0000)
        self.particles.emitter.setAmplitudeSpread(0.0000)
        self.particles.emitter.setOffsetForce(Vec3(0.0000, 0.0000, 0.0000))
        self.particles.emitter.setExplicitLaunchVector(Vec3(-(self.velocityVector)))
        self.particles.emitter.setRadiateOrigin(Point3(0.0000, 0.0000, 0.0000))
        # Sphere Surface parameters
        self.particles.emitter.setRadius(4.0000)
        self.particleEffect.addParticles(self.particles)

        print "PARTICLE COLOR: ", self.particles.renderer.getHeadColor()

    def cleanUp(self):
        if self.mouseLocked:
            self.toggleMouseMode()

        self.weaponsHandler.cleanUp()
        del self.weaponsHandler

        self.model.removeNode()
        del self.ship

        self.particleEffect.removeAllParticles()
        self.particleEffect.cleanup()
        del self.particleEffect


        del self.particles


        taskMgr.remove('adjustFromInertial')
        taskMgr.remove('speedAdjust')
        self.ignoreAll()
