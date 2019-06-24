from pandac.PandaModules import *
from Collidable import *
from Explosion import *
import config
import GameManager

class MyCollisionPlane(Collidable):
    UID = 0
    def __init__(self, startPos, lookAtNode, eventName = 'endzone'):
        self.id = None #ID for the collidable object
        self.otherNode = render.find("**/other")
        self.myNode = self.otherNode.attachNewNode("MyCollisionPlane")
        self.myArt = OnscreenImage(image = 'Art/textures/mission3_plane.png',
                                    scale = 6000,
                                    hpr = (90, 0, 0),
                                    color = (1, 0, 0, 0))
        self.myArt.reparentTo(self.myNode)
        self.myArt.setTransparency(TransparencyAttrib.MAlpha)
        self.type = "plane"
        self.HP = 50
        self.DMG = 50
        self.isDead = 'false'
        self.eventName = eventName
        #GameManager.EntityMgr.add( self )
        
        self.myNode.setPos(startPos)
        self.myNode.lookAt(lookAtNode)
        
        MyCollisionPlane.UID += 1
        self.tempID = MyCollisionPlane.UID
        
        
        plane = CollisionPlane(Plane(Vec3(0, 1, 0), Point3(0, 0, 0)))
        self.collisionNode = self.myNode.attachNewNode(CollisionNode('colPlane'))
        self.collisionNode.node().addSolid(plane)
##        base.cTrav.addCollider(self.collisionNode, config.collisionHandler)
        

        #Set up the collidable stuff)
        #after this call, self.id should be an INT
        Collidable.__init__(self, self, self.myNode, "other")
        
        #set this nodes tag so when there is a collision it can be found in the dictionary
        self.myNode.setTag("type", "other")
        self.myNode.setTag("id", str(self.id))
        self.myNode.setTag("collisionType", "from")
    def bulletCollide(self, bullet):
        pass
            
    def otherCollide(self, other):
        pass
        
    def otherCollideWithCockpit(self):
        messenger.send(self.eventName)
        self.myNode.removeNode()
        
    def cleanUp(self):
        self.myNode.removeNode()
##        base.cTrav.removeCollider(self.collisionNode)
        self.removeFromCollidables(self.id, "other")

        self.collisionNode.removeNode()

        del self.tempID