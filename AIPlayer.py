from pandac.PandaModules import *

from Ship import BaseShip
from AIFlightHandler import *
from Collidable import *
import config
import GameManager
from Exhaust import *

class AIPlayer(Collidable):
    def __init__(self, aitype ,shiptype, alignment, position): #position is a Vec3
        self.id = None
        self.isDead = False
        self.ship = BaseShip(shiptype)
        #self.modelString = self.ship.getShipModel()
        GameManager.EntityMgr.add( self )
        
        print "AITYPE!!!!", aitype
        if aitype == "roger":
            self.type = "roger"
        elif aitype == "ben":
            self.type = "ben"
        elif aitype == "battleShip":
            self.type = "battleship"
        elif aitype == "dumb":
            self.type = "dumb"
        print self.type
        
        

        self.aiGoodNode = render.find("**/good")
        self.aiBadNode = render.find("**/bad")
        if alignment == 'good':
            self.shipModel = self.ship.getShipModel()
            self.shipModel.setScale(3)
            self.shipModel.reparentTo(self.aiGoodNode)
            self.shipModel.setPos(position)
        elif alignment == 'bad':
            self.shipModel = self.ship.getShipModel()
            self.shipModel.setScale(3)
            self.shipModel.reparentTo(self.aiBadNode)
            self.shipModel.setPos(position)

        engines = self.shipModel.find("**/engines")
        self.engineList = []
        for x in engines.getChildrenAsList():
            engine = Exhaust(x, 1)
            self.engineList.append(engine)

        colnode = self.shipModel.find("**/collision")
        #colnode.ls()
        for x in colnode.getChildrenAsList():
            #x.show()
            base.cTrav.addCollider(x, config.collisionHandler)
            x.node().setFromCollideMask(BitMask32(0x0010))
            #print x.getName()
            x.setTag("location", x.getName())
        #self.cs = CollisionSphere(0, 0 , 0 , 1)
        #self.collisionNode = self.shipModel.attachNewNode(CollisionNode('cnode'))
        #self.collisionNode.node().addSolid(self.cs)
        #self.collisionNode.show()
        #base.cTrav.addCollider(self.collisionNode, config.collisionHandler)
        #self.collisionNode.node().setFromCollideMask(BitMask32(0x0010))

        Collidable.__init__(self,self, self.shipModel, "ship")
        self.shipModel.setTag("type", "ship")
        self.shipModel.setTag("id", str(self.id))
        self.shipModel.setTag("collisionType", "from")

        self.flightHandler = AIFlightHandler(self.ship, aitype, alignment)

    def cleanUp( self ) :
        messenger.send("shipDestroyed")

        for x in self.engineList:
            x.cleanUp()
            x = None
        del self.engineList

        self.flightHandler.cleanUp()
        del self.flightHandler

        del self.shipModel

        self.ship.cleanUp()
        del self.ship

        del self.aiGoodNode
        del self.aiBadNode
        del self.id
