from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
import config

from direct.task import Task
from math import *

class Radar(DirectObject.DirectObject):
    def __init__(self, cockpitNode):
        #find all of the nodes i need
        self.screenNode = render.find("**/radarScreen")
        self.cockpitNode = cockpitNode
        #self.hologramNode = self.cockpitNode.find("**/hologramLocator2")
        hull = self.cockpitNode.find("**/hull")
        self.missileNode = render.find("**/missiles")
        self.enemys = render.find("**/bad")
        self.allys = render.find("**/good")
        self.screenNode.setScale(1)
        #self.screenNode.setPos(self.screenNode, -3,-.2,-.127)
        self.screenNode.setPos(self.screenNode,-.25,-.55,.3)
        self.screenNode.setTransparency(TransparencyAttrib.MAlpha)
        #self.screenNode.setColor(1,1,1,.5)
        
        mainWindow = base.win
        self.altBuffer = mainWindow.makeTextureBuffer("radarScreen", 512, 512)
        self.altRender = NodePath("radarScreen")
        
        self.altCam = base.makeCamera(self.altBuffer)
        self.altCam.reparentTo(self.altRender)
        self.altCam.setPos(0,-3,0)
        
        self.setupScreen()        
        
        self.screenNode.setTexture( self.altBuffer.getTexture() ,1)
        
        taskMgr.doMethodLater(.03, self.manageRadar, 'RadarMoveTask')
        self.blipInstancer = OnscreenImage(image = 'Art/textures/radar_blip.png',
                                        pos = (0,-.01,0),
                                        scale = .04,
                                        #color = (1,1,1,.8),
                                        parent = self.altRender)
        self.blipInstancer.setTransparency(TransparencyAttrib.MAlpha)
        self.blipInstancer.detachNode()
        
        self.radarDirParent = self.altRender.attachNewNode("radarDirParent")
        self.radarDirection = OnscreenImage(image = 'Art/textures/radar_direction.png',
                                        pos = (0,0,0),
                                        scale = 1,
                                        color = (1,1,1,.8),
                                        parent = self.radarDirParent)
        self.radarDirection.setTransparency(TransparencyAttrib.MAlpha)
  
    def setupScreen(self):
        self.backImage = OnscreenImage(image = 'Art/textures/radar_traditional.png',
                                        pos = (0,.01,0),
                                        scale = 1,
                                        color = (1,1,1,.8),
                                        parent = self.altRender)
        self.backImage.setTransparency(TransparencyAttrib.MAlpha)
        self.blipNode = self.altRender.attachNewNode("blipNode")  
       
    def manageRadar(self, task):
        for x in self.blipNode.getChildrenAsList():
            x.removeNode()
        for x in self.enemys.getChildrenAsList():
            self.renderBlip("enemy", x)
        for x in self.allys.getChildrenAsList():
            self.renderBlip("friendly", x)
                
        #for x in self.missileNode.getChildrenAsList():
            #self.renderBlip("missile",x)
        pod = render.find("**/Pod")
        if not pod.isEmpty():
            self.renderBlip("friendly", pod)
        
        return task.again

    def renderBlip(self, type, him):
        RADAR_MAX_DISTANCE = 350
        if type == "enemy":
            color = Vec4(1.0,0.1,0.1,1.0)
        elif type == "friendly":
            color = Vec4(0,0,0,1.0)
            
        hisPos = him.getPos(self.cockpitNode)
        hisPosVector = Vec3(hisPos[0], hisPos[1], self.cockpitNode.getZ())
        hisPosPoint = Point3(hisPos[0], hisPos[1], hisPos[0]) ##Point3s are Consts
        hisPosVector.normalize()
        
        tempNode = render.attachNewNode("stupidTempNode")
        tempNode.setPos(him.getPos(render))
        
        distance = self.cockpitNode.getDistance(tempNode)
        placeholder = self.blipNode.attachNewNode("blipPlaceholder")
        ratio = distance / RADAR_MAX_DISTANCE
        if ratio > 1:
            ratio = 1
        ratioVec = hisPosVector * ratio
        placeholder.setPos(Point3(ratioVec[0], -.1, ratioVec[1]) * .7)
        placeholder.setColor(color)
        self.blipInstancer.instanceTo(placeholder)
        
        tempNode.removeNode()
        #tempCockpitNode.removeNode()
        
        ###
        #Old 3d  radarcode
        ##
        """
        blip = loader.loadModel("Art/greyblip.bam")
        rec = loader.loadModel("Art/greyrec.bam")
        
        blip.setScale(.07)
        rec.setScale(.07,1.12,.07)
        blip.setColor(color)
        rec.setColor(color)
        
        hisPos = him.getPos(self.cockpitNode)
        hisPosVector = Vec3(hisPos[0], hisPos[1], hisPos[2])
        hisPosVector.normalize()
        
        distance = self.cockpitNode.getDistance(him)
        percent = distance/RADAR_MAX_DISTANCE
        if percent <= 1:
            #important to orient the blip to opposite side
            #such that it is on the side of the sphere that is facing you
            hisPosVector = hisPosVector * -1
            
            blip.reparentTo(self.blipNode)
            blip.setPos(hisPosVector*percent)
            
            rec.reparentTo(self.blipNode)
            rec.lookAt(blip)
        """
        
    def cleanUp(self):
        taskMgr.remove('RadarMoveTask')

        self.blipNode.removeNode()
        
        self.altCam.removeNode()
        del self.altCam
        
        self.altBuffer.setOneShot(True)
        del self.altBuffer
        
        self.altRender.removeNode()
        del self.altRender