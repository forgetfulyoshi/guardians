#ZoneHandler.py
# The ZoneHandler will be responsible for loading the current zone graphicly
# and applying any and all graphic effects to it

import GameManager
from direct.fsm import FSM
from IntroMovie import *
from ZoneOne import *
from ZoneOneFive import *
from ZoneTwo import *
from ZoneTwoFive import *
from ZoneThree import *
#from CutSceneMovie import *
from ZoneThree import *
from ZoneThreeFive import *
from ZoneFour import *
##from ZoneFive import *

from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.task import Task



from AIPlayer import *
""" SETUP THE FSM TO SUPPORT EVENTS TO CHANGE THE STATE FOR THE ZONELOADER! - complete
    SETUP A TEST OBJECT TO RUN THE ZoneHandler WITH TEXT OUTPUT TO TEST TRANSITION - complete
    ADD THE REST OF THE PLANETS - in progress
    ADD FUNCTIONALITY FOR THE RENDERABLE EFFECTS - in progress
    TEST CORE FUNCTIONALITY OF ZoneHandler             - complete"""
class ZoneHandler(DirectObject.DirectObject, FSM.FSM) :
    #Creates a Zone FSM
    def __init__( self, fileHandler ) :

        self.fileHandler = fileHandler

        FSM.FSM.__init__(self, 'zoneHandlerFSM')
        self.setStateArray(["IntroMovie",
                            "ZoneOne",
                            "ZoneOneFive",
                            "ZoneTwo",
                            "ZoneTwoFive",
                            "CutSceneMovie",
                            "ZoneThree",
                            "ZoneThreeFive",
                            "ZoneFour",
                            "ZoneFive"])
        #self.ZoneHandlerFSM = FSM()
        #self.FSMSetup()
        #self.zoneEventsSetup()
        self.offScreen = loader.loadModel('Art/solarsystem.bam')
        #Create a node for the AI to parent itself to
        self.aiNode = render.attachNewNode("ai")
        self.aiNode.setPos(0,0,0)
        self.aiGoodNode = self.aiNode.attachNewNode("good")
        self.aiGoodNode.setPos(0, 0, 0)
        self.aiBadNode = self.aiNode.attachNewNode("bad")
        self.aiBadNode.setPos(0, 0, 0)

        self.bulletNode = render.attachNewNode("bullets")
        self.bulletNode.setPos(0,0,0)
        self.bulletNode.setTag("bullet","bullet")

        self.missileNode = render.attachNewNode("missiles")
        self.missileNode.setPos(0,0,0)
        self.missileNode.setTag("missile","missile")

        self.otherNode = render.attachNewNode("other")
        self.otherNode.setPos(0,0,0)
        self.otherNode.setTag("other","other")

        self.accept('gotonextzone', self.requestNext)


    def enterIntroMovie( self ):
        print "ENTER INTRO MOVIE"
        self.introMovie = IntroMovie()

    def exitIntroMovie( self ):
        print "EXIT INTRO MOVIE"
        self.introMovie.cleanUp()
        del self.introMovie

    def enterZoneOne( self, *hacks ) :
        print "ENTER ZONE ONE"
        if int(self.fileHandler.getSlotData()[0]) < 1:
            self.fileHandler.modifyCurrentSlot(['1'])
        self.zoneOneFSM = ZoneOneFSM()
        #self.zoneOneFSM.request('Pod')

    def exitZoneOne( self ) :
        print 'EXITING ZONE ONE'
        self.zoneOneFSM.cleanUp()
        del self.zoneOneFSM

    def enterZoneOneFive( self, *hacks ):
        print "ENTER ZONE ONE FIVE"
        self.zoneOneFive = ZoneOneFive()

    def exitZoneOneFive( self ):
        self.zoneOneFive.cleanUp()
        del self.zoneOneFive

    def enterZoneTwo( self, *hacks ) :
        print 'ENTERING ZONE TWO'
        if int(self.fileHandler.getSlotData()[0]) < 2:
            self.fileHandler.modifyCurrentSlot(['2'])
        self.zoneTwo = ZoneTwo()

    def exitZoneTwo( self ) :
        print 'EXITING ZONE TWO'
        self.zoneTwo.cleanUp()
        del self.zoneTwo

    def enterZoneTwoFive( self, *hacks ):
        print 'ENTERING ZONE TWO FIVE'
        self.zoneTwoFive = ZoneTwoFive()

    def exitZoneTwoFive( self ):
        self.zoneTwoFive.cleanUp()
        del self.zoneTwoFive

    def enterCutSceneMovie( self, *hacks ):
        print "ENTERING CUT SCENE"
        self.cutSceneMovie = CutSceneMovie()

    def exitCutSceneMovie( self ):
        print "EXITING CUT SCENE"
        self.cutSceneMovie.cleanUp()
        del self.cutSceneMovie

    def enterZoneThree(self, *hacks):
        print "ENTERING ZONE THREE"
        if int(self.fileHandler.getSlotData()[0]) < 3:
            self.fileHandler.modifyCurrentSlot(['3'])
        self.zoneThree = ZoneThree()

    def exitZoneThree(self):
        print "EXITING ZONE THREE"
        self.zoneThree.cleanUp()
        del self.zoneThree

    def enterZoneThreeFive( self, *hacks ):
        print "ENTERING ZONE THREE FIVE"
        self.zoneThreeFive = ZoneThreeFive()

    def exitZoneThreeFive( self ):
        print "EXITING ZONE THREE FIVE"
        self.zoneThreeFive.cleanUp()
        del self.zoneThreeFive

    def enterZoneFour(self, *hacks):
        print "ENTERING ZONE FOUR"
        self.zoneFour = ZoneFour()

    def exitZoneFour(self):
        print "EXITING ZONE FOUR"
        self.zoneFour.cleanUp()
        del self.zoneFour

    def enterZoneFive(self, *hacks):
        self.zoneFive = ZoneFive()

    def exitZoneFive(self):
        self.zoneFive.cleanUp()
        del self.zoneFive
