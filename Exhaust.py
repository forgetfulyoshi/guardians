from pandac.PandaModules import *
import copy
from direct.gui.OnscreenImage import OnscreenImage
import random

class Exhaust():
    RANGE_MIN = 40
    RANGE_MAX = 150
    ARRAY_MAX = RANGE_MAX - RANGE_MIN
    textureList = []

    ID = 0
    for x in range(RANGE_MIN,RANGE_MAX):
        if x < 100:
            textureList.append( loader.loadTexture("Art/textures/exhaustsprite/exhaust00" + str(x) + ".png"))
        else:
            textureList.append( loader.loadTexture("Art/textures/exhaustsprite/exhaust0" + str(x) + ".png"))
    def __init__(self, parentNode, scale):
        self.id = copy.copy(self.ID)
        Exhaust.ID += 1
        self.myNode = loader.loadModel('Art/exhaust2.bam')
        self.myNode.reparentTo(parentNode)
        self.myNode.setPos(0,.1,0)
        self.myNode.setScale(scale)
        self.myNode.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
        #self.myNode.setDepthTest(False)
        self.myNode.setDepthWrite(False)
        self.myNode.setBin("fixed",2)

        self.inside = self.myNode.find("**/inside")
        self.outside = self.myNode.find("**/outside")


        #self.inside.setTexture(self.textureList[0])
        #self.outside.setTexture(self.textureList[0])
        #self.inside.setBin("fixed",2)
        #self.outside.setBin("fixed",3)
        self.currentAnim = random.randint(0, self.ARRAY_MAX-1)
        self.rotateAngle = random.randint(0,360)
        self.animDir = 1
        taskMgr.doMethodLater(.05, self.animFunc, 'exhaust' + str(self.id))

    def animFunc(self,task):
        if self.animDir == 1:
            self.currentAnim += 1
            if self.currentAnim >= self.ARRAY_MAX:
                self.currentAnim -= 1
                self.animDir = 2
        else:
            self.currentAnim -= 1
            if self.currentAnim <= -1:
                self.currentAnim += 1
                self.animDir = 1

        self.rotateAngle += .5
        if self.rotateAngle >= 360:
            self.rotateAngle = 0

        #self.myNode.setTexture(self.textureList[self.currentAnim])
        self.inside.setTexture(self.textureList[self.currentAnim],1)
        self.outside.setTexture(self.textureList[self.currentAnim],1)
        self.outside.setR(self.rotateAngle)
        self.inside.setR(self.rotateAngle)
        #self.outside.setTexRotate(TextureStage.getDefault(), self.rotateAngle);


        return task.again

    def cleanUp(self):

        taskMgr.remove('exhaust' + str(self.id))
        del self.id

        self.myNode.removeNode()
        self.inside.removeNode()
        self.outside.removeNode()

        #for texture in self.textureList:
            #texture.clear()
