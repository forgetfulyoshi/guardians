from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *


from Menu import *
from InGameMenu import *
from MissionFailedMenu import *
from SoundHandler import *
from FileHandler import *
from LoadingScreen import *
from ZoneHandler import *
from AIPlayer import *
from Entity import EntityManager
from Explosion import *


import pygame


import gc

EntityMgr = EntityManager()

class GameManager(DirectObject.DirectObject):
    def __init__(self):
        base.disableMouse()
        base.win.setClearColor(Vec4(0,0,0,1))
        #self.mainmenu = MainMenu()
        self.fileHandler = FileHandler()
        self.zoneHandler = ZoneHandler(self.fileHandler)
        self.soundHandler = SoundHandler()

        EntityMgr.start()

        self.inGameMenu = InGameMenu()
        self.missionFailedMenu = MissionFailedMenu()

        self.accept("startgame", self.startGame)
        self.accept("ingamemenu", self.createInGameMenu)
        self.accept("missionfailedmenu", self.createMissionFailedMenu)
        self.accept("missionfailedexittomenu", self.exitToMenu)
        self.accept("exittomenu", self.exitToMenu)
        self.accept("missionfailedrestart", self.restartGame)
        self.accept("restart", self.restartGame)
        self.createMenu()


        #taskMgr.popupControls()

    def createMenu(self):
        print "CREATE MENU"
        self.mainMenu = MainMenu(self.soundHandler)


    def createInGameMenu(self):
        print "CREATE IN-GAME MENU"
        self.inGameMenu.display()

    def createMissionFailedMenu(self, text):
        print "CREATE MISSION FAILED MENU"
        self.missionFailedMenu.display(text)

    def startGame(self, zoneName):
        print "START GAME"
        print EntityManager.list
        self.zoneHandler.request(zoneName)


    def restartGame(self):
        print "RESTART GAME"
        self.cleanUp()
        self.startGame(self.zoneHandler.getCurrentOrNextState())

    def exitToMenu(self):
        print "EXIT TO MENU"
        self.cleanUp()
        self.zoneHandler.demand("Dummy") #Force the FSM to exit from the current Zone
        #self.zoneHandler.cleanup() #This is only causing problems
        self.createMenu()

    def cleanUp(self):
        print "GAME MANAGER CLEANUP"
        #Basicly, stuff is getting added to the list even while we remove stuff from it.
        #This makes sure that the list is empty and everything is deleted before moving on
        while len(EntityMgr.list) > 0:
            EntityMgr.cleanUpAI()




def BulletHit( fromClassReference , intoClassReference , location) :

        deadflag = False
        if location == 'col_front':
            fromClassReference.ship.frontHull -= intoClassReference.getDmg()
            if fromClassReference.ship.frontHull <= 0:
                deadflag = True
        elif location == 'col_back':
            fromClassReference.ship.backHull -= intoClassReference.getDmg()
            if fromClassReference.ship.backHull <= 0:
                deadflag = True
        elif location == 'col_left':
            fromClassReference.ship.leftHull -= intoClassReference.getDmg()
            if fromClassReference.ship.leftHull <= 0:
                deadflag = True
        elif location == 'col_right':
            fromClassReference.ship.rightHull -= intoClassReference.getDmg()
            if fromClassReference.ship.rightHull <= 0:
                deadflag = True
        if deadflag == True:
            fromClassReference.isDead = True
            Explosion(fromClassReference.shipModel.getPos(render),1)
            #newAI = AIPlayer('dumb' , 'pointless' , Vec3(400 , 500 , 0) )
        intoClassReference.lifetime = -1
        intoClassReference.isDead = True
            #intoClassReference.lifetime = 0

def MissileHit( fromClassReference , intoClassReference ,location) :

        deadflag = False
        if location == 'col_front':
            fromClassReference.ship.frontHull -= intoClassReference.getDmg()
            if fromClassReference.ship.frontHull <= 0:
                deadflag = True
        elif location == 'col_back':
            fromClassReference.ship.backHull -= intoClassReference.getDmg()
            if fromClassReference.ship.backHull <= 0:
                deadflag = True
        elif location == 'col_left':
            fromClassReference.ship.leftHull -= intoClassReference.getDmg()
            if fromClassReference.ship.leftHull <= 0:
                deadflag = True
        elif location == 'col_right':
            fromClassReference.ship.rightHull -= intoClassReference.getDmg()
            if fromClassReference.ship.rightHull <= 0:
                deadflag = True
        if deadflag == True:
            fromClassReference.isDead = True
            Explosion(fromClassReference.shipModel.getPos(render),1)
            #newAI = AIPlayer('dumb' , 'pointless' , Vec3(400 , 500 , 0) )
        intoClassReference.missileData.lifetime = -1
        intoClassReference.isDead = True

            #newAI = AIPlayer('dumb' , 'pointless' , Vec3(400 , 500 , 0) )=======
def CockpitBulletHit( fromClassReference, intoClassReference, location):
    deadflag = False
    if location == 'col_front':
        fromClassReference.playerShip.frontHull -= intoClassReference.getDmg()
        if fromClassReference.playerShip.frontHull <= 0:
            deadflag = True
    elif location == 'col_back':
        fromClassReference.playerShip.backHull -= intoClassReference.getDmg()
        if fromClassReference.playerShip.backHull <= 0:
            deadflag = True
    elif location == 'col_left':
        fromClassReference.playerShip.leftHull -= intoClassReference.getDmg()
        if fromClassReference.playerShip.leftHull <= 0:
            deadflag = True
    elif location == 'col_right':
        fromClassReference.playerShip.rightHull -= intoClassReference.getDmg()
        if fromClassReference.playerShip.rightHull <= 0:
            deadflag = True
    if deadflag == True:
        print "YOU DIED LOSER!"
        #fromClassReference.isDead = 'true'
        #newAI = AIPlayer('dumb' , 'pointless' , Vec3(400 , 500 , 0) )
        messenger.send("youdied")
    intoClassReference.lifetime = -1
    intoClassReference.isDead = True
        #intoClassReference.lifetime = 0

def ShipCollideWithCockpit(fromClassReference, intoClassReference, location):
    print "SHIPCOLLIDEWITHCOCKPIT"
    if intoClassReference.type == "battleship":
        fromClassReference.playerShip.frontHull =  0
        fromClassReference.playerShip.backHull  =  0
        fromClassReference.playerShip.leftHull  =  0
        fromClassReference.playerShip.rightHull =  0
    else:
        if location == 'col_front':
            fromClassReference.playerShip.frontHull -= intoClassReference.ship.blowupDamage
        elif location == 'col_back':
            fromClassReference.playerShip.backHull -= intoClassReference.ship.blowupDamage
        elif location == 'col_left':
            fromClassReference.playerShip.leftHull -= intoClassReference.ship.blowupDamage
        elif location == 'col_right':
            fromClassReference.playerShip.rightHull -= intoClassReference.ship.blowupDamage
        intoClassReference.isDead = True
    isPlayerDead(fromClassReference)
def isPlayerDead(player):
    if player.playerShip.frontHull <= 0:
        messenger.send("youdied")
        return
    if player.playerShip.backHull <= 0:
        messenger.send("youdied")
        return
    if player.playerShip.leftHull <= 0:
        messenger.send("youdied")
        return
    if player.playerShip.rightHull <= 0:
        messenger.send("youdied")
        return
def ShipCollideWithShip(fromClassReference, intoClassReference):
    fromClassReference.isDead = True
    intoClassReference.isDead = True
def OtherCollideWithCockpit( fromClassReference, intoClassReference, location):
    print "Collided with cockpit"

    print "FROM  ", fromClassReference, "INTO  ", intoClassReference, " LOCATION:  ", location
    #intoClassReference.otherCollideWithCockpit()
    if intoClassReference.type == "pod":
        intoClassReference.otherCollideWithCockpit()
        if location == 'col_front':
            fromClassReference.playerShip.frontHull -= 40
        elif location == 'col_back':
            fromClassReference.playerShip.backHull -= 40
        elif location == 'col_left':
            fromClassReference.playerShip.leftHull -= 40
        elif location == 'col_right':
            fromClassReference.playerShip.rightHull -= 40

        fromClassReference.flightHandler.setThrottle(0)
        #fromClassReference.flightHandler.velocityVector.normalize()
        #fromClassReference.flightHandler.velocityVector *=
    elif intoClassReference.type == "comet":
        intoClassReference.otherCollideWithCockpit()
        if location == 'col_front':
            fromClassReference.playerShip.frontHull -= intoClassReference.DMG
        elif location == 'col_back':
            fromClassReference.playerShip.backHull -= intoClassReference.DMG
        elif location == 'col_left':
            fromClassReference.playerShip.leftHull -= intoClassReference.DMG
        elif location == 'col_right':
            fromClassReference.playerShip.rightHull -= intoClassReference.DMG
    elif intoClassReference.type == "plane":
        intoClassReference.otherCollideWithCockpit()
        
    
    isPlayerDead(fromClassReference)


def OtherCollideWithBullet( other, bullet):
    other.bulletCollide(bullet)

    bullet.lifetime = -1
    bullet.isDead = True

def OtherCollideWithMissile( other, missile):
    missile.lifetime = -1
    missile.isDead = True

def OtherCollideWithOther( fromOther, intoOther):
    if fromOther.id != intoOther.id:
        fromOther.otherCollide(intoOther)
        intoOther.otherCollide(fromOther)
