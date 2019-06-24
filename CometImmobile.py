from pandac.PandaModules import *
from Collidable import *
from Explosion import *
import config
import GameManager
import copy

class CometImmobile(Collidable):
    UID = 0
    def __init__(self, startPos, scale = 4, hp = 50, damage = 50):
        self.id = None #ID for the collidable object
        self.otherNode = render.find("**/other")
        self.type = "comet"
        self.myNode = self.otherNode.attachNewNode("CometImmobile")
        cometType = randint(1,2)
        if cometType == 1:
            self.myArt = loader.loadModel('Art/asteroid_good1.bam')
        else:
            self.myArt = loader.loadModel('Art/asteroid_good2.bam')
        self.myArt.reparentTo(self.myNode)
        self.myArt.setScale(scale)
        self.HP = hp
        self.DMG = damage
        self.isDead = False
        GameManager.EntityMgr.add( self )

        self.myNode.setPos(startPos)
        self.myNode.setColor(0.5, 0.5, 0.5, 1)

        ##CometImmobile.UID += 1
        self.tempID = copy.copy(config.nextOtherID)


        self.collisionNode = self.myArt.find('**/colSphere')
        base.cTrav.addCollider(self.collisionNode, config.collisionHandler)

        #Set up the collidable stuff)
        #after this call, self.id should be an INT
        Collidable.__init__(self, self, self.myNode, "other")

        #set this nodes tag so when there is a collision it can be found in the dictionary
        self.myNode.setTag("type", "other")
        self.myNode.setTag("id", str(self.id))
        self.myNode.setTag("collisionType", "from")
    def bulletCollide(self, bullet):
        self.HP -= bullet.DMG
        if self.HP <= 0:
            Explosion(self.myNode.getPos(),0)
            self.myNode.removeNode()
            base.cTrav.removeCollider(self.collisionNode)
            self.removeFromCollidables(self.id, "other")


    def otherCollide(self, other):
        self.HP -= other.DMG
        if self.HP <= 0:
            self.isDead = True
##            self.myNode.removeNode()
##            base.cTrav.removeCollider(self.collisionNode)
##            self.removeFromCollidables(self.id, 'other')
    def otherCollideWithCockpit(self):
        self.HP -= 50
        print self.HP
        if self.HP <=0:
            Explosion(self.myNode.getPos(),0)
            self.isDead = True
##            self.myNode.removeNode()
##            base.cTrav.removeCollider(self.collisionNode)
##            self.removeFromCollidables(self.id, 'other')
            
    def cleanUp(self):
        self.myNode.removeNode()
        base.cTrav.removeCollider(self.collisionNode)
        self.removeFromCollidables(self.id, "other")

        self.collisionNode.removeNode()

        del self.tempID
