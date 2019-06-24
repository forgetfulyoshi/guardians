from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

from MyCollisionPlane import *
from CometImmobile import *
from AIPlayer import *
from Player import *

import config
import random



class ZoneThree(DirectObject.DirectObject):
    def __init__(self):

        self.seqList = []
        self.player = Player()
        self.aiPos = None
        self.continueTask = True

        self.accept('endzone', self.endZone)
        self.accept('stop_battleship_spawn', self.endBattleshipTask)


        #Set up the frame for text at beginning and end of zone
        #----------------------------------------------------------------------
        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.zoneImage = DirectFrame()
        self.zoneImage.reparentTo(aspect2d)
        self.zoneImage.setScale(.01)
        self.zoneText1 = OnscreenText(text = 'Chapter 3',
                                    fg = (1, 1, 1, 1),
                                    font = self.menuFont)
        self.zoneText1.reparentTo(self.zoneImage)
        self.zoneText2 = OnscreenText(text = 'Strange Bedfellows',
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
        self.objectiveText2 = OnscreenText(text = 'Get to the asteroid belt',
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
        self.zoneThree = render.attachNewNode('Zone Three')
        self.skybox = loader.loadModel("Art/skybox_mission3.bam")
        self.skybox.reparentTo(self.zoneThree)
        self.skybox.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.skybox.setScale(6000)
        self.endNode = self.skybox.find('**/endNode')
        self.startNode = self.skybox.find('**/startNode')
        self.comets = self.skybox.find('**/comets')

        self.cockpitNode = render.find('**/cockpit_2.egg')
        cockpitPos = self.startNode.getPos(render) + Point3(20, 20, 0)
        self.cockpitNode.setPos(cockpitPos)
        self.cockpitNode.lookAt(self.endNode)

        self.endPlane = MyCollisionPlane(self.endNode.getPos(render), self.startNode)
        #----------------------------------------------------------------------

        #Load comets
        #----------------------------------------------------------------------
        self.cometPos = self.zoneThree.attachNewNode('Comet Positions')
        self.comet1 = loader.loadModel('Art/comet_1.bam')
        self.comet2 = loader.loadModel('Art/comet_2.bam')
        for child in self.comets.getChildrenAsList():
            if randint(0,1) == 0:
                placeholder = self.cometPos.attachNewNode('comet')
                placeholder.setPos(child.getPos(render))
                placeholder.setScale(randint(7, 35))
                self.comet1.instanceTo(placeholder)
            else:
                placeholder = self.cometPos.attachNewNode('comet')
                placeholder.setPos(child.getPos(render))
                placeholder.setScale(randint(7, 35))
                self.comet2.instanceTo(placeholder)
        #----------------------------------------------------------------------

        #Load AI
        #----------------------------------------------------------------------
        AIPlayer("ben", "vulture", 'bad', self.startNode.getPos(render) + Point3(100, 100, 0))
        AIPlayer('ben' , 'hawkeye' , 'bad', self.startNode.getPos(render) + Point3(0, 75, 20))
        AIPlayer('ben' , 'hawkeye' , 'bad', self.startNode.getPos(render) + Point3(100, 0, 20))
        AIPlayer('roger' , 'hawkeye' , 'bad', self.startNode.getPos(render) + Point3(100, 100, 20))

        #
        self.battleShip = AIPlayer("battleShip", "alienBattleShip", "bad", self.startNode.getPos(render) + Point3(200, 0, 40))
    
        taskMgr.doMethodLater(100, self.spawnShipsFromCruiser, "ZoneThree_spawnShipsFromCruiserTask")
        #----------------------------------------------------------------------
        
        messenger.send("addSfx", [ "warning","Art/audio/shipWarning.wav"])
        taskMgr.add(self.checkDistance, 'Check Distance')

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
                                    Func(self.zoneImage.hide)),
                           Sequence(Func(self.objectiveTextNode.show),
                                    LerpColorScaleInterval(self.objectiveTextNode,
                                                            2.0,
                                                            Vec4(1, 1, 1, 1),
                                                            Vec4(1, 1, 1, 0)),
                                    Wait(12),
                                    LerpColorScaleInterval(self.objectiveTextNode,
                                                            2.0,
                                                            Vec4(1, 1, 1, 0),
                                                            Vec4(1, 1, 1, 1)),
                                    Func(self.objectiveTextNode.hide)))
        zoneSeq.start()
        self.seqList.append(zoneSeq)
        #----------------------------------------------------------------------
        
        messenger.send("toggleWarning")

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
        
    def spawnShipsFromCruiser(self, task):
        
        if not self.continueTask:
            return task.done
        
        spawnLocation = self.battleShip.shipModel.find("**/bays").getChildrenAsList()[random.randint(0,2)]
        
        for i in range(0,4):
            AIPlayer("ben", "vulture", "bad", spawnLocation.getPos(render))
            AIPlayer("roger", "hawkeye", "bad", spawnLocation.getPos(render))
            
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

        return task.again
    
    def endBattleshipTask(self):
        self.continueTask = False
        
    def checkDistance(self, task):
        if not render.getDistance(self.cockpitNode) <= 5000:
            messenger.send('missionfailedmenu', ['Outside boundaries'])
        else:
            return task.cont
        
    def cleanUp(self):
        messenger.send("toggleWarning")
        
        for seq in self.seqList:
            seq.pause()
            del seq
        del self.seqList
        
        taskMgr.remove("ZoneThree_spawnShipsFromCruiserTask")
        taskMgr.remove('Check Distance')
        
        self.endPlane.cleanUp()
        del self.endPlane
        
        for child in render.find('**/other').getChildrenAsList():
            child.removeNode()

        self.zoneThree.removeNode()
        self.zoneImage.destroy()
        self.endImage.destroy()
        self.objectiveTextNode.removeNode()

        self.player.cleanUp()
        del self.player
