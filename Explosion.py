from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
import copy

class Explosion(DirectObject.DirectObject):
    ID = 0
    textureList = []
    for x in range(2,70):
        if x < 10:
            textureList.append(loader.loadTexture("Art/textures/explosionsprite/explosion000" + str(x) + ".png"))
        else:
            textureList.append(loader.loadTexture("Art/textures/explosionsprite/explosion00" + str(x) + ".png"))
    def __init__(self, pos, type):
        self.myNode = render.attachNewNode("explosion" + str(self.ID))
        self.id = copy.copy(self.ID)
        self.myNode.setPos(pos)
        if type == 0: #asteroid
            self.myNode.setScale(11)
        elif type == 1: #ship
            self.myNode.setScale(15)
        self.ID += 1
        
        
        self.currentTexture = 0    
        self.explosion = OnscreenImage('Art/textures/explosionsprite/explosion0020.png')
        self.explosion.setTransparency(TransparencyAttrib.MAlpha)
        self.explosion.reparentTo(self.myNode)
        self.explosion.setBillboardPointEye()
        self.explosion.setDepthWrite(False)
        self.explosion.setBin("fixed",2)
        
        taskMgr.doMethodLater(0.033, self.cycleTexture, 'explosion' + str(self.ID))
        messenger.send('playSfx', ['shipDestroyed'])
    def cleanUp(self):
        self.myNode.removeNode()
        taskMgr.remove("explosion"+ str(self.id))
        
    def cycleTexture(self, task):
        self.currentTexture += 1
        if self.currentTexture >= len(self.textureList)-1:
            self.cleanUp()
            return
        else:
            self.explosion.setTexture(self.textureList[self.currentTexture])
        
        return task.again

