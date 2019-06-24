from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

from Pod import *
from AIPlayer import *
from Player import *

import config

# These are our #Defines for this level.  Time is in seconds
ZONE_TIME = 15 * 60
SPAWN_TIME = 180



class ZoneTwo(DirectObject.DirectObject):
    UID = 0
    def __init__(self):
        ZoneTwo.UID += 1
        self.zoneCompleted = False

        #Set up a list of sequences to make sure we finish them all
        #and delete accordingly
        self.sequenceList = []
        self.accept('poddied', self.podDied) #Stop the pods movement
        
        #Set up the player
        self.player = Player()

        self.aiPos = None


        #Set up the frame for text at beginning and end of zone
        #----------------------------------------------------------------------
        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.zoneImage = DirectFrame()
        self.zoneImage.reparentTo(aspect2d)
        self.zoneImage.setScale(2)
        self.zoneImage.setTransparency(TransparencyAttrib.MAlpha)
        self.zoneText1 = OnscreenText(text = 'Chapter 2',
                                    fg = (1, 1, 1, 1),
                                    font = self.menuFont)
        self.zoneText1.reparentTo(self.zoneImage)
        self.zoneText1.setTransparency(TransparencyAttrib.MAlpha)
        self.zoneText2 = OnscreenText(text = 'Unpleasant Surprises',
                                 pos = (0, -.1),
                                 fg = (1, 1, 1, 1),
                                 font = self.menuFont)
        self.zoneText2.reparentTo(self.zoneImage)
        self.zoneText2.setTransparency(TransparencyAttrib.MAlpha)
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
        self.objectiveText2 = OnscreenText(text = 'Stay close to the pod',
                                            mayChange = 1,
                                            scale = .05,
                                            fg = (1, 1, 1, 1),
                                            pos = (-.5, .45, 0))
        self.objectiveText2.reparentTo(self.objectiveTextNode)
        self.objectiveTextNode.setTransparency(TransparencyAttrib.MAlpha)
        self.objectiveText2.setTransparency(TransparencyAttrib.MAlpha)
        self.objectiveTextNode.hide()
        #----------------------------------------------------------------------

        #Load the skybox
        #----------------------------------------------------------------------
        self.zoneTwo = render.attachNewNode('Zone Two')
        self.skybox = loader.loadModel("Art/skybox_mission2.bam")
        self.skybox.reparentTo(self.zoneTwo)
        self.skybox.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.skybox.setScale(6000)
        self.endNode = self.skybox.find('**/endNode')

        self.pod = Pod(self.skybox.find('**/startNode').getPos(render) + Point3(20, 50, 0))
        self.podNode = render.find('**/Pod')
        self.podNode.lookAt(self.endNode)
        #----------------------------------------------------------------------

        #Load the capital ship models then hide them
        #----------------------------------------------------------------------
        self.endZoneShipNode = self.zoneTwo.attachNewNode('End Zone Ships')
        self.capShip = loader.loadModel('Art/cruiser_1.bam')
        self.capShip2 = loader.loadModel('Art/cruiser_2.bam')
        self.capShip2.setTransparency(TransparencyAttrib.MAlpha)
        self.capShip.setTransparency(TransparencyAttrib.MAlpha)
        #self.capShip2.setColor(1,1,1,0)
        for child in self.skybox.find("**/capShip1Locator").getChildrenAsList():
            placeholder = self.endZoneShipNode.attachNewNode("Capital Ship 1")
            placeholder.setPos(child.getPos(render))
            placeholder.setScale(7)
            self.capShip.instanceTo(placeholder)
            self.capShip.setScale(5)
            placeholder.lookAt(self.endNode)

        for child in self.skybox.find("**/capShip2Locator").getChildrenAsList():
            placeholder2 = self.endZoneShipNode.attachNewNode("Capital Ship 2")
            placeholder2.setPos(child.getPos(render))
            placeholder2.setScale(7)
            self.capShip2.instanceTo(placeholder2)
            self.capShip2.setScale(5)
            placeholder2.lookAt(self.endNode)
        self.endZoneShipNode.hide()
        #----------------------------------------------------------------------



        #Find the cockpit node and set its position for Humble Beginnings
        #----------------------------------------------------------------------
        self.cockpitNode = render.find('**/cockpit_2.egg')
        cockpitPos = (self.skybox.find('**/startNode').getPos(render))
        self.cockpitNode.setPos(cockpitPos)
        self.cockpitNode.lookAt(self.endNode)
        #----------------------------------------------------------------------

        #Start sequence and tasks
        #----------------------------------------------------------------------
        self.startZone()
        self.podSequence()
        taskMgr.doMethodLater(SPAWN_TIME, self.spawnAI, 'Spawn AI')
        taskMgr.doMethodLater(0.05, self.checkDistance, 'Check Distance')
        #----------------------------------------------------------------------

        #Spawn up some initial AI
        #----------------------------------------------------------------------
        vector = self.podNode.getQuat().getForward() * 500
        self.aiPos = Point3(vector[0], vector[1], vector[2])
        self.aiPos += self.podNode.getPos()
        AIPlayer("ben", "vulture", 'bad', self.aiPos + Point3(-20, -20, 0))
        AIPlayer("roger", "hawkeye", 'bad', self.aiPos + Point3(0, 50, -30))
        AIPlayer("roger", "hawkeye", 'bad', self.aiPos + Point3(20, 20, 30))
        AIPlayer("ben", "vulture", 'bad', self.aiPos + Point3(-50, 0, 20))
        #----------------------------------------------------------------------


    def podSequence(self):
        self.podSeq = Sequence()
        self.podSeq.append(LerpPosInterval(self.podNode,
                                            ZONE_TIME,
                                            self.endNode.getPos(render),
                                            self.podNode.getPos()))
        self.podSeq.append(Func(self.endZone))
        self.podSeq.append(Wait(6.5))
        self.podSeq.append(Func(messenger.send, 'gotonextzone'))
        self.podSeq.start()
        self.sequenceList.append(self.podSeq)

    def spawnAI(self, task):
        vector = self.podNode.getQuat().getForward() * 500
        self.aiPos = Point3(vector[0], vector[1], vector[2])
        self.aiPos += self.podNode.getPos()
        AIPlayer("ben", "vulture", 'bad', self.aiPos + Point3(-20, -20, 0))
        AIPlayer("ben", "hawkeye", 'bad', self.aiPos + Point3(0, 50, -30))
        AIPlayer("roger", "hawkeye", 'bad', self.aiPos + Point3(20, 20, 30))

        objectiveSeq = Sequence(Func(self.objectiveTextNode.show),
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
        objectiveSeq.start()
        self.sequenceList.append(objectiveSeq)
        return task.again

    def checkDistance(self, task):
        if not self.podNode.getDistance(self.cockpitNode) <= 500:
            messenger.send('missionfailedmenu', ['Too far from Pod'])

        else:
            return task.again

    def podDied(self):
        messenger.send('missionfailedmenu', ['The Pod died'])
        self.podSeq.pause()

    def startZone(self):
        #Set up frame for start sequence
        #----------------------------------------------------------------------
        self.zoneImage.show()

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
        self.sequenceList.append(zoneSeq)
        #----------------------------------------------------------------------

    def endZone(self):
        self.endImage.show()
        self.zoneSeq = Sequence(LerpColorInterval(self.endImage,
                                4,
                                Vec4(0, 0, 0, 1),
                                Vec4(0, 0, 0, 0)))
        self.zoneSeq.start()
        self.sequenceList.append(self.zoneSeq)

        self.zoneCompleted = True

    def cleanUp(self):
        print "ZONE TWO CLEANUP", ZoneTwo.UID

        taskMgr.remove('Spawn AI')
        taskMgr.remove('Check Distance')

        for seq in self.sequenceList:
            seq.pause()
            del seq
        del self.sequenceList



        self.endZoneShipNode.removeNode()
        self.cockpitNode.removeNode()
        self.zoneTwo.removeNode()
        self.zoneImage.destroy()
        self.endImage.destroy()
        self.objectiveTextNode.removeNode()


        self.pod.cleanUp()
        del self.pod

        self.player.cleanUp()
        del self.player
