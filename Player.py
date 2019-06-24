from FlightHandler import *
from direct.showbase import DirectObject
from pandac.PandaModules import *

from Ship import BaseShip
from Cockpit import *
from Collidable import *
from Radar import *
from VelocityScreen import *
from TargetHologram import *
from MainScreen import *
from ShipScreen import *
#Design flaw, but collidables need access to ship data,
#player should NOT be a collidable
class Player(Collidable, DirectObject.DirectObject):
    def __init__(self):

        self.accept('cockpitToShip', self.cockpitToShip)

	self.id = None #will exist after collidable is set

	#Create the players ship
	self.playerShip = BaseShip('player-pegasus') #.003 == 324 Km/hr

	self.playerCockpit = Cockpit()


	self.flightHandler = FlightHandler(self.playerCockpit.getCockpit(),
					   self.playerShip)

        taskMgr.doMethodLater(0.03, self.flightHandler.runMovement, 'runMovement')

        Collidable.__init__(self, self, self.playerCockpit.getCockpit(), "cockpit")

	self.playerCockpit.cockpit.setTag("id", str(self.id))
	self.playerCockpit.cockpit.find("**/topScreen").hide()

        self.radar = Radar(self.playerCockpit.getCockpit())

        self.velocityScreen = VelocityScreen(self.flightHandler, self.playerCockpit.getCockpit().find("**/middleScreen"))

        self.shipScreen = ShipScreen(self.playerShip, self.playerCockpit.cockpit.find("**/rightScreen"))
    
	#Set up the headlights
	#------------------------------------------------------
	slight = Spotlight('slight')
	slight.setColor(VBase4(2, 2, 2, 1))
	lens = PerspectiveLens()
	lens.setFov(50)
	slight.setLens(lens)
	cockpitNode = render.find("**/cockpit_2.egg")
	self.slnp = cockpitNode.attachNewNode(slight)
	self.slnp.setQuat(cockpitNode.getQuat())
	render.find("**/other").setLight(self.slnp)
	render.find("**/ai").setLight(self.slnp)
	#------------------------------------------------------
	
	#Set up ambient light
	#------------------------------------------------------
	alight = AmbientLight('alight')
	alight.setColor(VBase4(0.75, 0.75, 0.75, 1))
	self.alnp = render.attachNewNode(alight)
	render.setLight(self.alnp)
	#------------------------------------------------------

    def cockpitToShip(self):
        self.playerCockpit.changeCockpit()

    def cleanUp(self):
        render.find("**/other").clearLight(self.slnp)
        render.find("**/ai").clearLight(self.slnp)
        render.clearLight(self.alnp)
        
        self.ignoreAll()

        self.playerShip.cleanUp()
        del self.playerShip

        self.playerCockpit.cleanUp()
        del self.playerCockpit

        self.flightHandler.cleanUp()
        del self.flightHandler

        self.radar.cleanUp()
        del self.radar

        self.velocityScreen.cleanUp()
        del self.velocityScreen

        self.shipScreen.cleanUp()
        del self.shipScreen

        taskMgr.remove('runMovement')
