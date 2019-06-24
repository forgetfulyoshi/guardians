from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
import config


from Collidable import *
class TargetScreen(DirectObject.DirectObject):
    def __init__(self, screenNode):
        #self.id = id
        self.screenNode = screenNode
        self.screenNode.setTransparency(TransparencyAttrib.MAlpha)
        self.hasTarget = False
        self.targetShields = 0
        self.targetHull = 0
        
        CIRCLE_RADIUS = 1
        #self.targetRef = Collidable.dispatcher.collidables['ship'][id]
        
        #self.targetArrow = OnscreenImage(image = 'Art/textures/arrow.png',
        #                                     parent = screenNode.getParent().getParent().getParent().getParent(),
        #                                     pos = (0,-.04,.7),
        #                                     color = (1,1,1,.55),
        #                                     scale = .04
        #                                )
        ##self.targetArrow.setBillboardPointEye()
        #self.targetArrow.setTransparency(TransparencyAttrib.MAlpha)
        #self.targetArrow.hide()
        self.arrow = loader.loadModel("Art/arrow.bam")
        self.arrow.reparentTo(screenNode.getParent().getParent().getParent().getParent())
        self.arrow.setPos(0,-.3,1)
        self.arrow.setHpr(0,0,0)
        self.arrow.setScale(.02)
        self.arrow.setColor(.7,0,0,1)
        self.arrow.hide()
        plight = PointLight('plight')
        plight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        plnp = screenNode.getParent().getParent().getParent().getParent().attachNewNode(plight)
        plnp.setPos(0,-.1,1.2)
        #plnp.setPos(10, 20, 0)
        self.arrow.setLight(plnp)
        self.arrow.setBin("fixed", 1)

        #x = loader.loadTexture("Art/textures/metal1.png")
        #self.arrow.setTexture(x)
        #self.arrow.setColor(1,0,0,1)
        #creenNode.reverseLs()
        
        mainWindow = base.win
        
        self.altBuffer = mainWindow.makeTextureBuffer("targetScreen", 512, 512)
        self.altRender = NodePath("targetscreen")
        
        self.altCam = base.makeCamera(self.altBuffer)
        self.altCam.reparentTo(self.altRender)
        self.altCam.setPos(0,-3,0)
        self.targetShip = None
        
        self.cockpit = self.screenNode.getParent().getParent().getParent().getParent()
        self.interval = Sequence()
        
        #self.accept("v", base.bufferViewer.toggleEnable)
        #self.accept("V", base.bufferViewer.toggleEnable)
        #base.bufferViewer.setPosition("llcorner")
        #base.bufferViewer.setCardSize(0.25, 0.0)
        
        
        self.setupScreen()        
        
        self.screenNode.setTexture( self.altBuffer.getTexture() ,1)
        
        self.RED = Vec4(.6,0,0,1)
        self.ORANGE = Vec4(.89,.3,0,1)
        self.YELLOW = Vec4(.89,1,0,1)
        self.GREEN = Vec4(0,1,0,1)
        self.BLUE = Vec4(0,0,1,1)
        
        #taskMgr.doMethodLater(1, self.manageScreen, 'TargetScreen')
        
    def clearTarget(self):
        if self.targetShip:
            self.targetShip.removeNode()
            self.interval.pause()
            self.targetBillboard.removeNode()
    def NewTarget(self, id, node, nodeTarget):
        print "NEWTARGET"
        print nodeTarget
        self.clearTarget()
        self.hasTarget = True
        self.id = id
        self.targetNode = nodeTarget
        if Collidable.dispatcher.collidables['ship'].has_key(str(id)):
            self.targetRef = Collidable.dispatcher.collidables['ship'][str(id)]
        self.targetShip = loader.loadModel(self.targetRef.ship.shipPath)
        
        self.targetBillboard = OnscreenImage(image = 'Art/textures/target.png',
                                             parent = nodeTarget,
                                             #pos = self.targetNode.getPos(),
                                             color = (1,1,1,.4),
                                             scale = 1.1)
        self.targetBillboard.setTransparency(TransparencyAttrib.MAlpha)
        self.targetBillboard.setBillboardPointEye()
        
        
        self.interval = LerpHprInterval(self.targetBillboard, 6, Vec3(0,0,360), Vec3(0,0,0))
        self.interval.loop()
        
        self.targetShip.reparentTo(self.altRender)
        self.targetShip.setP(90)
        self.targetShip.setPos(0,0,0)
        self.targetShip.setScale(.5,.7,.7)
        attrib = RenderModeAttrib.make(2,2.5)
        self.targetShip.setAttrib(attrib)
        
        self.left = self.targetShip.find("**/left")
        self.right = self.targetShip.find("**/right")
        self.front = self.targetShip.find("**/front")
        self.back = self.targetShip.find("**/back")
        self.windows = self.targetShip.find("**/windows")
        
        #self.windows.setColor(Vec4(0,0,0,0))
        self.left.setColor(0,0,0,0)
        self.right.setColor(0,0,0,0)
        self.front.setColor(0,0,0,0)
        self.back.setColor(0,0,0,0)
        taskMgr.doMethodLater(.03, self.manageScreen, 'TargetScreen')
    def setupScreen(self):
        pass
        #self.TEXT_COLOR = Vec4(.1,.95,.1,9)
        
        
        #self.backImage.setTransparency(TransparencyAttrib.MAlpha)
        #self.backImage.setColor(0,0,0,.98)
    def setColor(self, hp, nodepath):
        if hp >= 81:
            if not nodepath.getColor() == self.BLUE:
                nodepath.setColor(self.BLUE)
        elif hp >= 61:
            if not nodepath.getColor() == self.GREEN:
                nodepath.setColor(self.GREEN)
        elif hp >= 41:
            if not nodepath.getColor() == self.YELLOW:
                nodepath.setColor(self.YELLOW)
        elif hp >= 21:
            if not nodepath.getColor() == self.ORANGE:
                nodepath.setColor(self.ORANGE)
        else:
            if not nodepath.getColor() == self.RED:
                nodepath.setColor(self.RED)

    def manageScreen(self, task):
        ##if self.hasTarget == False or self.targetRef == None:
         #   #self.screenNode.clearTexture()
         #   self.targetRef = None
         #   return task.done
        #print Collidable.dispatcher.collidables['ship'].has_key(self.id)
        if Collidable.dispatcher.collidables['ship'].has_key(self.id) and self.targetRef.isDead == False:
            #shield = self.targetRef.ship.getShieldLevel()
            #hull = self.targetRef.ship.getHullStrength()
            leftHull = self.targetRef.ship.leftHull
            rightHull = self.targetRef.ship.rightHull
            frontHull = self.targetRef.ship.frontHull
            backHull = self.targetRef.ship.backHull

            self.setColor(leftHull, self.left)
            self.setColor(rightHull, self.right)
            self.setColor(frontHull, self.front)
            self.setColor(backHull, self.back)
            
            him = self.targetNode
            me = self.cockpit
            hisPos = him.getPos(render)
            myPos = me.getPos(render)
   
            relPos2 = Vec3(hisPos[0]-myPos[0], hisPos[1]-myPos[1], hisPos[2]-myPos[2])
            #print relPos, relPos2
            relPos2.normalize()
            angle = self.cockpit.getQuat().getForward().angleDeg(relPos2)
            #print "Angle between", angle
            if angle > 20:
                self.arrow.show()
                self.arrow.lookAt(self.targetNode)
                
            else:
                self.arrow.hide()
            
          
            return task.again
        else:
            self.targetShip.removeNode()
            self.interval.pause()
            self.targetBillboard.removeNode()
        
        #else: #ship was deleted
            #self.screenNode.clearTexture()
        #    self.targetRef = None
        #    return task.done
        
    def cleanUp(self):
        taskMgr.remove('TargetScreen')
        if self.interval:
            self.interval.pause()
            
        self.altCam.removeNode()
        del self.altCam
        
        self.altBuffer.setOneShot(True)
        del self.altBuffer
        
        self.altRender.removeNode()
        del self.altRender