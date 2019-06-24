from pandac.PandaModules import *

from CollisionDispatcher import *
import config

class Collidable():
    dispatcher = CollisionDispatcher()

    def __init__(self, classReference, nodePath, tag):
        if tag == "bullet":
            x = str(config.nextBulletID)
            classReference.id = config.nextBulletID
            self.dispatcher.collidables[tag][x] = classReference
            config.nextBulletID += 1
        elif tag == "cockpit":
            x = str(config.nextCockpitID)
            classReference.id = config.nextCockpitID
            self.dispatcher.collidables[tag][x] = classReference
            config.nextCockpitID += 1
        elif tag == "ship":
            x = str(config.nextShipID)
            classReference.id = config.nextShipID
            self.dispatcher.collidables[tag][x] = classReference
            config.nextShipID += 1
            print "SHIP ID: ", config.nextShipID
        elif tag == "missile":
            x = str(config.nextMissileID)
            classReference.id = config.nextMissileID
            self.dispatcher.collidables[tag][x] = classReference
            config.nextMissileID += 1
        elif tag == "other":
            x = str(config.nextOtherID)
            classReference.id = config.nextOtherID
            self.dispatcher.collidables[tag][x] = classReference
            config.nextOtherID += 1
        else:
            pass
        
    def removeFromCollidables(self, id, tag):
        if self.dispatcher.collidables[tag].has_key(str(id)):
            del self.dispatcher.collidables[tag][str(id)]
