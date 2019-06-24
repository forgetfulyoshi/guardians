from pandac.PandaModules import *

class TargetHologram():
    def __init__(self, hologramNodePath):
        self.hologramNode = hologramNodePath
        self.targetNode = self.hologramNode.attachNewNode("holotarget")
        self.hologramNode.setScale(.4)
        
    def clearTarget(self):
        self.targetNode.getChild().removeNode()
    def setTarget(self, target):
        if self.targetNode.getChildrenAsList() != []:
            for x in self.targetNode.getChildrenAsList():
                x.removeNode()
        self.currentTarget = target.copyTo(self.targetNode)
        self.currentTarget.find("**/cnode").removeNode()
        self.currentTarget.setPos(0,-3,.85)
        self.currentTarget.setHpr(0,0,0)
        self.currentTarget.hprInterval(6, Point3(360,0,0)).loop()
        self.currentTarget.setColor(0,.9,.1,.5)
        self.currentTarget.setTransparency(TransparencyAttrib.MAlpha)

        