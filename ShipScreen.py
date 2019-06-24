#!/usr/bin/env python

from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
import config

class ShipScreen(DirectObject.DirectObject):
    def __init__(self, baseShip, screenNode):
        self.screenNode = screenNode
        self.screenNode.setTransparency(TransparencyAttrib.MAlpha)
        self.baseShip = baseShip
        
        self.mainWindow = base.win
        
        self.altBuffer = self.mainWindow.makeTextureBuffer("shipScreen", 512, 512)
        self.altRender = NodePath("shipscreen")
        
        self.altCam = base.makeCamera(self.altBuffer)
        self.altCam.reparentTo(self.altRender)
        self.altCam.setPos(0,-3,0)
        
        self.accept("v", base.bufferViewer.toggleEnable)
        self.accept("V", base.bufferViewer.toggleEnable)
        base.bufferViewer.setPosition("llcorner")
        base.bufferViewer.setCardSize(.25, 0.0)
        
        
        self.screenNode.setTexture( self.altBuffer.getTexture() ,1)
        
        taskMgr.doMethodLater(.3, self.manageScreen, 'TargetScreen')
        
        self.shipNode = loader.loadModel("Art/pegasus.bam")
        self.shipNode.reparentTo(self.altRender)
        self.shipNode.setP(90)
        self.shipNode.setPos(0,0,0)
        
        self.shipNode.setScale(.5,.7,.7)


        attrib = RenderModeAttrib.make(2,2)
        self.shipNode.setAttrib(attrib)
        
        self.left = self.shipNode.find("**/left")
        self.right = self.shipNode.find("**/right")
        self.front = self.shipNode.find("**/front")
        self.back = self.shipNode.find("**/back")
        self.windows = self.shipNode.find("**/windows")
        
        self.RED = Vec4(.6,0,0,1)
        self.ORANGE = Vec4(.89,.3,0,1)
        self.YELLOW = Vec4(.89,1,0,1)
        self.GREEN = Vec4(0,1,0,1)
        self.BLUE = Vec4(0,0,1,1)
        
        self.left.setColor(self.BLUE)
        self.right.setColor(self.BLUE)
        self.front.setColor(self.BLUE)
        self.back.setColor(self.BLUE)
        #self.left.setColor(self.RED)
        #self.right.setColor(self.ORANGE)
        #self.front.setColor(self.YELLOW)
        #self.back.setColor(self.BLUE)
        self.windows.setColor(Vec4(0,0,0,1))
        #self.shipNode.setColor(Vec4(.1,.95,.1,1))
    def setColor(self, hp, nodepath):
        if hp >= 81:
            if not nodepath.getColor() == self.BLUE:
                nodepath.setColor(self.BLUE)
        elif hp >= 61:
            if not nodepath.getColor() == self.GREEN:
                nodepath.setColor(self.GREEN)
        elif hp >= 41:
            if not nodepath.getColor() == self.YELLOW:
                nodepath.setColor(self.YELLOW)
        elif hp >= 21:
            if not nodepath.getColor() == self.ORANGE:
                nodepath.setColor(self.ORANGE)
        else:
            if not nodepath.getColor() == self.RED:
                nodepath.setColor(self.RED)
            #if hp <= 0:
                #messenger.send("youdied")

    def manageScreen(self, task):
        leftHull = self.baseShip.leftHull
        rightHull = self.baseShip.rightHull
        frontHull = self.baseShip.frontHull
        backHull = self.baseShip.backHull
        
        self.setColor(leftHull, self.left)
        self.setColor(rightHull, self.right)
        self.setColor(frontHull, self.front)
        self.setColor(backHull, self.back)
        return task.again
    
    def cleanUp(self):
        del self.baseShip
        self.screenNode.removeNode()
        taskMgr.remove('TargetScreen')
        
        self.altCam.removeNode()
        del self.altCam
        
        self.altBuffer.setOneShot(True)
        del self.altBuffer
        
        self.altRender.removeNode()
        del self.altRender
        
        self.ignore("v")
        self.ignore("V")
        