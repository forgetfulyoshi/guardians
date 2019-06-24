from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

from MyCollisionPlane import *
from CometImmobile import *
from Player import *
from AsteroidHandler import *
from AIPlayer import *

import config
import random



class ZoneFour(DirectObject.DirectObject):
    def __init__(self):

        self.seqList = []
        self.player = Player()

        self.accept('endzone', self.endZone)
        self.accept('outsidebelt', self.outsideBelt)

        #Set up the frame for text at beginning and end of zone
        #----------------------------------------------------------------------
        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.zoneImage = DirectFrame()
        self.zoneImage.reparentTo(aspect2d)
        self.zoneImage.setScale(.01)
        self.zoneText1 = OnscreenText(text = 'Chapter 4',
                                    fg = (1, 1, 1, 1),
                                    font = self.menuFont)
        self.zoneText1.reparentTo(self.zoneImage)
        self.zoneText2 = OnscreenText(text = 'Never Tell Me The Odds!',
                                 pos = (0, -.1),
                                 fg = (1, 1, 1, 1),
                                 font = self.menuFont)
        self.zoneText2.reparentTo(self.zoneImage)
        self.zoneImage.hide()
        
        self.endImage = OnscreenImage(image = 'Art/textures/mission3_plane.png',
                                        scale = 2,
                                        color = (0, 0, 0, 0))
        self.endImage.reparentTo(aspect2d)
        self.endImage.setTransparency(TransparencyAttrib.MAlpha)
        self.endImage.hide()
        
        self.objectiveTextNode = aspect2d.attachNewNode('Objective Font')
        self.objectiveText = OnscreenText(text = 'Objective',
                                            mayChange = 1,
                                            scale = .05,
                                            fg = (1, 1, 1, 1),
                                            pos = (-.5, .5, 0))
        self.objectiveText.reparentTo(self.objectiveTextNode)
        self.objectiveText.setTransparency(TransparencyAttrib.MAlpha)
        self.objectiveText2 = OnscreenText(text = 'Get through the asteroid belt',
                                            mayChange = 1,
                                            scale = .05,
                                            fg = (1, 1, 1, 1),
                                            pos = (-.5, .45, 0))
        self.objectiveText2.reparentTo(self.objectiveTextNode)
        self.objectiveTextNode.setTransparency(TransparencyAttrib.MAlpha)
        self.objectiveText2.setTransparency(TransparencyAttrib.MAlpha)
        self.objectiveTextNode.hide()
        #----------------------------------------------------------------------

        #Load skybox and other essentials
        #----------------------------------------------------------------------
        self.zoneFour = render.attachNewNode('Zone Four')
        self.skybox = loader.loadModel("Art/skybox_mission4.bam")
        self.skybox.reparentTo(self.zoneFour)
        self.skybox.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.skybox.setScale(2000)
        self.endNode = self.skybox.find('**/endNode')
        self.startNode = self.skybox.find('**/startNode')
        self.cockpitStartNode = self.skybox.find('**/cockpitNode')
        self.comets = self.skybox.find('**/comets')

        self.cockpitNode = render.find('**/cockpit_2.egg')
        cockpitPos = self.cockpitStartNode.getPos(render) + Point3(100, 100, 0)
        self.cockpitNode.setPos(cockpitPos)
        self.cockpitNode.lookAt(self.endNode)

        for child in self.comets.getChildrenAsList():
            CometImmobile(child.getPos(render), 100, 1000000, 200)

        self.topPlaneNode = self.skybox.find('**/topPlane')
        self.bottomPlaneNode = self.skybox.find('**/bottomPlane')
        self.rightPlaneNode = self.skybox.find('**/rightPlane')
        self.leftPlaneNode = self.skybox.find('**/leftPlane')
        self.endPlane = MyCollisionPlane(self.endNode.getPos(render), self.startNode)
        self.startPlane = MyCollisionPlane(self.startNode.getPos(render), self.endNode, 'outsidebelt')
        self.topPlane = MyCollisionPlane(self.topPlaneNode.getPos(render), self.bottomPlaneNode, 'outsidebelt')
        self.bottomPlane = MyCollisionPlane(self.bottomPlaneNode.getPos(render), self.topPlaneNode, 'outsidebelt')
        self.rightPlane = MyCollisionPlane(self.rightPlaneNode.getPos(render), self.leftPlaneNode, 'outsidebelt')
        self.leftPlane = MyCollisionPlane(self.leftPlaneNode.getPos(render), self.rightPlaneNode, 'outsidebelt')
        #----------------------------------------------------------------------
        
        #Load Arrow and start tasks
        #----------------------------------------------------------------------
        self.arrow = loader.loadModel("Art/arrow.bam")
        self.arrow.reparentTo(self.cockpitNode)
        self.arrow.setPos(0,-.3,1)
        self.arrow.setHpr(0,0,0)
        self.arrow.setScale(.02)
        self.arrow.setColor(.93,0,0,1)
        taskMgr.add(self.pointArrow, 'Arrow Pointer')
        taskMgr.doMethodLater(60, self.lerpObjective, 'Lerp Objective Text')
        #----------------------------------------------------------------------

       
        self.startZone()


    def startZone(self):
        #Set up frame for start sequence
        #----------------------------------------------------------------------
        self.zoneImage.show()
        #----------------------------------------------------------------------

        #Zoom In Sequence
        #----------------------------------------------------------------------
        zoneSeq = Parallel(Sequence(LerpScaleInterval(self.zoneImage,
                                6.0, 2.0, .01),
                                Wait(1.0),
                                Func(self.startAsteroids),
                                Func(self.zoneImage.hide)),
                            Sequence(Func(self.objectiveTextNode.show),
                                        LerpColorScaleInterval(self.objectiveTextNode,
                                                                2.0,
                                                                Vec4(1, 1, 1, 1),
                                                                Vec4(1, 1, 1, 0)),
                                        Wait(14),
                                        LerpColorScaleInterval(self.objectiveTextNode,
                                                                2.0,
                                                                Vec4(1, 1, 1, 0),
                                                                Vec4(1, 1, 1, 1)),
                                        Func(self.objectiveTextNode.hide)))
        zoneSeq.start()
        self.seqList.append(zoneSeq)
        #----------------------------------------------------------------------
        

    def endZone(self):
        #Zoom In Sequence
        #----------------------------------------------------------------------
        zoneSeq = Sequence(Func(self.endImage.show))
        zoneSeq.append(LerpColorInterval(self.endImage,
                                4,
                                Vec4(0, 0, 0, 1),
                                Vec4(0, 0, 0, 0)))
        zoneSeq.append(Func(messenger.send, 'gotonextzone'))
        zoneSeq.start()
        self.seqList.append(zoneSeq)
        #----------------------------------------------------------------------
        
    def startAsteroids(self):
        self.asteroidHandler = AsteroidHandler(self.player.playerCockpit.getCockpit())
    
    def pointArrow(self, task):
        self.arrow.lookAt(self.endNode)
        return task.cont
    
    def lerpObjective(self, task):
        self.objectiveSeq = Sequence(Func(self.objectiveTextNode.show),
                                LerpColorScaleInterval(self.objectiveTextNode,
                                                        2.0,
                                                        Vec4(1, 1, 1, 1),
                                                        Vec4(1, 1, 1, 0)),
                                Wait(14),
                                LerpColorScaleInterval(self.objectiveTextNode,
                                                        2.0,
                                                        Vec4(1, 1, 1, 0),
                                                        Vec4(1, 1, 1, 1)),
                                Func(self.objectiveTextNode.hide))
        self.objectiveSeq.start()
        self.seqList.append(self.objectiveSeq)

    def outsideBelt(self):
        Sequence(Func(self.asteroidHandler.cleanUp),
                    Func(self.endImage.show),
                    LerpColorInterval(self.endImage,
                                2,
                                Vec4(0, 0, 0, 1),
                                Vec4(0, 0, 0, 0)),
                    Wait(2),
                    Func(self.outsideBelt2)).start()
##        self.asteroidHandler.cleanUp()
##        del self.asteroidHandler
        
    def outsideBelt2(self):
        self.endImage.hide()
        messenger.send('changecockpit')
        messenger.send('stopship')
        taskMgr.remove('runMovement')
        self.pegasusNode = render.find('**/pegasus.egg')
        self.player.playerShip.frontHull = 5
        self.player.playerShip.backHull = 5
        self.player.playerShip.leftHull = 5
        self.player.playerShip.rightHull = 5
        print self.pegasusNode.getPos(render)
        print base.camera.getPos(render)
        self.battleShip = AIPlayer("ben",
                                    "vulture",
                                    "bad",
                                    self.pegasusNode.getPos(render) + Point3(100, 100, 0))
        self.battleShip.shipModel.lookAt(self.pegasusNode)
        base.camera.reparentTo(self.battleShip.shipModel)
        base.camera.setPos(0, -10, 2)
        base.camera.wrtReparentTo(self.zoneFour)
        base.camera.lookAt(self.pegasusNode)
        
        
    def cleanUp(self):
        
        taskMgr.remove('Arrow Pointer')
        taskMgr.remove('Lerp Objective Text')
        
        self.ignoreAll()
        
        for seq in self.seqList:
            seq.pause()
            del seq
##        del self.seqList
        
        if self.asteroidHandler:
            self.asteroidHandler.cleanUp()
        
        #Clean up the collision planes
        #----------------------------------------------------------------------
        self.player.cleanUp()
        del self.player
        
        self.topPlane.cleanUp()
        del self.topPlane
        
        self.bottomPlane.cleanUp()
        del self.bottomPlane
        
        self.rightPlane.cleanUp()
        del self.rightPlane
        
        self.leftPlane.cleanUp()
        del self.leftPlane
        
        self.endPlane.cleanUp()
        del self.endPlane
        
        self.startPlane.cleanUp()
        del self.startPlane
        #----------------------------------------------------------------------
          
        #Make sure the other node has no children  
        for child in render.find('**/other').getChildrenAsList():
            child.removeNode()
        
        
        self.zoneFour.removeNode()
        self.zoneImage.destroy()
        self.endImage.destroy()
        self.objectiveTextNode.removeNode()