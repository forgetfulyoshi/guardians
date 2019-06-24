from pandac.PandaModules import *
from Asteroid import *
import random
import math
import config

class AsteroidHandler():
    def __init__(self, shipModel):
        self.shipModel = shipModel
        self.MAX_ASTEROIDS = 50
        self.RADIUS = 250
        self.asteroidNode = NodePath("asteroidNode")
        self.asteroidNode.reparentTo(render)
        self.asteroidList = []
        print self.shipModel
        taskMgr.doMethodLater(0.08, self.spawnAsteroid, "AsteroidHandler_spawnAsteroid")
        
        
    def spawnAsteroid(self, task):
        if (len(self.asteroidList) < self.MAX_ASTEROIDS):
            Xpos = random.uniform(-self.RADIUS, self.RADIUS)
            Ypos = math.sqrt(self.RADIUS**2 - Xpos**2)
            Yprime = random.uniform(-Ypos, Ypos)
            Zpos = math.sqrt(Ypos**2 - Yprime**2) * random.randint(-1,1)
            self.asteroidList.append(Asteroid(Point3(Xpos, Ypos, Zpos), self.shipModel, self.shipModel))
            
        for asteroid in self.asteroidList:
            if asteroid.myNode.getDistance(self.shipModel) >= self.RADIUS + 50:
                asteroid.isDead = True
                self.asteroidList.remove(asteroid)
                del asteroid
##                print "DELETED ASTEROID"
        
        return task.again
            
        
    def cleanUp(self):
        
        taskMgr.remove("AsteroidHandler_spawnAsteroid") 
        
        for asteroid in self.asteroidList:
            asteroid.isDead = True
            self.asteroidList.remove(asteroid)
            del asteroid
            
        self.asteroidNode.removeNode()
        
        
        