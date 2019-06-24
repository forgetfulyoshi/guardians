from Bullet import *

from pandac.PandaModules import *
from direct.showbase.PythonUtil import *

import random
import threading
import copy
from math import *

class AIBattleShip():
    UID = 0
    WEAPONS_RANGE = 1000
    TASK_TIME = 0.01
    BULLET_SPEED = 2
    BULLET_LIFETIME = 100
    
    def __init__(self, ship, alignment):

        self.alignment = alignment
        self.currentTarget = None
        self.targetList = []
        self.ship = ship
        self.shipModel = self.ship.getShipModel()
        
        #Need to rotate the engines 180
        self.shipModel.setScale(100)
        engines = self.shipModel.find("**/engines")
        for engine in engines.getChildrenAsList():
            engine.setH(180)
      
        
        self.UID = copy.deepcopy(AIBattleShip.UID)
        print "CREATED AI BattleShip ", self.UID
        AIBattleShip.UID += 1
        self.type = "battleship"
        self.isTargeted = False
        self.currentDestination = Point3(0,0,0)
        self.gunLocation = 0
        
        self.topTurrets = self.shipModel.find("**/topturrets").getChildrenAsList()
        for x in self.topTurrets:
            print x.getPos()
        self.bottomTurrets = self.shipModel.find("**/bottomturrets").getChildrenAsList()
        self.gunList = self.topTurrets + self.bottomTurrets
        
        self.numGuns = len(self.gunList)
        
        self.launchBays = self.shipModel.find("**/bays").getChildrenAsList()
        self.canShoot = True

        self.targetCurrentPos = Vec3(0,0,0)
        self.targetPreviousPos = Vec3(0,0,0)
        
        if self.alignment == 'bad':
            self.targetList = render.find('**/good').getChildrenAsList()
        elif self.alignment == 'good':
            self.targetList = render.find('**/bad').getChildrenAsList()

        taskMgr.doMethodLater(0.01, self.moveTask, "AIBattleShip_moveTask: " + str(self.UID))
    def setTarget(self, nodepath):
        self.currentTarget = nodepath
        self.hasTarget = True
    
    def moveTask(self, task):
        
        self.getTarget()
        
        ANGLE_FUDGE = 3
        # Get the current orientation, as a hpr
        currentHpr = self.shipModel.getHpr()

        # Get the orientation needed to face the target
        self.shipModel.lookAt(self.currentDestination)
        targetHpr = self.shipModel.getHpr()
        self.shipModel.setHpr(currentHpr)

        # Make sure the hpr's are both on the same side of the circle.
        targetHpr = VBase3(fitDestAngle2Src(currentHpr[0], targetHpr[0]),
                            fitDestAngle2Src(currentHpr[1], targetHpr[1]),
                            fitDestAngle2Src(currentHpr[2], targetHpr[2]))


        # Now rotate a bit torwards the target.
        hprChange =(targetHpr - currentHpr)

        #set them component wise because you should angle me able to make
        #a certain angle of turn per frame
        hChange = hprChange[0]
        pChange = hprChange[1]
        rChange = hprChange[2]

        if hChange > ANGLE_FUDGE:
            self.shipModel.setH(self.shipModel, self.ship.getMaxAnglePerFrame())
        elif hChange < -ANGLE_FUDGE:
            self.shipModel.setH(self.shipModel, -self.ship.getMaxAnglePerFrame())
        else:
            pass #No change to heading

        if pChange > ANGLE_FUDGE:
            self.shipModel.setP(self.shipModel, self.ship.getMaxAnglePerFrame())
        elif pChange < -ANGLE_FUDGE:
            self.shipModel.setP(self.shipModel, -self.ship.getMaxAnglePerFrame())
        else:
            pass #No change to pitch

        if rChange > ANGLE_FUDGE:
            self.shipModel.setR(self.shipModel, self.ship.getMaxAnglePerFrame())
        elif rChange < -ANGLE_FUDGE:
            self.shipModel.setR(self.shipModel, -self.ship.getMaxAnglePerFrame())
        else:
            pass #No change to roll


        self.speed = self.ship.getMaxSpeed()

        self.velocityVector = self.shipModel.getQuat().getForward() * self.speed
        self.shipModel.setPos(self.velocityVector[0] + self.shipModel.getX(),
                              self.velocityVector[1] + self.shipModel.getY(),
                              self.velocityVector[2] + self.shipModel.getZ())

        if ((self.shipModel.getPos() - self.currentDestination).length() < AIBattleShip.BULLET_SPEED * AIBattleShip.BULLET_LIFETIME):
            if self.canShoot:
                self.shoot()
                #self.shoot()
                #self.shoot()
                #self.shoot()
                t = threading.Timer(.5, self.setCanShoot).start()
                self.canShoot = False
                
        return task.again


    def shoot(self):
        
        startLoc = self.gunList[self.gunLocation]
        print "SHIP POS, == " , self.shipModel.getPos(render), "GUN POS, == ", startLoc.getPos(render)
        
        Bullet("bullet", "ai", startLoc, self.shipModel, 0, self.velocityVector, self.currentDestination)

        self.cycleGun()

    def cycleGun(self):
        self.gunLocation = (self.gunLocation + 1) % self.numGuns

    def setCanShoot(self):
        self.canShoot = True

    def getTarget(self):
        tempNode = render.attachNewNode("tempNode")
        
        if self.currentTarget == None:
            self.currentTarget = self.targetList[random.randint(0, len(self.targetList) - 1)]
        
        self.targetCurrentPos = self.currentTarget.getPos(render)

        bulletETA = self.shipModel.getDistance(self.currentTarget) / AIBattleShip.BULLET_SPEED


        positionAtBulletHit = self.targetCurrentPos + ((self.targetCurrentPos - self.targetPreviousPos) * bulletETA)
        tempNode.setPos(positionAtBulletHit)
        distToTarget = self.shipModel.getDistance(tempNode)


        self.targetPreviousPos = self.targetCurrentPos

        tempVector = positionAtBulletHit

        self.currentDestination = Point3(tempVector[0], tempVector[1], tempVector[2])
        
        tempNode.removeNode()


    def cleanUp(self):
        messenger.send("stop_battleship_spawn")
        taskMgr.remove("AIBattleShip_moveTask: " + str(self.UID))

        del self.shipModel
        del self.ship


        print "DELETED AI BattleShip ", self.UID


