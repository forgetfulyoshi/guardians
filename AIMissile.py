from direct.task import Task
from math import *
from pandac.PandaModules import Quat
from pandac.PandaModules import VBase3
from pandac.PandaModules import *
from direct.showbase.PythonUtil import *
import GameManager
class AIMissile() :
    UID = 0
    def __init__(self, missileData):
        #self.baseMissile = missile
        AIMissile.UID +=1
        self.tempID = AIMissile.UID
        taskMgr.doMethodLater(.01, self.moveTask, 'MissileMoveTask' + str(self.tempID))
        self.missileData = missileData
        self.missileNodePath = self.missileData.getModelData()
        #GameManager.EntityMgr.add( self )
    def cleanUp( self ) :
       # print 'Missile Destruction in AIMissile'
        #del self.missileNodePath
        self.missileNodePath.removeNode()
        taskMgr.remove('MissileMoveTask' + str(self.tempID))
        self.missileData.cleanUp()
        del self.missileData

    def moveTask(self, task):


     if self.missileData.lifetime <= 0 :
            self.missileData.isDead = True
            if self.missileNodePath:
                if not self.missileNodePath.isEmpty():
                    self.missileNodePath.hide()
            #self.missileNodePath.hide()
            #self.missileNodePath.hide()
            return
     else :
        MAX_ANGLE_OF_TURN = .6
        ANGLE_FUDGE = 3
        # Get the current orientation, as a hpr
        currentHpr = self.missileNodePath.getHpr()

        # Get the orientation needed to face the target
        self.missileNodePath.lookAt(self.missileData.getTarget())
        targetHpr = self.missileNodePath.getHpr()
        self.missileNodePath.setHpr(currentHpr)

        # Make sure the hpr's are both on the same side of the circle.
        targetHpr = VBase3(fitDestAngle2Src(currentHpr[0], targetHpr[0]),
                            fitDestAngle2Src(currentHpr[1], targetHpr[1]),
                            fitDestAngle2Src(currentHpr[2], targetHpr[2]))


        # Now rotate a bit torwards the target.        
        if (-180 < self.missileNodePath.getR(self.missileData.getTarget()) and self.missileNodePath.getR(self.missileData.getTarget()) <= -90) or (90 < self.missileNodePath.getR(self.missileData.getTarget()) and self.missileNodePath.getR(self.missileData.getTarget()) <= 180):
            hprChange = (currentHpr - targetHpr)
        elif (-90 < self.missileNodePath.getR(self.missileData.getTarget()) and self.missileNodePath.getR(self.missileData.getTarget()) <= 0) or (0 < self.missileNodePath.getR(self.missileData.getTarget()) and self.missileNodePath.getR(self.missileData.getTarget()) <= 90) :
            hprChange =(targetHpr - currentHpr)                      

        #set them component wise because you should angle me able to make
        #a certain angle of turn per frame
        hChange = hprChange[0]
        pChange = hprChange[1]
        rChange = hprChange[2]

        if hChange > ANGLE_FUDGE:
            hChange = MAX_ANGLE_OF_TURN
            #self.missileNodePath.setH(self.missileNodePath, MAX_ANGLE_OF_TURN)
        elif hChange < -ANGLE_FUDGE:
            hChange = -MAX_ANGLE_OF_TURN
            #self.missileNodePath.setH(self.missileNodePath, -MAX_ANGLE_OF_TURN)
        else:
            pass #No change to heading

        if pChange > ANGLE_FUDGE:
            pChange = MAX_ANGLE_OF_TURN
            #self.missileNodePath.setP(self.missileNodePath, MAX_ANGLE_OF_TURN)
        elif pChange < -ANGLE_FUDGE:
            pChange = -MAX_ANGLE_OF_TURN
            #self.missileNodePath.setP(self.missileNodePath, -MAX_ANGLE_OF_TURN)
        else:
            pass #No change to pitch

        if rChange > ANGLE_FUDGE:
            rChange = MAX_ANGLE_OF_TURN
            #self.missileNodePath.setR(self.missileNodePath, MAX_ANGLE_OF_TURN)
        elif rChange < -ANGLE_FUDGE:
            rChange = -MAX_ANGLE_OF_TURN
            #self.missileNodePath.setR(self.missileNodePath, -MAX_ANGLE_OF_TURN)
        else:
            pass #No change to roll
        
        changeQuat = Quat()
        changeQuat.setHpr(VBase3(hChange, pChange, rChange))
        
        
        self.missileNodePath.setQuat(changeQuat * self.missileNodePath.getQuat())

        self.speed = self.missileData.getSpeed()

        self.velocityVector = self.missileNodePath.getQuat().getForward() * self.speed
        self.missileNodePath.setPos(self.velocityVector[0] + self.missileNodePath.getX(),
                                    self.velocityVector[1] + self.missileNodePath.getY(),
                                    self.velocityVector[2] + self.missileNodePath.getZ())
        
        self.missileData.lifetime -= 1
        return task.again
