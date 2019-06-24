from direct.task import Task
from math import *
from pandac.PandaModules import Quat
from pandac.PandaModules import VBase3
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *

class AIDumb():
    UID = 0
    def __init__(self, baseShip):
        self.baseShip = baseShip
        self.shipNodePath = self.baseShip.getShipModel()
        AIDumb.UID += 1
        self.tempID = AIDumb.UID
        taskMgr.doMethodLater(.01, self.moveTask, 'AIMoveTask' + str(self.tempID))
        self.target = render.find("**/player")
    def cleanUp( self ) :
        taskMgr.remove('AIMoveTask' + str(self.tempID))
        del self.baseShip
        del self.target
        del self.tempID
    def moveTask(self, task):
        #MAX_ANGLE_OF_TURN = .33
        ANGLE_FUDGE = 3
        # Get the current orientation, as a hpr
        currentHpr = self.shipNodePath.getHpr()

        # Get the orientation needed to face the target
        self.shipNodePath.lookAt(self.target)
        targetHpr = self.shipNodePath.getHpr()
        self.shipNodePath.setHpr(currentHpr)

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
            self.shipNodePath.setH(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
        elif hChange < -ANGLE_FUDGE:
            self.shipNodePath.setH(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
        else:
            pass #No change to heading

        if pChange > ANGLE_FUDGE:
            self.shipNodePath.setP(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
        elif pChange < -ANGLE_FUDGE:
            self.shipNodePath.setP(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
        else:
            pass #No change to pitch

        if rChange > ANGLE_FUDGE:
            self.shipNodePath.setR(self.shipNodePath, self.baseShip.getMaxAnglePerFrame())
        elif rChange < -ANGLE_FUDGE:
            self.shipNodePath.setR(self.shipNodePath, -self.baseShip.getMaxAnglePerFrame())
        else:
            pass #No change to heading


        self.speed = self.baseShip.getMaxSpeed()

        self.velocityVector = self.shipNodePath.getQuat().getForward() * self.speed
        self.shipNodePath.setPos(  self.velocityVector[0] + self.shipNodePath.getX(),
                            self.velocityVector[1] + self.shipNodePath.getY(),
                            self.velocityVector[2] + self.shipNodePath.getZ())

        return task.again
