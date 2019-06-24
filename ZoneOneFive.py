from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.fsm import FSM
from direct.task import Task
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *


from CometImmobile import *
from Pod import *
from Player import *

import config


class ZoneOneFive(DirectObject.DirectObject):
    def __init__(self):
        #Set up a list of sequences to make sure we finish them all
        #and delete accordingly
        self.sequenceList = []
        self.exhaustList = []
        


        #sound
        messenger.send("addVoice", ["mission1-10","Art/audio/chapter1/Clip 10.mp3"])
        messenger.send("addSfx", ["mission1-bg","Art/audio/chapter1/Open Space Drone.mp3"])

        self.bgSeq = Sequence()
        self.bgSeq.append(Func(messenger.send, 'playSfx', ['mission1-bg']))
        self.bgSeq.append(Wait(140.0))
        self.bgSeq.loop()
        self.sequenceList.append(self.bgSeq)

        #Load the zone and stretch it from the unit circle
        #----------------------------------------------------------------------
        self.zoneOneFiveLocations = loader.loadModel('Art/zoneOneFive.bam')
        self.zoneOneFiveLocations.reparentTo(render)
        for child in self.zoneOneFiveLocations.find('**/zoneOneFiveNode').getChildrenAsList():
            child.setPos(child.getPos() * 70)
        #----------------------------------------------------------------------
        
        #Set up the frame for text at beginning and end of zone
        #----------------------------------------------------------------------
        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.zoneImage = DirectFrame(image = 'Art/textures/gamemenu_bg.png',
                                        frameColor = (0, 0, 0, 1))
        self.zoneImage.reparentTo(aspect2d)
        self.zoneImage.setScale(.01)
        self.zoneText1 = OnscreenText(text = 'End Chapter 1',
                                    fg = (1, 1, 1, 1),
                                    font = self.menuFont)
        self.zoneText1.reparentTo(self.zoneImage)
        self.zoneText2 = OnscreenText(text = 'Humble Beginnings',
                                 pos = (0, -.1),
                                 fg = (1, 1, 1, 1),
                                 font = self.menuFont)
        self.zoneText2.reparentTo(self.zoneImage)
        self.zoneImage.hide()
        #----------------------------------------------------------------------


        #Load the pegasus and position camera
        #----------------------------------------------------------------------
        base.camera.setPos(12.26, -25.41, 4.27)
        
        self.pegasus = loader.loadModel('Art/pegasus.bam')
        self.pegasus.reparentTo(self.zoneOneFiveLocations)
        pegasusPos = (self.zoneOneFiveLocations.find('**/pegasusNode').getPos())
        self.pegasus.setPos(pegasusPos + Vec3(0, -15, 0))
        self.pegasus.setScale(2)
        for exhaust in self.pegasus.find('**/engines').getChildrenAsList():
            x = Exhaust(exhaust, 1)
            x.myNode.setH(180)
            x.myNode.setPos(0, -1, 0)
            self.exhaustList.append(x)
        self.pegasus.find('**/engines').hide()
        self.pegasus.find('**/windows').setColor(0, 0, 0, 1)
        #----------------------------------------------------------------------

        #Load the skybox, pod and the portal
        #----------------------------------------------------------------------
        self.skybox = loader.loadModel("Art/skybox_mission1.bam")
        self.skybox.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.skybox.reparentTo(self.zoneOneFiveLocations)
        self.skybox.setScale(6000)
        self.skybox.setPos(0,0,0)

##        self.pod = loader.loadModel('Art/pod3.bam')
##        #self.pod.reparentTo(self.zoneOneFiveLocations.find('**/podNode'))
##        self.pod.reparentTo(render)
##        self.pod.setPos(self.zoneOneFiveLocations.find('**/podNode').getPos(render))
##        self.pod.setScale(.5)
##        for exhaust in self.pod.find('**/locators').getChildrenAsList():
##            x = Exhaust(exhaust, 1.2)
##            self.exhaustList.append(x)

        self.portal = loader.loadModel("Art/mission1_portal.bam")
        self.portalNode = self.zoneOneFiveLocations.find('**/portalNode')
        #self.portalNode.setPos(self.portalNode.getPos())
        self.portal.reparentTo(self.portalNode)
        self.portal.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        vec = self.portal.getQuat().getForward() * 100
        self.portal.setPos(self.portal, Point3(vec[0], vec[1], vec[2]))
        self.portal.setScale(7)
        base.camera.lookAt(self.portal)
        self.pegasus.lookAt(self.portal)
        #self.portalSeq = Sequence()

        self.textureList = []
        for x in range(30,60):
            self.textureList.append(loader.loadTexture("Art/textures/portalsprite/portal00" + str(x) +".png" ))

        self.portalSwirl = self.portal.find("**/portal")
        self.portalSwirl.setTexture(self.textureList[0], 1)
        self.currentAnim = 0
        self.animDir = 1
        taskMgr.doMethodLater(.05, self.animFunc, 'portalAnim')
        self.portalSwirl.setDepthWrite(False)
        self.portalSwirl.setBin("fixed",2)
        self.portalSwirl.setScale(1.4)
        #self.portalSeq.append(LerpHprInterval(self.portal.find('**/portal'), 9, Vec3(0,0,360), Vec3(0,0,0)))
        #self.portalSeq.loop()
        #----------------------------------------------------------------------
       
        self.scene()

    def scene(self):
        sceneSequence = Sequence(Func(messenger.send, 'playVoice', ['mission1-10']))
        sceneSequence.append(Wait(3))
        sceneSequence.append(Func(self.pegasus.find('**/engines').show))
        sceneSequence.append(LerpPosInterval(self.pegasus,
                                                4,
                                                self.portal.getPos(render),
                                                self.pegasus.getPos()))
        sceneSequence.append(Func(self.pegasus.hide))
        sceneSequence.append(Func(self.zoneImage.show))
        sceneSequence.append(LerpScaleInterval(self.zoneImage,
                                6.0, 2.0, .01))
        sceneSequence.append(Wait(1.0))
        sceneSequence.append(Func(messenger.send, 'gotonextzone'))
        sceneSequence.start()
        self.sequenceList.append(sceneSequence)
    
    def animFunc(self, task):
        if self.animDir == 1:
            self.currentAnim += 1
            if self.currentAnim >= 30:
                self.currentAnim -= 1
                self.animDir = 2
        else:
            self.currentAnim -= 1
            if self.currentAnim <= -1:
                self.currentAnim += 1
                self.animDir = 1
        self.portalSwirl.setTexture(self.textureList[self.currentAnim], 1)
        return task.again


    def cleanUp(self):
        print "ZONE ONE CLEANUP"
        for seq in self.sequenceList:
            seq.pause()
            del seq
        del self.sequenceList


        messenger.send("stopVoice")
        messenger.send("stopSfx")

        #self.cockpitNode.reparentTo(render)
        self.zoneOneFiveLocations.removeNode()
        self.portalNode.removeNode()
        if self.zoneImage:
            self.zoneImage.destroy()
        self.zoneImage.removeNode()
##        self.pod.removeNode()

        for exhaust in self.exhaustList:
            exhaust.cleanUp()

        taskMgr.remove('portalAnim')

        for child in render.find('**/other').getChildrenAsList():
            child.removeNode()
        #for child in self.cockpitNode.find('**/collisions').getChildrenAsList():
        #    base.cTrav.addCollider(child, config.collisionHandler)
