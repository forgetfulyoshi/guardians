from pandac.PandaModules import *
from direct.task import Task

from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from AIMissile import *
from Collidable import *
from BaseMissile import *
import GameManager
from Exhaust import *


class Missile(Collidable):
    def __init__(self, type, targetNode, startNode):
        self.missileData = BaseMissile(type)
        
        #Add missile to MissileManager
        GameManager.EntityMgr.add( self )
        
        self.missileData.setTarget(targetNode)
        self.missile = self.missileData.getModelData()
        self.missileNode = render.find("**/missiles")
        self.missile.reparentTo(self.missileNode)
        self.missile.setPos(startNode.getPos(render))
        self.missile.setHpr(startNode.getHpr(render))
        self.myNode = self.missile.attachNewNode("missile")
        
        #taskMgr.add( self.cleanupTask , 'MissilecleanUp')
        
        
        self.cs = CollisionTube(0 , 1 , 0,  0, -1, 0, .09)
        self.collisionNode = self.myNode.attachNewNode(CollisionNode('cnode1'))
        self.collisionNode.node().addSolid(self.cs)
        #self.collisionNode.show()
        
        self.locator = self.missile.find("**/locator1")
        self.locator.setH(180)
        self.exhaust = Exhaust(self.locator, .3)
        #self.p = ParticleEffect()
        #self.p.loadConfig(Filename("Art/fireish.ptf"))
        #self.p.start(self.missile)
        #self.p.setPos(self.locator.getPos()+Vec3(0,-.15,0))
        #self.p.setP(90)
        #self.p.setScale(.15,.15,.75)
        
        
        
        
        Collidable.__init__(self,self, self.missile, "missile")
        
        self.myNode.setTag("type", "missile")
        self.myNode.setTag("id", str(self.id))
        self.myNode.setTag("collisionType", "into")
        
        self.missileAi = AIMissile( self.missileData )
        
    def setDmg( self , tempDMG ) : self.missileData.maxDMG = tempDMG
    def getDmg( self ) : return self.missileData.maxDMG
    def cleanUp( self ) :
        #print 'Missile Destruction in Missile'
        #Cleanup and remove all refrences that the class instance contains
        # missile missileNode missileAi
        
        
        del self.collisionNode
        del self.cs
        self.exhaust.cleanUp()
        del self.exhaust
        self.myNode.removeNode()
        del self.myNode
        
        del self.missileNode
        del self.missile
        del self.missileData
         
        self.missileAi.cleanUp()
        del self.missileAi
    def cleanupTask( self , task ) :
        
        if self.missileData.lifetime <= 0 :
            
            self.cleanUp()
            
            
            return task.done
        else :
           
            return task.again
        
        