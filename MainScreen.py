from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
import config

class MainScreen(DirectObject.DirectObject):
    def __init__(self, baseShip, screenNode):
        self.screenNode = screenNode
        self.baseShip = baseShip
        
        mainWindow = base.win
        
        self.altBuffer = mainWindow.makeTextureBuffer("mainScreen", 512, 512)
        self.altRender = NodePath("mainscreen")
        
        self.altCam = base.makeCamera(self.altBuffer)
        self.altCam.reparentTo(self.altRender)
        self.altCam.setPos(0,-3,0)
        
        self.setupScreen()
        
        self.screenNode.setTexture( self.altBuffer.getTexture() ,1)
        
        taskMgr.doMethodLater(.3, self.manageScreen, 'TargetScreen')
    def setupScreen(self):
        self.tempText = TextNode('tempText')
        self.tempText.setText("MainWindowTemp")
        self.tempText.setTextColor(config.TEXT_COLOR)
        self.tempTextNodePath = self.altRender.attachNewNode(self.tempText)
        self.tempTextNodePath.setPos(-.75,0,0)
        self.tempTextNodePath.setScale(.22)
        
        
        self.backImage = OnscreenImage(image = 'Art/textures/blades.png',
                                        pos = (-1,1,-1),
                                        scale = 5,
                                        color = (0,0,0,1),
                                        parent = self.altRender)
        self.backImage.setTransparency(TransparencyAttrib.MAlpha)
        self.backImage.setColor(0,0,0,.98)
    def manageScreen(self, task):
        return task.again
        
    def cleanUp(self):
        del self.screenNode
        del self.baseShip
        taskMgr.remove('TargetScreen')