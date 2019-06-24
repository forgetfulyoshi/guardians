import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.task import Task
from ball import *
from math import *
from CameraHandler import *


####Load up Basic models
skybox = loader.loadModel("backbox1.bam")
skybox.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
skybox.reparentTo(render)

table = loader.loadModel("warshow.bam")
table.setAttrib(CullFaceAttrib.make(CullFaceAttrib.MCullNone))
table.reparentTo(render)
table.setScale(.5)
#######################



###Build the collision handler/traverser
traverser = CollisionTraverser('traverser name')
base.cTrav = traverser
#traverser.addCollider(fromObject, handler)
queue = CollisionHandlerEvent()
#traverser.addCollider(fromObject, queue)
traverser.traverse(render)
queue.addInPattern('collide')
#######################

#Create node to parent balls to
ballNode = render.attachNewNode("ballNode")
ball1 = ball(.1, 25, 2, 0)
traverser.addCollider(ball1.cnodePath, queue)
ball2 = ball(.2, -34, 1, 1)
traverser.addCollider(ball2.cnodePath, queue) 
ball3 = ball(.15, 60, 0, 2)
traverser.addCollider(ball3.cnodePath, queue)
###
#Set up the collision planes 
###
rightPlane = CollisionPlane(Plane(Vec3(-1,0,0), Point3(6,0,3.99)))
rightPlanePath = render.attachNewNode(CollisionNode('wallright'))
rightPlanePath.node().addSolid(rightPlane)
rightPlanePath.show()

leftPlane = CollisionPlane(Plane(Vec3(1,0,0), Point3(-6,0,3.99)))
leftPlanePath = render.attachNewNode(CollisionNode('wallleft'))
leftPlanePath.node().addSolid(leftPlane)
leftPlanePath.show()

bottomPlane = CollisionPlane(Plane(Vec3(0,1,0), Point3(0,-6.5,3.99)))
bottomPlanePath = render.attachNewNode(CollisionNode('wallbottom'))
bottomPlanePath.node().addSolid(bottomPlane)
bottomPlanePath.show()

topPlane = CollisionPlane(Plane(Vec3(0,-1,0), Point3(0,6.5,3.99)))
topPlanePath = render.attachNewNode(CollisionNode('walltop'))
topPlanePath.node().addSolid(topPlane)
topPlanePath.show()
####

axis = loader.loadModel('zup-axis.bam')
axis.reparentTo(render)
axis.setPos(0,0,3.99)



base.disableMouse()
camera = CameraHandler()

def gameTask(task):
    #queue.traverse()
    ball1.motion()
    ball2.motion()
    ball3.motion()
    camera.motion()
    return task.again

gameLoop = taskMgr.doMethodLater(.03,gameTask, 'gameLoop')
run()
