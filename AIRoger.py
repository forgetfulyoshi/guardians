from direct.task import Task
from math import *
from pandac.PandaModules import Quat
from pandac.PandaModules import VBase3
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
from Bullet import *
import threading
import random

class AIRoger():
    UID = 0
    def __init__(self, baseShip, alignment):
        self.baseShip = baseShip
        self.shipNodePath = self.baseShip.getShipModel()
        AIRoger.UID += 1
        self.tempID = AIRoger.UID
        taskMgr.doMethodLater(.01, self.moveTask, 'AIRogerMoveTask' + str(self.tempID))
        
        if alignment == 'bad':
            self.targetList = render.find('**/good').getChildrenAsList()
        elif alignment == 'good':
            self.targetList = render.find('**/bad').getChildrenAsList()
        
        self.getTarget()

        self.lastFramePos = self.target.getPos(render)
        self.thisFramePos = self.target.getPos(render)
        #
        #self.shipNodePath.ls()
        self.velocityVector = VBase3(0,0,0)
        self.speed = self.baseShip.getMaxSpeed()
        self.accel= self.baseShip.getAccelRate()


        self.gunLocation = 1
        self.canShoot = True
        #state stuffs
        #0 - positioning
        #1 - aiming
        #2 - shooting
        #3 - creating distance
        self.state = 0
        self.POS_STATECHANGE_ANGLE = 2
    def cycleGun(self):
        self.gunLocation += 1
        if self.gunLocation >= 3:
            self.gunLocation = 1
    def cleanUp( self ) :
        del self.speed
        del self.accel
        del self.baseShip
        del self.target
        taskMgr.remove('AIRogerMoveTask' + str(self.tempID))
        del self.tempID

    def setCanShoot(self):
        self.canShoot = True
    def shoot(self, hisPos):
        searchString = "**/gun" + str(self.gunLocation)
        startLoc = self.shipNodePath.find(searchString)

        hisPos2 = hisPos + Point3(randint(-6,6), randint(-6,6), randint(-6,6))
        hisPos3 = Point3(hisPos2[0], hisPos2[1], hisPos2[2])
        Bullet("bullet", "ai", startLoc, self.shipNodePath, 3, self.velocityVector, hisPos3)
        self.cycleGun()
    def getTarget(self):
        if len(self.targetList) == 1:
            self.target = self.targetList[0]
        elif len(self.targetList) > 1:
            self.target = self.targetList[randint(0,len(self.targetList) - 1)]
        else:
            self.target = render.attachNewNode('tempNode')
        self.hasTarget = True
        print self.target
    def setTarget(self, nodePath):
        self.target = nodePath
        self.hasTarget = True
    def moveTask(self, task):
        #target Logic
        #
        #current bullet speed 1.4 (per frame)
        ###
        self.thisFramePos = self.target.getPos(render)
        frameChange = self.thisFramePos - self.lastFramePos

        tempNode = render.attachNewNode("getDistanceMustBeNodePath")

        distance = self.shipNodePath.getDistance(self.target)

        framesToDest = int((distance / 2) * self.baseShip.maxSpeed)

        positionWhenBulletArrives = self.thisFramePos + (frameChange * framesToDest)

        tempNode.setPos(positionWhenBulletArrives)
        distanceToEstimatedPos = self.shipNodePath.getDistance(tempNode)
        framesToEstPos = int((distanceToEstimatedPos / 2) * self.baseShip.maxSpeed)

        estimatedPos = self.thisFramePos + (frameChange * framesToEstPos)
        tempNode.removeNode()

        #print framesToDest

        #estimatedPos = self.thisFramePos +(frameChange * framesToDest) #+ (frameChange * 1.4)

        hisPos = estimatedPos
        #print estimatedPos

        self.lastFramePos = self.thisFramePos
        ###

        #castedVector = Vec3(hisPos[0],hisPos[1], self.shipNodePath.getZ())
        currentHpr = self.shipNodePath.getHpr()
        self.shipNodePath.lookAt(hisPos)
        targetHpr = self.shipNodePath.getHpr()
        self.shipNodePath.setHpr(currentHpr)

        # Make sure the hpr's are both on the same side of the circle.
        targetHpr = VBase3(fitDestAngle2Src(currentHpr[0], targetHpr[0]),
                            fitDestAngle2Src(currentHpr[1], targetHpr[1]),
                            fitDestAngle2Src(currentHpr[2], targetHpr[2]))

        # Now rotate a bit torwards the target.
        hprChange =(targetHpr - currentHpr)

        hChange = hprChange[0]
        pChange = hprChange[1]
        rChange = hprChange[2]
        #hisPosVector = Vec3(hisPos[0],hisPos[1], hisPos[2])

        hClose = False
        pClose = False
        rClose = False

        #hisPosVector[3] = 0 #casting z value
        #print castedVector
        if self.state < 2:
            if hChange > self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setH(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
            elif hChange < -self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setH(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
            else: #its inbetween the statechange,
                #self.shipNodePath.setH(targetHpr[0])
                hClose = True

            if pChange > self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setP(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
            elif pChange < -self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setP(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
            else:
                #self.shipNodePath.setP(targetHpr[1])
                pClose = True

            if rChange > self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setR(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
            elif rChange < -self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setR(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
            else:
                #self.shipNodePath.setR(targetHpr[2]) #No change to heading
                rClose = True

        ####
        #STATE STUFFS
        ####
        #print self.state
        if self.state == 0:
            if not self.hasTarget:
                self.getTarget()
            if hClose and pClose and rClose:
                self.state = 1
            forwardVec = self.shipNodePath.getQuat().getForward()
            ratio = self.baseShip.maxSpeed
            #self.shipNodePath.setPos(  self.shipNodePath, forwardVec * ratio)
            velocityVector = forwardVec * ratio
            self.shipNodePath.setPos(  velocityVector[0] + self.shipNodePath.getX(),
                            velocityVector[1] + self.shipNodePath.getY(),
                            velocityVector[2] + self.shipNodePath.getZ())
            if distance <=  10:
                self.wantHpr= self.shipNodePath.getHpr() + Vec3(0,90,0)
                self.state = 2
        elif self.state == 1:
            if self.canShoot and distance < 2*150*(self.baseShip.maxSpeed + 1):
                self.shoot(hisPos)
                self.shoot(hisPos)
                t = threading.Timer(1, self.setCanShoot).start()
                self.canShoot = False
            forwardVec = self.shipNodePath.getQuat().getForward()
            ratio = self.baseShip.maxSpeed * 0.3
            velocityVector = forwardVec * ratio
            self.shipNodePath.setPos(  velocityVector[0] + self.shipNodePath.getX(),
                            velocityVector[1] + self.shipNodePath.getY(),
                            velocityVector[2] + self.shipNodePath.getZ())
            #self.shipNodePath.setPos(  self.shipNodePath, forwardVec * ratio)

            if hChange > self.POS_STATECHANGE_ANGLE or hChange < -self.POS_STATECHANGE_ANGLE:
                self.state = 0
            if pChange > self.POS_STATECHANGE_ANGLE or pChange < -self.POS_STATECHANGE_ANGLE:
                self.state = 0
            if rChange > self.POS_STATECHANGE_ANGLE or rChange < -self.POS_STATECHANGE_ANGLE:
                self.state = 0
            if distance <=  70:
                self.wantHpr= self.shipNodePath.getHpr() + Vec3(0,90,0)
                self.state = 2
        elif self.state == 2:
            targetHpr = self.wantHpr - currentHpr

            hclose = False
            pclose = False
            rclose = False

            if targetHpr[0] > self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setH(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
            elif targetHpr[0]< -self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setH(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
            else:
                hclose = True

            if targetHpr[1] > self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setP(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
            elif targetHpr[1]< -self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setP(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
            else:
                pclose = True

            if targetHpr[2] > self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setR(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
            elif targetHpr[2]< -self.POS_STATECHANGE_ANGLE:
                self.shipNodePath.setR(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
            else:
                rclose = True

            #print hclose, pclose, rclose
            if hclose and pclose and rclose:
                self.state = 3
                self.evasionH = 0#self.shipNodePath.getH() + 45
                self.evasionGoal = 45
                self.evasionState = 0

            forwardVec = self.shipNodePath.getQuat().getForward()
            ratio = self.baseShip.maxSpeed * 0.4
            velocityVector = forwardVec * ratio
            self.shipNodePath.setPos(  velocityVector[0] + self.shipNodePath.getX(),
                            velocityVector[1] + self.shipNodePath.getY(),
                            velocityVector[2] + self.shipNodePath.getZ())
        elif self.state == 3:
            #print "instate3"
            self.hasTarget = False
            if distance >= 200:
                self.state = 0
            forwardVec = self.shipNodePath.getQuat().getForward()
            ratio = self.baseShip.maxSpeed
            velocityVector = forwardVec * ratio
            if self.evasionState == 0:
                self.shipNodePath.setP(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
                self.evasionH += self.baseShip.getMaxAnglePerFrame()
                #anglediff = fabs( self.shipNodePath.getP() - self.evasionH )
                #print self.evasionH
                if self.evasionH > self.evasionGoal:
                    self.evasionState = 1
                    self.evasionGoal = -45
            elif self.evasionState == 1:
                self.shipNodePath.setP(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
                self.evasionH -= self.baseShip.getMaxAnglePerFrame()
                if self.evasionH < self.evasionGoal:
                    self.evasionState = 0
                    self.evasionGoal = 45
            #self.shipNodePath.setH(self.shipNodePath, sign1 *self.baseShip.getMaxAnglePerFrame())
            #self.shipNodePath.setP(self.shipNodePath, sign2 *self.baseShip.getMaxAnglePerFrame())
            #self.shipNodePath.setR(self.shipNodePath, sign3 *self.baseShip.getMaxAnglePerFrame())
            self.shipNodePath.setPos(  velocityVector[0] + self.shipNodePath.getX(),
                            velocityVector[1] + self.shipNodePath.getY(),
                            velocityVector[2] + self.shipNodePath.getZ())
        else:
            pass

        return task.again
