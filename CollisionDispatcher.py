from pandac.PandaModules import *
from direct.showbase import DirectObject
import config
from random import *

import GameManager

class CollisionDispatcher(DirectObject.DirectObject):
    def __init__(self):
        self.accept("collide", self.handleCollision)
        #Dictionary of Dictionaries
        self.collidables = {'bullet' : {},
                            'missile': {},
                            'ship'   : {},
                            'cockpit' : {},
                            'other'   : {},
                            }
    #all of the fun logic will go down here
    def handleCollision(self, collisionEntry):
        
        #print "Collision"
        isRay = False
        fromNode = collisionEntry.getFromNodePath()
        intoNode = collisionEntry.getIntoNodePath()
        
        fromType = fromNode.getNetTag("type")
        fromId = fromNode.getNetTag("id")
        #print fromType
        if fromType == "targetRay":
            #messenger.send("targetPicked",[fromNode, id])
            isRay = True
        fromCollisionType = fromNode.getNetTag("collisionType")
        if isRay == False:
            if self.collidables[fromType].has_key(fromId):
                fromClassReference = self.collidables[fromType][fromId]
                location = fromNode.getNetTag("location")
            else:
                return
        
        intoType = intoNode.getNetTag("type")
        intoId = intoNode.getNetTag("id")
        intoCollisionType = intoNode.getNetTag("collisionType")
        
        
        if isRay and intoType == 'other':
            return
        if self.collidables[intoType].has_key(intoId):
            intoClassReference = self.collidables[intoType][intoId]
        else:
            return
        if isRay and intoType != 'cockpit':
            messenger.send("targetPicked",[intoNode.getParent().getParent(), intoId])
        
        if ((fromCollisionType == "from") and (intoCollisionType == "from")):
            if fromType == "cockpit":
                if intoType == "other":
                    GameManager.OtherCollideWithCockpit( fromClassReference,
                                                        intoClassReference,
                                                        location,
                                                        )
                    print "OTHERCOLLIDEWITHCOCKPIT!"
                    return
                if intoType == "ship":
                    GameManager.ShipCollideWithCockpit(fromClassReference, intoClassReference, location)
                    return
        if fromType == "other" and not intoType == "cockpit":
            if intoType == "bullet":
                GameManager.OtherCollideWithBullet(fromClassReference, intoClassReference)
            elif intoType == "missile":
                GameManager.OtherCollideWithMissile(fromClassReference, intoClassReference)
            elif intoType == "other":
                GameManager.OtherCollideWithOther(fromClassReference, intoClassReference)
            elif intoType == "figureitoutlater":
                pass #other vs AI, other,     
            else:
                return # Ship collides with cockpit.. special case
            #Missiles/guns ect are into colliders
        
        if fromType == "ship" and intoType == "bullet":
            GameManager.BulletHit( fromClassReference , intoClassReference , location)
        if fromType == 'ship' and intoType == 'missile' :
            GameManager.MissileHit( fromClassReference , intoClassReference, location)
        if fromType == 'cockpit' and intoType == "bullet":
            GameManager.CockpitBulletHit( fromClassReference , intoClassReference, location)
        if fromType == 'ship' and intoType == 'ship':
            if intoId != fromId:
                GameManager.ShipCollideWithShip(fromClassReference, intoClassReference)
            
    
        ##handle collision depending on types