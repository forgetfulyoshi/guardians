#Cockpit.py
# Created - 11/24/2008
# Programmer - Eric Ranaldi, Roger Hughston
from direct.showbase import DirectObject
from pandac.PandaModules import *
import config
from direct.filter.CommonFilters import CommonFilters
from Explosion import *

class Cockpit(DirectObject.DirectObject) :
    isSet = False
    def __init__( self ) :
        
        self.accept('youdied', self.blowupSequence)
        self.accept('changecockpit', self.changeCockpit)
        self.shipBlowingUp = False
        
        self.cockpit = loader.loadModel("Art/cockpit_2.egg")
        self.cockpit.reparentTo(render.find("**/good"))

        self.pegasus = loader.loadModel("Art/pegasus.bam")
        self.pegasus.reparentTo(render)
        self.pegasus.setScale(3)
        self.pegasus.hide()
        self.pegasus.find('**/windows').setColor(0, 0, 0, 1)

        self.cockpit.setTag("type", "cockpit")
        self.cockpit.setTag("collisionType", "from")
        self.cockpit.setTwoSided(True)

        if Cockpit.isSet == False:
            print "SETTING UP FILTERS"
            if not (base.win.getGsg().getSupportsBasicShaders() == 0):
                if config.wantShaders:
                    self.filters = CommonFilters(base.win, base.cam)
                    self.filters.setBloom(blend=(1.0,0.0,0.0,0.0), mintrigger=0.9, desat=-0.5, intensity=2.0, size=1.0)
                    Cockpit.isSet = True
            else:
                print "GFX Card Error: Shaders not supported."


        colnode = self.cockpit.find("**/collisions")
        #colnode.ls()
        for x in colnode.getChildrenAsList():
            #x.show()
            base.cTrav.addCollider(x, config.collisionHandler)
            x.node().setFromCollideMask(BitMask32(0x0001))
            #print x.getName()
            x.setTag("location", x.getName())


        self.windows = self.cockpit.find("**/windows")
        self.windows.setColor(1,1,1,.5)
        self.windows.setBin("fixed",21)
        #self.collisionNode.show()

        #Node for the AI to find and attack it
        self.playerNode = self.cockpit.attachNewNode("player")


        self.crosshair = self.cockpit.find("**/crosshair")
        self.crosshair.setScale(.5)
        self.crosshair.setColor(1,1,1,.7)
        self.crosshair.setPos(self.crosshair, 0,.2,0 )

        base.disableMouse()
        #self.cockpit.setScale(.5) #3 KM
        base.camera.wrtReparentTo(self.cockpit)
        #base.camera.setScale(.2)
        base.camera.setHpr(0,2,0)
        #base.camera.setPos(0,0,0)
        base.camera.setPos(0,-1.7,.65)
        base.camLens.setFov(58)
        base.camLens.setNear(.08)

        #self.cockpit.setScale(.1)

        left = self.cockpit.find("**/leftScreen")
        right = self.cockpit.find("**/rightScreen")
        middle = self.cockpit.find("**/middleScreen")
        top = self.cockpit.find("**/topScreen")

        ###IMPORTANT###
        #With a transparent object in the cockpit, and the fact that the cockpits actual
        #position is closer than the hull of the ship (same object), it results in
        #depth buffer fighting between to two
        #
        #to fix this proble, i had to make sure that the cockpit
        #and the blips render BEFORE the big hologram circle
        #otherwise things would get lopped of in the depth test
        ###
        self.cockpit.setBin("fixed", 40)
        self.tubes = self.cockpit.find("**/tubes")
        self.tubes.setBin("fixed",20)

    def getCockpit( self ) :
        return self.cockpit
    
    def getCrosshair( self ) :
        return self.crosshair

    def changeCockpit( self ) :
        self.cockpit.hide()
        self.pegasus.show()
        self.pegasus.setPos(self.cockpit.getPos(render))
        self.pegasus.setHpr(self.cockpit.getHpr())
        
    def blowupSequence( self ) :
        if not self.shipBlowingUp:
            self.shipBlowingUp = True
            self.cockpit.hide()
            self.pegasus.show()
            self.pegasus.setPos(self.cockpit.getPos(render))
            self.pegasus.setHpr(self.cockpit.getHpr())
            if base.camera.getParent() != self.cockpit:
                base.camera.reparentTo(self.cockpit)
            base.camera.setPos(0, -20, 5)
            base.camera.wrtReparentTo(render)
            print base.camera.getPos(render)
            print self.pegasus.getPos(render)
            print self.cockpit.getPos(render)
            base.camera.lookAt(self.cockpit)
            Sequence(Wait(1),
                    Func(self.pegasus.hide),
                    Func(Explosion, self.pegasus.getPos(render), 1),
                    Func(Explosion, self.pegasus.getPos(render), 1),
                    Func(Explosion, self.pegasus.getPos(render), 1),
                    Wait(2),
                    Func(messenger.send, 'missionfailedmenu', ['You Died Loser'])).start()

    def cleanUp(self):
        print "COCKPIT CLEANUP"
        #self.filters.delBloom()
        #self.filters.cleanup()

        self.cockpit.removeNode()
        self.pegasus.removeNode()
        self.windows.removeNode()
        self.playerNode.removeNode()
        self.tubes.removeNode()

        base.camera.reparentTo(render)
        base.camLens.setFov(40)
        base.camLens.setNear(1)
