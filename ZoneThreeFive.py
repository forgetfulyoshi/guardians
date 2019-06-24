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

class ZoneThreeFive(DirectObject.DirectObject):
    def __init__(self):
        self.exhaustList = []
        self.sequenceList = []
        
        self.accept('c', self.printPos)
        
        #Set up the frame for text at beginning and end of zone
        #----------------------------------------------------------------------
        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.zoneImage = DirectFrame(image = 'Art/textures/gamemenu_bg.png',
                                        frameColor = (0, 0, 0, 1))
        self.zoneImage.reparentTo(aspect2d)
        self.zoneImage.setScale(.01)
        self.zoneImage.setTransparency(TransparencyAttrib.MAlpha)
        self.zoneText1 = OnscreenText(text = 'End Chapter 3',
                                    fg = (1, 1, 1, 1),
                                    font = self.menuFont)
        self.zoneText1.reparentTo(self.zoneImage)
        self.zoneText1.setTransparency(TransparencyAttrib.MAlpha)
        self.zoneText2 = OnscreenText(text = 'Strange Bedfellows',
                                 pos = (0, -.1),
                                 fg = (1, 1, 1, 1),
                                 font = self.menuFont)
        self.zoneText2.reparentTo(self.zoneImage)
        self.zoneText2.setTransparency(TransparencyAttrib.MAlpha)
        self.zoneImage.hide()
        #----------------------------------------------------------------------
        
        #Load all the models and position the camera
        #----------------------------------------------------------------------
        self.zoneThreeFive = render.attachNewNode("Zone Three Five")
        self.skybox = loader.loadModel('Art/skybox_mission35.bam')
        self.skybox.reparentTo(self.zoneThreeFive)
        self.skybox.setPos(0, 0, 0)
        self.skybox.setScale(6000)
        self.cameraPos = self.skybox.find('**/cameraNode').getPos(render)
        self.pegasusPos = self.skybox.find('**/endNode').getPos(render)
        self.pegasusEndPos = self.skybox.find('**/pegasusEndNode').getPos(render)
        self.comets = self.skybox.find('**/comets')
        
        base.camLens.setFov(50)
        base.camera.setPos(self.cameraPos + Point3(0, 0, 200))
        base.camera.lookAt(self.skybox.find('**/cameraLookAtNode'))
        
        self.pegasus = loader.loadModel('Art/pegasus.bam')
        self.pegasus.reparentTo(render.find('**/good'))
        self.pegasus.setPos(self.pegasusPos)
        self.pegasus.setScale(3)
        for exhaust in self.pegasus.find('**/engines').getChildrenAsList():
            x = Exhaust(exhaust, 1)
            x.myNode.setH(180)
            x.myNode.setPos(0, -1, 0)
            self.exhaustList.append(x)
        self.pegasus.find('**/engines').hide()
        self.pegasus.find('**/windows').setColor(0, 0, 0, 1)
        self.pegasus.lookAt(self.skybox.find('**/pegasusEndNode'))
        
        self.cometPos = self.zoneThreeFive.attachNewNode('Comet Positions')
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
        
        self.scene()
      
    def scene(self):
        sceneSequence = Sequence(Func(self.loadAI),
                                LerpPosInterval(self.pegasus,
                                                60,
                                                self.pegasusEndPos,
                                                self.pegasusPos),
                                Wait(60),
                                Func(self.zoneImage.show),
                                LerpScaleInterval(self.zoneImage,
                                                    6.0, 2.0, .01),
                                Func(messenger.send, 'gotonextzone'))
        sceneSequence.start()
        self.sequenceList.append(sceneSequence)
        
    def loadAI(self):
        for child in self.skybox.find('**/enemy').getChildrenAsList():
            AIPlayer("ben", "hawkeye", "bad", child.getPos(render))
        for child in self.skybox.find('**/guardians').getChildrenAsList():
            AIPlayer("roger", "pegasus-wings", "good", child.getPos(render))
            
    def printPos(self):
        print camera.getPos()
      
    def cleanUp(self):
        self.zoneThreeFive.removeNode()
        self.zoneImage.destroy()
        self.pegasus.removeNode()
        base.camLens.setFov(40)
        
        for exhaust in self.exhaustList:
            exhaust.cleanUp()
            del exhaust
        del self.exhaustList
        
        for seq in self.sequenceList:
            seq.pause()
            del seq
        del self.sequenceList