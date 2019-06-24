#!/usr/bin/env python
from pandac.PandaModules import *
from direct.showbase import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *
from direct.task import Task


class LoadingScreen(DirectObject.DirectObject):
    LOWEST_WAIT_TIME = 1
    def __init__(self):
        #self.image = loader.loadTexture('Art/textures/loading1.egg')
        self.loading1 = loader.loadModel('Art/loading1.bam')
        self.bg = self.loading1.find("**/bg1")
        self.front = self.loading1.find("**/fr")
        self.hourglass = self.loading1.find("**/hourglass")
        
        
        self.loadingNode = aspect2d.attachNewNode("LoadingNode")
        self.bg.reparentTo(self.loadingNode)
        self.front.reparentTo(self.loadingNode)
        self.hourglass.reparentTo(self.loadingNode)
        
        self.front.setScale(.6,1,.35)
        self.bg.setScale(.9,1,1)
        self.hourglass.setPos(0,0,-.2)
        self.hourglass.setScale(.08)
        
        self.endSequence = Sequence()
        self.endSequence.append(Wait(self.LOWEST_WAIT_TIME))
        self.endSequence.start()
        
        self.hourglassT = taskMgr.doMethodLater(.03, self.hourglassTask, 'hourglassTask')
        #self.hourglassSeq = Sequence()
        #self.endSequence.append(Func(self.finished))
    def finished(self):
        if self.endSequence.isPlaying():
            self.endSequence.pause()
            self.endSequence.append(Func(self.finished))
            self.endSequence.start()
            return
        
        taskMgr.remove(self.hourglassT)
        self.loadingNode.hide()
        #aspect2d.ls()
        
    def hourglassTask(self,task):
        self.hourglass.setR(self.hourglass, 3)
        return task.again
    
    def cleanUp(self):
        self.loadingNode.removeNode()