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

class ZoneTwoFive(DirectObject.DirectObject):
    def __init__(self):
        self.exhaustList = []
        self.sequenceList = []
        
        #Set up the frame for text at beginning and end of zone
        #----------------------------------------------------------------------
        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.zoneImage = DirectFrame(image = 'Art/textures/gamemenu_bg.png',
                                        frameColor = (0, 0, 0, 1))
        self.zoneImage.reparentTo(aspect2d)
        self.zoneImage.setScale(.01)
        self.zoneImage.setTransparency(TransparencyAttrib.MAlpha)
        self.zoneText1 = OnscreenText(text = 'End Chapter 2',
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
        #----------------------------------------------------------------------
        
        #Load all the models and position the camera
        #----------------------------------------------------------------------
        self.zoneTwoFive = render.attachNewNode('Zone Two Five')
        self.skybox = loader.loadModel("Art/skybox_mission25.bam")
        self.skybox.reparentTo(self.zoneTwoFive)
        self.skybox.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.skybox.setScale(6000)
        
        cameraPos = self.skybox.find('**/endNode').getPos(render) + Point3(-10, -10, 10)
        base.camera.setPos(cameraPos)
        base.camera.lookAt(self.skybox.find('**/cameraLookAtNode'))
        
        self.pegasus = loader.loadModel('Art/pegasus.bam')
        self.pegasus.reparentTo(self.zoneTwoFive)
        self.pegasus.setPos(self.zoneTwoFive.find('**/endNode').getPos(render))
        self.pegasus.setScale(2)
        self.pegasus.lookAt(self.zoneTwoFive.find('**/cameraLookAtNode'))
        for exhaust in self.pegasus.find('**/engines').getChildrenAsList():
            x = Exhaust(exhaust, 1)
            x.myNode.setH(180)
            x.myNode.setPos(0, -1, 0)
            self.exhaustList.append(x)
        self.pegasus.find('**/engines').hide()
        self.pegasus.find('**/windows').setColor(0, 0, 0, 1)
        
        self.pod = loader.loadModel('Art/pod3.bam')
        self.pod.reparentTo(self.zoneTwoFive)
        self.pod.setPos(self.zoneTwoFive.find('**/endNode').getPos(render))
        self.pod.setScale(1)
        self.pod.lookAt(self.zoneTwoFive.find('**/cameraLookAtNode'))
        self.pod.setH(135)
        for exhaust in self.pod.find('**/locators').getChildrenAsList():
            x = Exhaust(exhaust, 1.2)
            self.exhaustList.append(x)
        #----------------------------------------------------------------------
        
        
        #Load the capital ship models then hide them
        #----------------------------------------------------------------------
        self.endZoneShipNode = self.zoneTwoFive.attachNewNode('End Zone Ships')
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
            placeholder.lookAt(self.zoneTwoFive.find('**/endNode'))
        for child in self.skybox.find("**/capShip2Locator").getChildrenAsList():
            placeholder2 = self.endZoneShipNode.attachNewNode("Capital Ship 2")
            placeholder2.setPos(child.getPos(render))
            placeholder2.setScale(7)
            self.capShip2.instanceTo(placeholder2)
            self.capShip2.setScale(5)
            placeholder2.lookAt(self.zoneTwoFive.find('**/endNode'))
        self.endZoneShipNode.hide()
        #----------------------------------------------------------------------
        
        self.scene()
      
    def scene(self):
        self.podLocation = self.skybox.find('**/cameraLookAtNode').getPos(render)
        self.pegasusLocation = self.skybox.find('**/endNode').getPos(render) + Point3(100, 100, 0)
        sceneSequence = Sequence(Parallel(LerpPosInterval(self.pod,
                                                    18,
                                                    self.podLocation,
                                                    self.pod.getPos(render)),
                                            Sequence(Wait(6),
                                                    LerpPosInterval(self.pegasus,
                                                                    12,
                                                                    self.pegasusLocation,
                                                                    self.pod.getPos(render))),
                                            Sequence(Wait(6),
                                                    Func(self.endZoneShipNode.show),
                                                    LerpColorInterval(self.endZoneShipNode,
                                                            12,
                                                            Vec4(1, 1, 1, 1),
                                                            Vec4(1, 1, 1, 0)))),
                                Func(self.zoneImage.show),
                                LerpScaleInterval(self.zoneImage,
                                                    6.0, 2.0, .01),
                                Func(messenger.send, 'gotonextzone'))
        sceneSequence.start()
        self.sequenceList.append(sceneSequence)
      
    def cleanUp(self):
        self.zoneTwoFive.removeNode()
        self.zoneImage.destroy()
        
        for exhaust in self.exhaustList:
            exhaust.cleanUp()
            del exhaust
        del self.exhaustList
        
        for seq in self.sequenceList:
            seq.pause()
            del seq
        del self.sequenceList