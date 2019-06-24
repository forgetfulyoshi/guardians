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


class ZoneOneFSM(DirectObject.DirectObject, FSM.FSM):
    def __init__(self):
        FSM.FSM.__init__(self, 'zoneOneFSM')
        #Set up a list of sequences to make sure we finish them all
        #and delete accordingly
        self.sequenceList = []
        self.accept('poddied', self.podDied)
        
        
        #Set up the player
        self.player = Player()

        #Flag to test for zone completion
        self.zoneCompleted = False

        #sound
        messenger.send("addVoice", [ "mission1-1","Art/audio/chapter1/Clip 01.mp3"])
        messenger.send("addVoice", ["mission1-2","Art/audio/chapter1/Clip 02.mp3"])
        messenger.send("addVoice", ["mission1-3","Art/audio/chapter1/Clip 03.mp3"])
        messenger.send("addVoice", ["mission1-4","Art/audio/chapter1/Clip 04.mp3"])
        messenger.send("addVoice", ["mission1-5","Art/audio/chapter1/Clip 05.mp3"])
        messenger.send("addVoice", ["mission1-6","Art/audio/chapter1/Clip 06.mp3"])
        messenger.send("addVoice", ["mission1-7","Art/audio/chapter1/Clip 07.mp3"])
        messenger.send("addVoice", ["mission1-8","Art/audio/chapter1/Clip 08.mp3"])
        messenger.send("addVoice", ["mission1-9","Art/audio/chapter1/Clip 09.mp3"])
        messenger.send("addVoice", ["mission1-10","Art/audio/chapter1/Clip 10.mp3"])

        messenger.send("addSfx", ["mission1-int1","Art/audio/chapter1/AC Interior.mp3"])
        messenger.send("addSfx", ["mission1-int2","Art/audio/chapter1/Ac Interior 2.mp3"])
        messenger.send("addSfx", ["mission1-bg","Art/audio/chapter1/Open Space Drone.mp3"])

        self.interiorSeq1 = Sequence()
        self.interiorSeq1.append(Func(messenger.send, 'playSfx', ['mission1-int1']))
        self.interiorSeq1.append(Wait(52.0))
        self.interiorSeq1.loop()
        self.sequenceList.append(self.interiorSeq1)

        self.interiorSeq2 = Sequence()
        self.interiorSeq2.append(Func(messenger.send, 'playSfx', ['mission1-int2']))
        self.interiorSeq2.append(Wait(130.0))
        self.interiorSeq2.loop()
        self.sequenceList.append(self.interiorSeq2)

        self.bgSeq = Sequence()
        self.bgSeq.append(Func(messenger.send, 'playSfx', ['mission1-bg']))
        self.bgSeq.append(Wait(140.0))
        self.bgSeq.loop()
        self.sequenceList.append(self.bgSeq)



        self.ringCount = 0
        self.currentRing = 0
        self.currentRingNode = None
        self.EarthNode = render.attachNewNode("EarthNode")

        #Load the zone and stretch it from the unit circle
        #----------------------------------------------------------------------
        self.zoneOneLocations = loader.loadModel('Art/zones/zoneOne.egg')
        self.zoneOneLocations.reparentTo(render)
        for child in self.zoneOneLocations.find('**/zoneOneNode').getChildrenAsList():
            child.setPos(child.getPos() * 100)
        #----------------------------------------------------------------------

        #Set up the frame for text at beginning and end of zone
        #----------------------------------------------------------------------
        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.zoneImage = DirectFrame()
        self.zoneImage.reparentTo(aspect2d)
        self.zoneImage.setScale(2)
        self.zoneText1 = OnscreenText(text = 'Chapter 1',
                                    mayChange = 1,
                                    fg = (1, 1, 1, 1),
                                    font = self.menuFont)
        self.zoneText1.reparentTo(self.zoneImage)
        self.zoneText2 = OnscreenText(text = 'Humble Beginnings',
                                 pos = (0, -.1),
                                 mayChange = 1,
                                 fg = (1, 1, 1, 1),
                                 font = self.menuFont)
        self.zoneText2.reparentTo(self.zoneImage)
        self.zoneImage.setTransparency(TransparencyAttrib.MAlpha)
        self.zoneText1.setTransparency(TransparencyAttrib.MAlpha)
        self.zoneText2.setTransparency(TransparencyAttrib.MAlpha)
        self.zoneImage.hide()
        
        self.endImage = OnscreenImage(image = 'Art/textures/mission3_plane.png',
                                        scale = 2,
                                        color = (0, 0, 0, 0))
        self.endImage.reparentTo(aspect2d)
        self.endImage.setTransparency(TransparencyAttrib.MAlpha)
        self.endImage.hide()
        #----------------------------------------------------------------------
        
        #Set up the voice text
        #----------------------------------------------------------------------
        self.voiceTextNode = aspect2d.attachNewNode('Voice Text')
        self.voiceText1 = OnscreenText(text = "Fly through the rings",
                                        mayChange = 1,
                                        scale = .05,
                                        fg = (1, 1, 1, 1),
                                        pos = (-.5, .5, 0))
        self.voiceText2 = OnscreenText(text = "Press the '1' - '9' keys to set",
                                        mayChange = 1,
                                        scale = .05,
                                        fg = (1, 1, 1, 1),
                                        pos = (-.5, .45, 0))
        self.voiceText3 = OnscreenText(text = "the speed of your ship",
                                        mayChange = 1,
                                        scale = .05,
                                        fg = (1, 1, 1, 1),
                                        pos = (-.5, .4, 0))
        self.voiceText4 = OnscreenText(mayChange = 1,
                                        scale = .05,
                                        fg = (1, 1, 1, 1),
                                        pos = (-.5, .35, 0))
        self.voiceText5 = OnscreenText(mayChange = 1,
                                        scale = .05,
                                        fg = (1, 1, 1, 1),
                                        pos = (-.5, .3, 0))
        self.voiceText1.reparentTo(self.voiceTextNode)
        self.voiceText2.reparentTo(self.voiceTextNode)
        self.voiceText3.reparentTo(self.voiceTextNode)
        self.voiceText4.reparentTo(self.voiceTextNode)
        self.voiceText5.reparentTo(self.voiceTextNode)
        self.voiceText1.setTransparency(TransparencyAttrib.MAlpha)
        self.voiceText2.setTransparency(TransparencyAttrib.MAlpha)
        self.voiceText3.setTransparency(TransparencyAttrib.MAlpha)
        self.voiceText4.setTransparency(TransparencyAttrib.MAlpha)
        self.voiceText5.setTransparency(TransparencyAttrib.MAlpha)
        
        self.voiceTextNode.hide()
        #----------------------------------------------------------------------


        #Find the cockpit node and set its position for Humble Beginnings
        #----------------------------------------------------------------------
        self.cockpitNode = render.find('**/cockpit_2.egg')
        self.cockpitNode.reparentTo(self.zoneOneLocations)
        cockpitPos = (self.zoneOneLocations.find('**/shipNode').getPos())
        self.cockpitNode.setPos(cockpitPos)
        #----------------------------------------------------------------------

        #Load the skybox, pod and the portal
        #----------------------------------------------------------------------
        self.skybox = loader.loadModel("Art/skybox_mission1.bam")
        self.skybox.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        self.skybox.reparentTo(self.EarthNode)
        self.skybox.setScale(6000)
        self.skybox.setPos(0,0,0)

        self.pod = Pod(self.zoneOneLocations.find('**/podNode').getPos())
        self.podNode = render.find('**/Pod')
        self.podNode.find('**/locators').hide()

        self.portal = loader.loadModel("Art/mission1_portal.bam")
        self.portalNode = self.zoneOneLocations.find('**/portalNode')
        #self.portalNode.setPos(self.portalNode.getPos())
        self.portal.reparentTo(self.portalNode)
        self.portal.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        vec = self.portal.getQuat().getForward() * 500
        self.portal.setPos(self.portal, Point3(vec[0], vec[1], vec[2]))
        self.portal.setScale(5)
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


        #Setup collision stuffs
        #----------------------------------------------------------------------
        #Remove the cockpit collision nodes from the collision dispatcher
        self.cockpitColNode = self.cockpitNode.find('**/collisions')
        #This is some REALLY hacky code ...
        #But whatever its here now.
        #even though you remove them from the other traverser they will be
        # into nodes.

        for child in self.cockpitColNode.getChildrenAsList():
            base.cTrav.removeCollider(child)
        #base.cTrav.removeCollider(self.cockpitNode.find('cnode'))
        #Got to re attach these at the end or crap will hit fan
        self.retardedIdeaNodeParent = self.cockpitColNode.getParent()
        self.retardedIdeaNode = self.cockpitColNode
        self.cockpitColNode.detachNode()

        self.cockpitColNode = self.retardedIdeaNodeParent.attachNewNode("tempCockpitColNode")

        self.cs = CollisionSphere(0, 0, 0, .2)
        self.cockpitColNode1 = self.cockpitNode.attachNewNode(CollisionNode('cNode'))
        self.cockpitColNode1.node().addSolid(self.cs)
        #self.cockpitColNode1.show()

        self.colHandler = CollisionHandlerEvent()
        self.colHandler.addOutPattern('into')
        self.accept('into', self.into)


        self.traverser = CollisionTraverser('zoneOneTraverser')
        self.traverser.addCollider(self.cockpitColNode1, self.colHandler)
        self.traverser.traverse(self.zoneOneLocations)
        taskMgr.add(self.traverse, 'Traverse Zone One')
        taskMgr.add(self.pointArrow, 'Arrow Pointer')
        taskMgr.add(self.checkDistance, 'Check Distance')



        self.arrow = loader.loadModel("Art/arrow.bam")
        self.arrow.reparentTo(self.cockpitNode)
        self.arrow.setPos(0,-.3,1)
        self.arrow.setHpr(0,0,0)
        self.arrow.setScale(.02)
        self.arrow.setColor(.93,0,0,1)
        #plight = PointLight('plight')
        #plight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        #plnp = self.cockpitNode.attachNewNode(plight)
        #plnp.setPos(0,-.1,1.2)
        #plnp.setPos(10, 20, 0)
        #self.arrow.setLight(plnp)
        #----------------------------------------------------------------------


        #Start the FSM
        self.request('Stabilized')

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

    def into(self, collisionEntry):
        print "reallybadcode"
        fromNode = collisionEntry.getFromNodePath()
        intoNode = collisionEntry.getIntoNodePath()
        if intoNode.getNetTag("type") == "rings-stabilized":
            print intoNode.getNetTag("num"), "  ", self.currentRing + 1
            if intoNode.getNetTag("num") == str(self.currentRing+1):
                self.ringCount += 1
                self.currentRing += 1
                if self.ringCount < 4:
                    intoNode.getParent().hide()
                    self.currentRingNode = self.ringList[self.ringCount]
                if self.ringCount >= 4:
                    self.ringCount = 0
                    self.currentRing = 0
                    self.request('Inertial')
                    return
        if intoNode.getNetTag("type") == "rings-inertial":
            print intoNode.getNetTag("num"), "  ", self.currentRing + 1
            if intoNode.getNetTag("num") == str(self.currentRing+5):
                self.ringCount += 1
                self.currentRing += 1
                if self.ringCount < 4:
                    intoNode.getParent().hide()
                    self.currentRingNode = self.ringList[self.ringCount]
                if self.ringCount >= 4:
                    self.ringCount = 0
                    self.request('Pod')
                    return

        #print fromNode
        #print intoNode, "\n\n"

    def enterWelcome(self):


        self.request('Stabilized')
    def exitWelcome(self):
        pass

    def enterStabilized(self):
        #Play the sequence to show chapter
        self.startZone()

        #Create rings and make them billboards
        #----------------------------------------------------------------------
        #copy pasting code makes me sad! - Roger
        #me too. -AJ
        self.ringOne = OnscreenImage('Art/textures/tutorial_ring.png')
        self.ringOne.setTransparency(TransparencyAttrib.MAlpha)
        self.ringOne.reparentTo(self.zoneOneLocations.find('**/ringOneNode'))
        self.ringOne.setBillboardPointEye()

        self.ringTwo = OnscreenImage('Art/textures/tutorial_ring.png')
        self.ringTwo.setTransparency(TransparencyAttrib.MAlpha)
        self.ringTwo.reparentTo(self.zoneOneLocations.find('**/ringTwoNode'))
        self.ringTwo.setBillboardPointEye()

        self.ringThree = OnscreenImage('Art/textures/tutorial_ring.png')
        self.ringThree.setTransparency(TransparencyAttrib.MAlpha)
        self.ringThree.reparentTo(self.zoneOneLocations.find('**/ringThreeNode'))
        self.ringThree.setBillboardPointEye()

        self.ringFour = OnscreenImage('Art/textures/tutorial_ring.png')
        self.ringFour.setTransparency(TransparencyAttrib.MAlpha)
        self.ringFour.reparentTo(self.zoneOneLocations.find('**/ringFourNode'))
        self.ringFour.setBillboardPointEye()

        self.ringList = [self.ringOne, self.ringTwo, self.ringThree, self.ringFour]

        self.currentRingNode = self.ringOne
        #----------------------------------------------------------------------

        #Setup collision spheres for rings
        #----------------------------------------------------------------------
        ringOneCSNode = self.zoneOneLocations.find('**/ringOneNode').attachNewNode(
                                                                        CollisionNode('ring'))
        ringOneCSNode.setTag("num", "1")
        self.cs = CollisionSphere(0, 0, 0, 1)
        ringOneCSNode.node().addSolid(self.cs)
        self.zoneOneLocations.setTag("type", "rings-stabilized")
        #ringOneCSNode.show()

        self.cs = CollisionSphere(0, 0, 0, 1)
        ringTwoCSNode = self.zoneOneLocations.find('**/ringTwoNode').attachNewNode(
                                                                        CollisionNode('ring'))
        ringTwoCSNode.setTag("num", "2")
        ringTwoCSNode.node().addSolid(self.cs)

        self.cs = CollisionSphere(0, 0, 0, 1)
        ringThreeCSNode = self.zoneOneLocations.find('**/ringThreeNode').attachNewNode(
                                                                        CollisionNode('ring'))
        ringThreeCSNode.setTag("num", "3")
        ringThreeCSNode.node().addSolid(self.cs)

        self.cs = CollisionSphere(0, 0, 0, 1)
        ringFourCSNode = self.zoneOneLocations.find('**/ringFourNode').attachNewNode(
                                                                        CollisionNode('ring'))
        ringFourCSNode.setTag("num", "4")
        ringFourCSNode.node().addSolid(self.cs)
        #----------------------------------------------------------------------

        self.voiceSeq = Sequence()
        self.voiceSeq.append(Func(messenger.send, 'playVoice', ['mission1-1']))
        self.voiceSeq.append(Wait(13))
        self.voiceSeq.append(Func(messenger.send, 'playVoice', ['mission1-2']))
        self.voiceSeq.append(Wait(9))
        self.voiceSeq.append(Parallel(Sequence(Func(self.voiceTextNode.show),
                                                LerpColorScaleInterval(self.voiceTextNode,
                                                                    2.0,
                                                                    Vec4(1, 1, 1, 1),
                                                                    Vec4(1, 1, 1, 0)),
                                                Wait(14),
                                                LerpColorScaleInterval(self.voiceTextNode,
                                                                    2.0,
                                                                    Vec4(1, 1, 1, 0),
                                                                    Vec4(1, 1, 1, 1)),
                                                Func(self.voiceTextNode.hide)),
                                       Func(messenger.send, 'playVoice', ['mission1-3'])))
        self.voiceSeq.start()
        self.sequenceList.append(self.voiceSeq)

    def exitStabilized(self):
        self.ringOne.removeNode()
        self.ringTwo.removeNode()
        self.ringThree.removeNode()
        self.ringFour.removeNode()
        self.voiceSeq.pause()

    def enterInertial(self):
        #Create rings and make them billboards
        #----------------------------------------------------------------------
        self.ringFive = OnscreenImage('Art/textures/tutorial_ring.png')
        self.ringFive.setTransparency(TransparencyAttrib.MAlpha)
        self.ringFive.reparentTo(self.zoneOneLocations.find('**/ringFiveNode'))
        self.ringFive.setBillboardPointEye()

        self.ringSix = OnscreenImage('Art/textures/tutorial_ring.png')
        self.ringSix.setTransparency(TransparencyAttrib.MAlpha)
        self.ringSix.reparentTo(self.zoneOneLocations.find('**/ringSixNode'))
        self.ringSix.setBillboardPointEye()

        self.ringSeven = OnscreenImage('Art/textures/tutorial_ring.png')
        self.ringSeven.setTransparency(TransparencyAttrib.MAlpha)
        self.ringSeven.reparentTo(self.zoneOneLocations.find('**/ringSevenNode'))
        self.ringSeven.setBillboardPointEye()

        self.ringEight = OnscreenImage('Art/textures/tutorial_ring.png')
        self.ringEight.setTransparency(TransparencyAttrib.MAlpha)
        self.ringEight.reparentTo(self.zoneOneLocations.find('**/ringEightNode'))
        self.ringEight.setBillboardPointEye()

        self.currentRingNode = self.ringFive

        self.ringList = [self.ringFive, self.ringSix, self.ringSeven, self.ringEight]

        ringFiveCSNode = self.zoneOneLocations.find('**/ringFiveNode').attachNewNode(
                                                                        CollisionNode('ring'))
        ringFiveCSNode.setTag("num", "5")
        self.cs = CollisionSphere(0, 0, 0, 1)
        ringFiveCSNode.node().addSolid(self.cs)
        self.zoneOneLocations.setTag("type", "rings-inertial")
        #ringOneCSNode.show()

        self.cs = CollisionSphere(0, 0, 0, 1)
        ringSixCSNode = self.zoneOneLocations.find('**/ringSixNode').attachNewNode(
                                                                        CollisionNode('ring'))
        ringSixCSNode.setTag("num", "6")
        ringSixCSNode.node().addSolid(self.cs)

        self.cs = CollisionSphere(0, 0, 0, 1)
        ringSevenCSNode = self.zoneOneLocations.find('**/ringSevenNode').attachNewNode(
                                                                        CollisionNode('ring'))
        ringSevenCSNode.setTag("num", "7")
        ringSevenCSNode.node().addSolid(self.cs)

        self.cs = CollisionSphere(0, 0, 0, 1)
        self.ringEightCSNode = self.zoneOneLocations.find('**/ringEightNode').attachNewNode(
                                                                        CollisionNode('ring'))
        self.ringEightCSNode.setTag("num", "8")
        self.ringEightCSNode.node().addSolid(self.cs)
        #----------------------------------------------------------------------

        self.voiceText2['text'] = "Press the 'i' key to switch"
        self.voiceText3['text'] = "to inertial mode"
        self.voiceText4['text'] = "Press the space bar to"
        self.voiceText5['text'] = "engage the thrusters"

        self.voiceSeq = Sequence()
        self.voiceSeq.append(Func(messenger.send, 'playVoice', ['mission1-4']))
        self.voiceSeq.append(Wait(18.5))
        self.voiceSeq.append(Parallel(Sequence(Func(self.voiceTextNode.show),
                                                LerpColorScaleInterval(self.voiceTextNode,
                                                                    2.0,
                                                                    Vec4(1, 1, 1, 1),
                                                                    Vec4(1, 1, 1, 0)),
                                                Wait(10),
                                                LerpColorScaleInterval(self.voiceTextNode,
                                                                    2.0,
                                                                    Vec4(1, 1, 1, 0),
                                                                    Vec4(1, 1, 1, 1)),
                                                Func(self.voiceTextNode.hide)),
                                        Func(messenger.send, 'playVoice', ['mission1-5'])))
        self.voiceSeq.start()
        self.sequenceList.append(self.voiceSeq)

    def exitInertial(self):
        self.ringFive.removeNode()
        self.ringSix.removeNode()
        self.ringSeven.removeNode()
        self.ringEight.removeNode()
        self.ringEightCSNode.removeNode()
        self.currentRingNode = self.cockpitNode
        self.cockpitColNode1.removeNode()
        self.voiceSeq.pause()

    def enterPod(self):
        taskMgr.remove('Traverse Zone One')
        self.currentRingNode = self.podNode
        self.retardedIdeaNode.reparentTo(self.retardedIdeaNodeParent)
        for child in self.retardedIdeaNode.getChildrenAsList():
            base.cTrav.addCollider(child, config.collisionHandler)

        self.podNode.find('**/locators').show()

        #Spawn the comets procedurally
        #----------------------------------------------------------------------
        for x in range(1,5):
            self.podNode.lookAt(self.portal)
            vector = self.podNode.getQuat().getForward()
            vector = vector * ( x * 100 )
            cometPos = Point3(vector[0],vector[1],vector[2])
            cometPos = cometPos + self.podNode.getPos()
            comet = CometImmobile(cometPos)
        for x in range(1,9):
            cometPos = Point3(self.podNode.getX() + randint(-50, 50),
                                self.podNode.getY() + randint(50, 400),
                                self.podNode.getZ() + randint(-50, 50))
            comet = CometImmobile(cometPos)
        #----------------------------------------------------------------------

        #Send the pod to the comets
        #----------------------------------------------------------------------
        self.podSequence = Sequence()
        self.podSequence.append(Wait(25))
        self.podSequence.append(LerpPosInterval(self.podNode,
                                            200,
                                            self.portal.getPos(render),
                                            self.podNode.getPos(),
                                            ))
        self.podSequence.append(Func(self.podNode.hide))
        self.podSequence.append(Func(self.endZone))
        self.podSequence.append(Wait(6.0))
        self.podSequence.append(Func(messenger.send, 'gotonextzone'))
        self.podSequence.start()
        self.sequenceList.append(self.podSequence)
        #----------------------------------------------------------------------

        self.voiceText1['text'] = "Clear the pods path"
        self.voiceText2['text'] = "Fire your bullets with the"
        self.voiceText3['text'] = "left mouse button"
        self.voiceText4['text'] = ""
        self.voiceText5['text'] = ""
        
        self.voiceSeq = Sequence()
        self.voiceSeq.append(Func(messenger.send, 'playVoice', ['mission1-6']))
        self.voiceSeq.append(Wait(10.5))
        self.voiceSeq.append(Func(messenger.send, 'playVoice', ['mission1-7']))
        self.voiceSeq.append(Wait(6.5))
        self.voiceSeq.append(Func(messenger.send, 'playVoice', ['mission1-8']))
        self.voiceSeq.append(Wait(14.5))
        self.voiceSeq.append(Parallel(Sequence(Func(self.voiceTextNode.show),
                                                LerpColorScaleInterval(self.voiceTextNode,
                                                                    2.0,
                                                                    Vec4(1, 1, 1, 1),
                                                                    Vec4(1, 1, 1, 0)),
                                                Wait(18),
                                                LerpColorScaleInterval(self.voiceTextNode,
                                                                    2.0,
                                                                    Vec4(1, 1, 1, 0),
                                                                    Vec4(1, 1, 1, 1)),
                                                Func(self.voiceTextNode.hide)),
                                        Func(messenger.send, 'playVoice', ['mission1-9'])))
        #self.voiceSeq.append(Wait(17))
        #self.voiceSeq.append(Func(messenger.send, 'playVoice', ['mission1-10']))
        self.voiceSeq.start()
        self.sequenceList.append(self.voiceSeq)

    def exitPod(self):
        pass

    def throughRing(self, entry):
        print "Through Ring"

    def traverse(self, task):
        self.traverser.traverse(self.zoneOneLocations)
        return task.cont

    def pointArrow(self, task):
        self.arrow.lookAt(self.currentRingNode)
        return task.cont

    def checkDistance(self, task):
        if not render.getDistance(self.cockpitNode) <= 3000:
            messenger.send('missionfailedmenu', ['Outside boundaries'])
        else:
            return task.cont

    def startZone(self):
        #Zoom In Sequence
        #----------------------------------------------------------------------
        self.zoneImage.show()
        self.zoneSeq = Sequence(LerpScaleInterval(self.zoneImage,
                                    6.0, 2, .01))
        self.zoneSeq.append(Func(self.zoneImage.hide))
        self.zoneSeq.start()
        self.sequenceList.append(self.zoneSeq)
        #----------------------------------------------------------------------

    def endZone(self):
        self.endImage.show()
        self.zoneSeq = Sequence(LerpColorInterval(self.endImage,
                                4,
                                Vec4(0, 0, 0, 1),
                                Vec4(0, 0, 0, 0)))
        self.zoneSeq.start()
        self.sequenceList.append(self.zoneSeq)
        
    def podDied(self):
        messenger.send('missionfailedmenu', ['The Pod died'])
        self.podSequence.pause()


    def cleanUp(self):
        print "ZONE ONE CLEANUP"
        taskMgr.remove('Traverse Zone One')
        taskMgr.remove('Arrow Pointer')
        taskMgr.remove('Check Distance')
        
        self.ignoreAll()

        self.traverser.clearColliders()

        for seq in self.sequenceList:
            seq.pause()
            del seq
        del self.sequenceList

        self.player.cleanUp()
        del self.player

        self.pod.cleanUp()
        del self.pod

        messenger.send("stopVoice")
        messenger.send("stopSfx")

        #self.cockpitNode.reparentTo(render)
        self.cockpitNode.removeNode()
        self.zoneOneLocations.removeNode()
        self.EarthNode.removeNode()
        self.portalNode.removeNode()
        self.retardedIdeaNodeParent.removeNode()
        self.voiceTextNode.removeNode()



        taskMgr.remove('portalAnim')
        if self.zoneImage:
            self.zoneImage.destroy()
        self.zoneImage.removeNode()
        
        if self.endImage:
            self.endImage.destroy()
        self.endImage.removeNode()

        for child in render.find('**/other').getChildrenAsList():
            child.removeNode()
        #for child in self.cockpitNode.find('**/collisions').getChildrenAsList():
        #    base.cTrav.addCollider(child, config.collisionHandler)
