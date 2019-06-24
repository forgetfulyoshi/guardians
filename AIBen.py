#from direct.fsm import *
from Bullet import *
import direct.fsm
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
from direct.task import Task


import random
import threading
import copy
from math import *

class AIBen(direct.fsm.FSM.FSM):
    UID = 0
    TASK_TIME = 0.01
    BULLET_SPEED = 5
    BULLET_LIFETIME = 100
    
    def __init__(self, ship, alignment):
        direct.fsm.FSM.FSM.__init__(self,'AIBen_FSM')
        self.SEARCH_RADIUS = 150
        self.FOV = 58
        self.THRESH = 35
        self.currentWorry = None
        self.alignment = alignment
        self.currentTarget = NodePath("TempTarget")
        self.targetList = []
        self.ship = ship
        self.shipModel = self.ship.getShipModel()
        self.currentHealth = self.ship.leftHull + self.ship.rightHull + self.ship.backHull + self.ship.frontHull
        self.previousHealth = self.currentHealth
        self.UID = copy.deepcopy(AIBen.UID)
        AIBen.UID += 1
        self.currentDestination = Point3(0,0,0)
        self.gunLocation = 1
        self.searchNum = 0
        self.numGuns = len(self.shipModel.find("**/guns").getChildrenAsList())
        self.canShoot = True

        self.targetCurrentPos = Vec3(0,0,0)
        self.targetPreviousPos = Vec3(0,0,0)
        self.currentPosition = Vec3(0,0,0)
        self.previousPosition = Vec3(0,0,0)

        taskMgr.doMethodLater(0.03, self.moveTask, "AIBen_moveTask: " + str(self.UID))
        taskMgr.doMethodLater(0.1, self.preserveLife, "AIBen_preserveLife: " + str(self.UID))
        self.request("Idle")
    
    def setTarget(self, nodePath):
        self.currentTarget = nodePath

    def enterIdle(self):
        print "IDLE"
        self.getTarget()
        
        startPos = self.shipModel.getPos()
        taskMgr.doMethodLater(3, self.search, "AIBen_search: " + str(self.UID), extraArgs = [Task, startPos])
        taskMgr.doMethodLater(0.1, self.checkForTarget, "AIBen_checkForTarget: " + str(self.UID))
        
    def exitIdle(self):
        taskMgr.remove("AIBen_search: " + str(self.UID))
        taskMgr.remove("AIBen_checkForTarget: " + str(self.UID))

    def enterAttack(self):
        print "ATTACK"
        self.getTarget()
                
        taskMgr.doMethodLater(0.03, self.trackTarget, "AIBen_trackTarget: " + str(self.UID))

    def exitAttack(self):
        taskMgr.remove("AIBen_trackTarget: " + str(self.UID))

    def enterEvasive(self):
        print "EVASIVE"
        taskMgr.doMethodLater(2, self.getEvasiveDest, "AIBen_getEvasiveDest: " + str(self.UID))

    def exitEvasive(self):
        taskMgr.remove("AIBen_getEvasiveDest: " + str(self.UID))
    
    def getTarget(self):
        if self.alignment == 'bad':
            self.targetList = render.find('**/good').getChildrenAsList()
        elif self.alignment == 'good':
            self.targetList = render.find('**/bad').getChildrenAsList()
            
        for target in self.targetList:
            if self.shipModel.getDistance(target) < self.shipModel.getDistance(self.currentTarget):
                self.currentTarget = target
    
    def search(self, task, startPos):
        print startPos
        if self.searchNum == 0:
            self.currentDestination = startPos + Point3(0, self.SEARCH_RADIUS, 0)
            self.searchNum = (self.searchNum + 1)%4
        elif self.searchNum == 1:
            self.currentDestination = startPos + Point3(self.SEARCH_RADIUS, 0, 0)
            self.searchNum = (self.searchNum + 1)%4
        elif self.searchNum == 2:
            self.currentDestination = startPos + Point3(0, -self.SEARCH_RADIUS, 0)
            self.searchNum = (self.searchNum + 1)%4
        elif self.searchNum == 3:
            self.currentDestination = startPos + Point3(-self.SEARCH_RADIUS, 0, 0)
            self.searchNum = (self.searchNum + 1)%4
    
        return task.again
    
    def checkForTarget(self, task):
        trueTargetVector = self.currentTarget.getPos(render) - self.shipModel.getPos(render)
        trueTargetVector.normalize()
        
        if self.shipModel.getQuat().getForward().relativeAngleDeg(trueTargetVector) < self.FOV or self.shipModel.getQuat().getForward().relativeAngleDeg(trueTargetVector) > -self.FOV:
            self.request("Attack")
        
        return task.again
    
    def trackTarget(self, task):
        tempNode = render.attachNewNode("tempNode")
        
        self.targetCurrentPos = self.currentTarget.getPos(render)
        self.currentPosition = self.shipModel.getPos(render)
        
        targetForward = (self.targetCurrentPos - self.currentPosition) - (self.targetPreviousPos - self.previousPosition)
        
        bulletETA = self.shipModel.getDistance(self.currentTarget) / AIBen.BULLET_SPEED
        
        positionAtBulletHit = self.targetCurrentPos + (targetForward * bulletETA)
        tempNode.setPos(positionAtBulletHit)
        distToTarget = self.shipModel.getDistance(tempNode)

        self.targetPreviousPos = self.targetCurrentPos
        self.previousPosition = self.currentPosition

        tempVector = positionAtBulletHit
        
        self.currentDestination = Point3(tempVector[0], tempVector[1], tempVector[2])
        
        tempNode.removeNode()
        return task.again
    
    def preserveLife(self, task):
        self.currentHealth = self.ship.leftHull + self.ship.rightHull + self.ship.backHull + self.ship.frontHull
        
        for ent in render.find("**/good").getChildrenAsList() + render.find("**/bad").getChildrenAsList():
            if ent != self.shipModel and self.shipModel.getDistance(ent) < self.THRESH and self.state != "Evasive":
                print "TOO CLOSE"
                self.currentDestination =  (self.shipModel.getPos(render) * 2) - ent.getPos(render)
                self.currentWorry = ent
                self.searchNum = 0
                self.request("Evasive")
                break
                
                
        if self.currentHealth < self.previousHealth:
            print "GETTING HIT"
            self.request("Evasive")
            
        
        self.previousHealth = self.currentHealth
        return task.again
    
    def getEvasiveDest(self, task):
        
        if self.searchNum == 0:
            self.searchNum = 1
        elif self.searchNum == 1:
            if self.shipModel.getDistance(self.currentWorry) > self.THRESH: self.request("Idle")
            self.currentDestination += Point3(0, self.SEARCH_RADIUS, self.SEARCH_RADIUS)
            self.searchNum = 2
        elif self.searchNum == 2:
            if self.shipModel.getDistance(self.currentWorry) > self.THRESH: self.request("Idle")
            self.currentDestination += Point3(self.SEARCH_RADIUS, self.SEARCH_RADIUS, 0)
            self.searchNum = 3
        elif self.searchNum == 3:
            if self.shipModel.getDistance(self.currentWorry) > self.THRESH: self.request("Idle")
            self.currentDestination += Point3(0, self.SEARCH_RADIUS, -self.SEARCH_RADIUS)
            self.searchNum = 4
        elif self.searchNum == 4:
            self.currentDestination += Point3(-self.SEARCH_RADIUS, self.SEARCH_RADIUS, 0)
            self.searchNum = 0
            self.request("Idle")
        
        return task.again
    
    
#----------------------------------------------------------------------------------------------
# Moving, shooting, etc.
#----------------------------------------------------------------------------------------------
    def moveTask(self, task):
        self.currentDestination = Point3(self.currentDestination[0],
                                         self.currentDestination[1],
                                         self.currentDestination[2])
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

        if ((self.shipModel.getPos() - self.currentDestination).length() < AIBen.BULLET_SPEED * AIBen.BULLET_LIFETIME) and self.state == 'Attack' and currentHpr.almostEqual(targetHpr, 3):
            if self.canShoot:
                self.shoot()
                self.shoot()
                t = threading.Timer(.5, self.setCanShoot).start()
                self.canShoot = False
                
        return task.again


    def shoot(self):
        searchString = "**/gun" + str(self.gunLocation)
        startLoc = self.shipModel.find(searchString)

        Bullet("bullet", "ai", startLoc, self.shipModel, 0, self.velocityVector, self.currentDestination)

        self.cycleGun()

    def cycleGun(self):
        self.gunLocation += 1
        if self.gunLocation >= self.numGuns:
            self.gunLocation = 1

    def setCanShoot(self):
        self.canShoot = True

    def targeted(self):
        # Redo
        pass


    def cleanUp(self):
        self.cleanup()
        taskMgr.remove("AIBen_preserveLife: " + str(self.UID))
        taskMgr.remove('AIBen_moveTask: ' + str(self.UID))

        del self.shipModel
        del self.ship
