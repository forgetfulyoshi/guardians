
from pandac.PandaModules import *
from math import *
from direct.showbase import DirectObject


class ball(DirectObject.DirectObject):
    def __init__(self, speed, direction, type, ballNum):
        self.speed = speed
        self.direction = direction #in degrees
        self.type = type #color of ball 0-2 Yellow, Cue, EightBall
        self.ballNum = ballNum
        self.sound = loader.loadSfx("sound35.mp3")
    
        model = loader.loadModel("balls.bam")
        one = model.find("**/one")
        cueball = model.find("**/cueball")
        eight = model.find("**/eight")
        if self.type == 0:
            self.activeBall = one
            cueball.hide()
            eight.hide()
        elif self.type == 1:
            self.activeBall = cueball
            one.hide()
            eight.hide()
        elif self.type == 2:
            self.activeBall = eight
            one.hide()
            cueball.hide()
        ballNode = render.find("**/ballNode")
        self.activeBall.reparentTo(ballNode)
        self.activeBall.setPos(0,0,3.99)
        self.activeBall.setScale(.4)
        
        cs = CollisionSphere(0,0,0,1)
        self.cnodePath = self.activeBall.attachNewNode(CollisionNode('ball%d' % (self.ballNum)))
        self.cnodePath.node().addSolid(cs)

        #messenger
        self.accept('collide',self.handleCollide)
		
    def getSpeed(self):
    	return self.speed
             
    def motion(self):

        xvalue = cos(radians(self.direction))
        yvalue = sin(radians(self.direction))

        xdelta = xvalue * self.speed
        ydelta = yvalue * self.speed

        currentX = self.activeBall.getX()
        currentY = self.activeBall.getY()

        self.activeBall.setX(currentX + xdelta)
        self.activeBall.setY(currentY + ydelta)
        
        currentRoll = self.activeBall.getR()
        self.activeBall.setR(currentRoll + 8)


    def handleCollide(self, collisionEntry):
        if self.cnodePath.getName() == collisionEntry.getFromNodePath().getName(): 
            intoPath = collisionEntry.getIntoNodePath().getName()
            if intoPath == "wallleft" or intoPath == "wallright":
                self.direction = degrees(atan2( radians(sin(radians(self.direction))),
                                                radians(cos(radians(180+self.direction)))))
                self.sound.play()
                self.activeBall.setH(self.direction)
            elif intoPath == "walltop" or intoPath == "wallbottom":
                self.direction = degrees(atan2( radians(sin(radians(180+self.direction))),
                                                radians(cos(radians(self.direction)))))
                self.sound.play()
                self.activeBall.setH(self.direction)
            else: #collided with another ball not a Wall
				
            	if self.cnodePath == collisionEntry.getIntoNodePath():	
            		otherBall = collisionEntry.getFromNodePath()
            	else:
            		otherBall = collisionEntry.getIntoNodePath()
            	
            	otherBallX = cos(radians(otherBall.getH()))
            	otherBallY = sin(radians(otherBall.getH()))
            	
            	thisBallX = cos(radians(180+self.direction))
            	thisBallY = sin(radians(180+self.direction))
            	
            	self.direction = degrees(atan2( otherBallY + thisBallY,
            									otherBallX + thisBallX))
            									
            	self.sound.play()
            	self.activeBall.setH(self.direction)