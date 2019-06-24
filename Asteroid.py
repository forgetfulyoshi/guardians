from pandac.PandaModules import *
from Collidable import *
from Explosion import *

import config
import random
import GameManager

class Asteroid(Collidable):
    UID = 0
    def __init__(self, startPos, destination, shipModel, scale = 8, hp = 1000000, damage = 4000):
        
        #self.forwardVec = forwardVector
        self.SPEED = 2.5         
        self.id = None #ID for the collidable object
        self.otherNode = render.find("**/other")
        self.type = "comet"
        #self.myNode = self.otherNode.attachNewNode("Asteroid")
        
        self.myNode = NodePath("Asteroid")
        self.myNode.reparentTo(self.otherNode)
        
        cometType = randint(1,2)
        if cometType == 1:
            self.myArt = loader.loadModel('Art/asteroid_good3.bam')
        else:
            self.myArt = loader.loadModel('Art/asteroid_good3.bam')
        self.myArt.reparentTo(self.myNode)
        self.myArt.setScale(0.1)
        self.HP = hp
        self.DMG = damage
        self.isDead = False
        GameManager.EntityMgr.add( self )

        self.myNode.setPos(shipModel, startPos[0], startPos[1], startPos[2])
        
        self.forwardVec = destination.getPos() - self.myNode.getPos()
        self.forwardVec.normalize()
        
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
        self.myNode.setTag("collisionType", "into")
        
        self.lerp = LerpScaleInterval(self.myNode, 0.5, 20, 0.1)
        self.lerp.start()
        
        taskMgr.doMethodLater(0.03, self.move, "Asteroid_moveTask: " + str(self.tempID))
        
    def move(self, task):
        
        velocityVector = self.forwardVec * self.SPEED
        
        self.myNode.setPos( self.myNode.getX() + velocityVector.getX(),
                            self.myNode.getY() + velocityVector.getY(),
                            self.myNode.getZ() + velocityVector.getZ())
        
        return task.again
    
    def bulletCollide(self, bullet):
        self.HP -= bullet.DMG
        if self.HP <= 0:
            Explosion(self.myNode.getPos(),0)
            self.cleanUp()
            #self.myNode.removeNode()
            #base.cTrav.removeCollider(self.collisionNode)
            #self.removeFromCollidables(self.id, "other")

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
        
        self.lerp.finish()
        taskMgr.remove("Asteroid_moveTask: " + str(self.tempID))
        
        self.myNode.removeNode()
        base.cTrav.removeCollider(self.collisionNode)
        self.removeFromCollidables(self.id, "other")

        self.collisionNode.removeNode()
##        print "DELETED ASTEROID"
##        config.asteroidList.remove(self)

        del self.tempID
    
    