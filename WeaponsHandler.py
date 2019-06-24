from direct.showbase import DirectObject
from pandac.PandaModules import *
import threading
import config

from Bullet import *
from Missile import *
from TargetHologram import *

#import Collidable
from TargetScreen import *

class WeaponsHandler(DirectObject.DirectObject):
    def __init__(self, flightHandler, ship, model, type):
        self.Target = 'NO TARGET'
        self.count = 0
        self.ship = ship
        self.model = model
        self.gunlocation = 1
        self.flightHandler = flightHandler
        self.accept("fireGun", self.fireGun)
        self.accept("fireMissile", self.fireMissile)
        #self.accept("a" , self.ship.cycleActiveWeapon)
        self.accept('t' , self.aquireTarget)
        self.accept('targetPicked', self.handleTarget)
        self.t = threading.Timer(.5, self.setCanAquire)
        self.canAquire = True
        self.currentId = 0
            
        #self.targetHologram = TargetHologram(self.model.find("**/hologramLocator1"))
        self.targetScreen = TargetScreen(self.model.find("**/leftScreen"))
        #self.targetScreen = )
        taskMgr.doMethodLater(.5, self.renewEnergy, 'renewEnergy')
    def renewEnergy(self,task):
        if self.ship.energy <= 100:
            self.ship.energy += 4
        
        return task.again
    def fireGun(self):
        self.ship.energy -= 2
        if self.ship.energy >= 0:
            #print self.ship.energy
            NUMBER_OF_GUNS = 1
            x = self.model.find("**/guns")
            x = x.getChildrenAsList()
           
            #for y in range(NUMBER_OF_GUNS):
                #Make sure to not save any references of this
                #if so cleanup inside of bullet must remove the reference
                #to itself
            if self.gunlocation == 1 :
                #print 'shoot gun 1'
                Bullet("bullet","player",x[self.gunlocation-1], self.model, -1, self.flightHandler.velocityVector)
                self.gunlocation = 2
            else :
                #print 'shoot gun 2'
                Bullet('bullet' ,"player", x[self.gunlocation-1] , self.model , 1 , self.flightHandler.velocityVector)
                self.gunlocation = 1
        
    def fireMissile(self):
        if self.Target == 'NO TARGET' :
            print 'no valid target fire aborted'
            return
        else:
            if self.ship.missiles > 0:
                self.ship.missiles -= 1
                self.count += 1
                #print "fireMissile"
                aiNode = render.find("**/ai")
                #tempTarget = aiNode.getChildrenAsList()[0]
               # self.Target = tempTarget
                x = self.model.find("**/guns")
                x = x.getChildrenAsList()
            
                y = Missile('homingmissile', self.Target, x[1])
                #print self.count
            
    def aquireTarget( self ) :
        aiNode = render.find('**/ai')
        ##self.Target = aiNode.getChildrenAsList()[randint(0 , len(aiNode.getChildrenAsList()) - 1)]
        #self.targetHologram.setTarget(self.Target)
        
        #cs = CollisionSphere(0, 0, 0, 1)
        #self.collisionNode = self.cockpit.attachNewNode(CollisionNode('cnode'))
        #self.collisionNode.node().addSolid(cs)
        #base.cTrav.addCollider(self.collisionNode, config.collisionHandler)
        #self.collisionNode.node().setFromCollideMask(BitMask32(0x0001))
        
        if self.canAquire:
            print "Trying to Target!"
            self.canAquire = False
            startNode = self.model.find("**/crosshair")
            startPos = startNode.getPos(render)
            direction = self.model.getQuat().getForward()
            self.targetRayNode = render.attachNewNode(CollisionNode("targetRayNode"))
            self.targetRay = CollisionRay(startPos[0], startPos[1], startPos[2], direction[0],direction[1],direction[2])
            self.targetRayNode.setCollideMask(BitMask32(0x0000))
            self.targetRayNode.setTag("type", "targetRay")
            self.targetRayNode.node().addSolid(self.targetRay)
            #self.targetRay.reparentTo(self.targetRayNode)
            self.t = threading.Timer(.5, self.setCanAquire).start()
            base.cTrav.addCollider(self.targetRayNode, config.collisionHandler)
            base.cTrav.traverse(render)
        #print Collidable.Collidable.dispatcher.collidables
        #type = intoNode.getNetTag("type")
        ##id = self.Target.getNetTag("id")
        #aiRefernce = Collidable.Collidable.dispatcher.collidables['ship'][id]
        ##self.targetScreen.NewTarget(id, aiNode, self.Target)
    def setCanAquire(self):
        self.canAquire = True
        self.targetRayNode.removeNode()
        
    def handleTarget(self, node, id):
        if not id == self.currentId:
            print "handelTarget"
            aiNode = render.find('**/ai')
            self.currentId = id
            self.Target = node
            self.targetScreen.NewTarget(id, aiNode, self.Target)
            #self.t.stop()
            self.canAquire = True
            self.targetRayNode.removeNode()
        
    def cleanUp(self):
        self.targetScreen.cleanUp()
        del self.targetScreen
        taskMgr.remove('renewEnergy')
        del self.Target
        del self.flightHandler
        del self.model
        del self.ship
        self.ignore('fireGun')
        self.ignore('fireMissile')
        self.ignore('a')
        self.ignore('t')
        self.ignore('targetPicked')
        
        
