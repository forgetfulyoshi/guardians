from pandac.PandaModules import *
from Collidable import *
import config
import GameManager

class Bullet(Collidable):
    UID = 0
    def __init__(self,bulletType, maskType,startNode, shipNode, headingOffset, shipVelocity, target = Point3(0,0,0)):
        self.shipVelocity = shipVelocity
        self.id = None #ID for the collidable object
        self.bulletNode = render.find("**/bullets")
        self.myNode = self.bulletNode.attachNewNode("bullet")
        self.shipNode = shipNode
        if maskType == "player":
            self.DMG = 10
        else:
            self.DMG = 3
        self.isDead = False
        GameManager.EntityMgr.add( self )

        self.startPos = startNode.getPos(render) #+ shipNode.getPos(render)
        self.myNode.setPos(self.startPos)
        self.myNode.setQuat(shipNode.getQuat())
        self.myNode.setH(self.shipNode, self.myNode.getH(self.shipNode) + headingOffset)

        if target != Point3(0,0,0):
            #currentHpr = self.myNode.getHpr()
            self.myNode.lookAt(target)
            #targetH = self.myNode.getH()
            #self.myNode.setHpr(currentHpr)
            #self.myNode.setH(targetH)


        self.dirVector = self.myNode.getQuat().getForward()
        self.dirVector.normalize()
        Bullet.UID += 1
        self.tempID = Bullet.UID
        taskMgr.doMethodLater(0.03, self.move, 'Bullet_move' + str(self.tempID))



        if bulletType == "bullet":
            self.lifetime =  100# ~= 5 seconds
            cs = CollisionSphere(0, 0, 0, .2)
            self.collisionNode = self.myNode.attachNewNode(CollisionNode('cnode'))
            self.collisionNode.node().addSolid(cs)
            #base.cTrav.addCollider(self.collisionNode, config.collisionHandler)
            x = loader.loadModel("Art/cylinder.bam")
            x.reparentTo(self.myNode)
            x.setScale(.05,.7,.05)
            x.setColor(1,0,0,.8)
            #self.collisionNode.show()
            self.speed = 5


        else:
            pass #use some other anim ect

        if maskType == "ai":
            self.collisionNode.setCollideMask(BitMask32(0x0001))
        else:
            self.collisionNode.setCollideMask(BitMask32(0x0010))
        #Set up the collidable stuff)
        #after this call, self.id should be an INT
        Collidable.__init__(self, self, self.myNode, "bullet")

        #set this nodes tag so when there is a collision it can be found in the dictionary
        self.myNode.setTag("type", "bullet")
        self.myNode.setTag("id", str(self.id))
        self.myNode.setTag("collisionType", "into")



    def setDmg( self , tempDMG ) : self.DMG = tempDMG
    def getDmg( self ) : return self.DMG
    def cleanUp(self):
        
        self.myNode.removeNode()


    def move(self, task):
        if self.myNode:
            if self.myNode.isEmpty():
                return
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.isDead = True
            if self.myNode:
                if not self.myNode.isEmpty():
                    self.myNode.hide()
            taskMgr.remove('Bullet_move' + str(self.tempID))
            #self.myNode.hide()
            return
        else:
            velVector = self.dirVector * self.speed
            #velVector = velVector * -1
            #print velVector
            self.myNode.setPos(velVector[0] + self.shipVelocity[0] + self.myNode.getX(),
                               velVector[1] + self.shipVelocity[1] +self.myNode.getY(),
                               velVector[2] + self.shipVelocity[2] +self.myNode.getZ())
            return task.again
