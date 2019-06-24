from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
import config

class VelocityScreen(DirectObject.DirectObject):
    def __init__(self, flightHandler, screenNode):
        self.screenNode = screenNode
        self.ship = flightHandler.ship
        self.screenNode.setScale(1.5)
        self.screenNode.setPos(self.screenNode, 0,0,.05)
        self.screenNode.setTransparency(TransparencyAttrib.MAlpha)
        self.flightHandler = flightHandler
        self.isInertial = flightHandler.inertialMode
        
        mainWindow = base.win
        self.missileAmmo = self.ship.missiles
        
        self.altBuffer = mainWindow.makeTextureBuffer("velocityScreen", 512, 512)
        self.altRender = NodePath("velocityscreen")
        
        self.altCam = base.makeCamera(self.altBuffer)
        self.altCam.reparentTo(self.altRender)
        self.altCam.setPos(0,-3,0)

        self.setupScreenLocations()        
        
        self.screenNode.setTexture( self.altBuffer.getTexture() ,1)
        
        taskMgr.doMethodLater(.07, self.manageScreen, 'VelocityScreen')
        
    def setupScreenLocations(self):
        self.energyHeader = TextNode('energyHeader')
        self.energyHeader.setText("Energy ")
        self.energyHeader.setTextColor(config.TEXT_COLOR)
        self.energyHeaderNodePath = self.altRender.attachNewNode(self.energyHeader)
        self.energyHeaderNodePath.setPos(-.77,0,-.16)
        self.energyHeaderNodePath.setScale(.13)
        
        self.missileHeader = TextNode('missileHeader')
        self.missileHeader.setText("Missiles: ")
        self.missileHeader.setTextColor(config.TEXT_COLOR)
        self.missileHeaderNodePath = self.altRender.attachNewNode(self.missileHeader)
        self.missileHeaderNodePath.setPos(-.8,0,0)
        self.missileHeaderNodePath.setScale(.13)
        
        self.missileCount = TextNode('missileCount')
        self.missileCount.setText("0")
        self.missileCount.setTextColor(config.TEXT_COLOR)
        self.missileCountNodePath = self.altRender.attachNewNode(self.missileCount)
        self.missileCountNodePath.setPos(-.35,0,0)
        self.missileCountNodePath.setScale(.13)
        
        self.speedHeader = TextNode('speedHeader')
        self.speedHeader.setText("Speed")
        self.speedHeader.setTextColor(config.TEXT_COLOR)
        self.speedHeaderNodePath = self.altRender.attachNewNode(self.speedHeader)
        self.speedHeaderNodePath.setPos(.03,0,-.15)
        self.speedHeaderNodePath.setScale(.13)
        
        self.throttleHeader = TextNode('throttleHeader')
        self.throttleHeader.setText("Throttle")
        self.throttleHeader.setTextColor(config.TEXT_COLOR)
        self.throttleHeaderNodePath = self.altRender.attachNewNode(self.throttleHeader)
        self.throttleHeaderNodePath.setPos(.42,0,-.15)
        self.throttleHeaderNodePath.setScale(.13)
        
        #self.meterbarNode = self.altRender.attachNewNode("meterbarNode")
        self.speedMeterBorder = OnscreenImage(image = 'Art/textures/meterbar.png',
                                        pos = (.2,0,-.5),
                                        scale = (.22,1,.3),
                                        color = (1,1,1,1),
                                        parent = self.altRender)
        self.speedMeterBorder.setTransparency(TransparencyAttrib.MAlpha)
        self.throttleMeterBorder = OnscreenImage(image = 'Art/textures/meterbar.png',
                                        pos = (.6,0,-.5),
                                        scale = (.22,1,.3),
                                        color = (1,1,1,1),
                                        parent = self.altRender)
        self.throttleMeterBorder.setTransparency(TransparencyAttrib.MAlpha)
        
        self.speedMeterMiddle= OnscreenImage(image = 'Art/textures/meterbar_middle.png',
                                        pos = (.2,.1,-1.1), #-.5 is top
                                        scale = (.33,1,.33),
                                        color = (1,1,1,1),
                                        parent = self.altRender)
        self.speedMeterMiddle.setTransparency(TransparencyAttrib.MAlpha)
        self.throttleMeterMiddle = OnscreenImage(image = 'Art/textures/meterbar_middle.png',
                                        pos = (.61,.1,-1.1),#-.5 is top
                                        scale = (.33,1,.33),
                                        color = (1,1,1,1),
                                        parent = self.altRender)
        self.throttleMeterMiddle.setTransparency(TransparencyAttrib.MAlpha)
        self.acrossMeter = OnscreenImage(image = 'Art/textures/meterbar_across.png',
                                        pos = (.40,0,-.77),#-.5 is top
                                        scale = (.22,.1,.03),
                                        color = (1,1,1,1),
                                        parent = self.altRender)
        
        self.energyMeterBorder = OnscreenImage(image = 'Art/textures/meterbar.png',
                                        pos = (-.6,0,-.5),
                                        scale = (.22,1,.3),
                                        color = (1,1,1,1),
                                        parent = self.altRender)
        self.energyMeterBorder.setTransparency(TransparencyAttrib.MAlpha)
        self.energyMeterMiddle = OnscreenImage(image = 'Art/textures/meterbar_middle.png',
                                        pos = (-.62,.1,-1.1), #-.5 is top
                                        scale = (.33,1,.33),
                                        color = (1,1,1,1),
                                        parent = self.altRender)
        self.energyMeterMiddle.setTransparency(TransparencyAttrib.MAlpha)
        
        
        self.backShip = loader.loadModel("Art/pegasus.bam")
        self.backShip.reparentTo(self.altRender)
        self.backShip.setP(90)
        self.backShip.setPos(.38,0,.4)
        self.backShip.setScale(.28)
        #self.backShip.
        attrib = RenderModeAttrib.make(2,1)
        self.backShip.setAttrib(attrib)
        self.backShip.setColor(Vec4(.1,.95,.1,1))
        
        self.velocityArrow = loader.loadModel("Art/arrow.bam")
        self.velocityArrow.reparentTo(self.altRender)
        self.velocityArrow.setColor(.89,0,0,1)
        self.velocityArrow.setScale(.03,.07,.03)
        self.velocityArrow.setPos(.38,0,.4)
        #self.axis = loader.loadModel('zup-axis.egg')
        #self.axis.reparentTo(self.altRender)
        #self.axis.setScale(.08)
        #self.axis.setPos(-.3,0,0)
        ##self.axis.setColor(1,1,1,.6)
        ##self.axis.setHpr(10,10,10)
        #self.axis.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        
        
    def manageScreen(self, task):
        velocity = self.flightHandler.velocityVector
        inertial = self.flightHandler.inertialMode
        throttle = self.flightHandler.throttleValue
        
        if inertial != self.isInertial:
            self.isInertial = not self.isInertial
            if inertial:
                self.acrossMeter.hide()
            else:
                self.acrossMeter.show()
    
        

        throttlePercentMove = throttle * .55 #.6 is how much move up to max out
        self.throttleMeterMiddle.setZ(-1.1 + throttlePercentMove)
        
        speedPercentMove = (velocity.length() / self.flightHandler.ship.getMaxSpeed()) *.55
        self.speedMeterMiddle.setZ(-1.1 + speedPercentMove)
        
        energyPercentMove = (float(self.ship.energy)/ 100.0) * .55
        #print "ENERGY:" ,self.ship.energy, "  ", energyPercentMove
        self.energyMeterMiddle.setZ(-1.1+energyPercentMove)
        
        if self.ship.missiles != int(self.missileCount.getText()):
            self.missileCount.setText(str(self.ship.missiles))
        
        if not self.isInertial:
            self.acrossMeter.setZ(-.77 + throttlePercentMove)

        
        #print throttle
        velocity2 = Vec3(velocity[0], velocity[1], velocity[2])
        velocity2.normalize()
        dummyNode = self.altRender.attachNewNode("dummyNode")
        dummyNode.setPos(Point3(.38,0,.4) + Point3(velocity2[0],velocity2[1], velocity2[2]))
            
        self.velocityArrow.lookAt(dummyNode)
        dummyNode.removeNode()
        
        self.backShip.setHpr(self.flightHandler.model.getHpr())
        
        
        return task.again
    
    def cleanUp(self):
        del self.flightHandler
        del self.ship
        taskMgr.remove('VelocityScreen')
        
        self.altCam.removeNode()
        del self.altCam
        
        self.altBuffer.setOneShot(True)
        del self.altBuffer
        
        self.altRender.removeNode()
        del self.altRender
        