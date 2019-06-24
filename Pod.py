from pandac.PandaModules import *
from Collidable import *
import config
import GameManager
from Explosion import *
from Exhaust import *
import copy

class Pod(Collidable):
    UID = 0
    def __init__(self, startPos):
        self.id = None #ID for the collidable object
        self.otherNode = render.find("**/other")
        self.myNode = self.otherNode.attachNewNode("Pod")
        self.myArt = loader.loadModel('Art/mission1_pod3.bam')
        self.myArt.reparentTo(self.myNode)
        self.myArt.setScale(6)
        self.myArt.setH(180)
        self.type = "pod"
        self.HP = 100
        self.DMG = 25
        self.isDead = 'false'

        self.myNode.setPos(startPos)
        self.myNode.setScale(.75)

        #Pod.UID += 1
        self.tempID = copy.copy(config.nextOtherID)
        
        self.colNodes = []
        self.colNodes.append(self.myArt.find("**/col_front"))
        self.colNodes.append(self.myArt.find("**/col_back"))
        self.colNodes.append(self.myArt.find("**/left_front"))
        self.colNodes.append(self.myArt.find("**/left_back"))
        self.colNodes.append(self.myArt.find("**/right_front"))
        self.colNodes.append(self.myArt.find("**/right_back"))
        
        for x in self.colNodes:
            #print x
            base.cTrav.addCollider(x, config.collisionHandler)
            #x.show()
            #x.show()
        #cs = CollisionSphere(0, 0, 0, 2)
        #self.collisionNode = self.myNode.attachNewNode(CollisionNode('cnode'))
        #self.collisionNode.node().addSolid(cs)

        #self.collisionNode.show()

        #Set up the collidable stuff)
        #after this call, self.id should be an INT
        Collidable.__init__(self, self, self.myNode, "other")

        #set this nodes tag so when there is a collision it can be found in the dictionary
        self.myNode.setTag("type", "other")
        self.myNode.setTag("id", str(self.id))
        self.myNode.setTag("collisionType", "from")

        #Add particles
        #----------------------------------------------------------------------
##        base.enableParticles()
        podLocatorNode = self.myArt.find('**/locators')
        for child in podLocatorNode.getChildrenAsList():
            self.exhaust = Exhaust(child, 1.5)
            child.setH(90)
            child.setP(-24)
            child.setPos(child, 0,-.16,0)
            #x = loader.loadModel('Art/exhaust2.egg')
            #x.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
            #x.reparentTo(child)
            #x.setScale(2)
            #x.setPos(x, 0,.2,0)
            #y = loader.loadTexture("Art/textures/exhaustsprite/exhaust0040.png")
            ##x.setTexture(y)
            ##x.setTransparency(TransparencyAttrib.MAlpha)
            #x.find("**/inside").setBin("fixed",2)
            #x.find("**/outside").setBin("fixed",3)
            #break
        #    x.setColor(.6,0,0,1)
        #    x.setP(180)
##            engine = ParticleEffect()
##            engine.loadConfig(Filename("Art/fireish.ptf"))
##            engine.start(child)
##            engine.setP(-90)
        #----------------------------------------------------------------------

    def bulletCollide(self, bullet):
        self.HP -= bullet.DMG
        if self.HP <= 0:
            Explosion(self.myNode.getPos(),0)
            self.myNode.removeNode()
            self.removeFromCollidables(self.id, "other")
            messenger.send('poddied')

    def otherCollide(self, other):
        self.HP -= other.DMG
        if self.HP <= 0:
            Explosion(self.myNode.getPos(),0)
            self.myNode.removeNode()
            self.removeFromCollidables(self.id, 'other')
            messenger.send('poddied')
    def otherCollideWithCockpit(self):
        self.HP -= 20
        if self.HP <= 0:
            Explosion(self.myNode.getPos(),0)
            self.myNode.removeNode()
            self.removeFromCollidables(self.id, 'other')
            messenger.send('poddied')
    def cleanUp(self):
        self.myNode.removeNode()
        for x in self.colNodes:
            x.removeNode()
        #self.collisionNode.removeNode()

        self.exhaust.cleanUp()
        del self.exhaust

        del self.tempID
