#Missle.py
#Programmers : Eric Ranaldi
#Created : 12/22/2008

from pandac.PandaModules import *

class BaseMissile :
    def __init__(self, missleType ) :
        self.isDead = False
        if missleType == 'homingmissile' :

            self.lifetime   = 1000
            self.speed      = 1.1 #tempDATASPOT
            self.maxSpeed   = 10
            self.targetID   = 0 #EnemyShipID
            self.ownerID    = 0 #OwnerShipID
            self.maxDMG     = 50
            self.tracking   = 0
            
            self.ModelData = loader.loadModel("Art/missile3.bam")
            #locator = self.ModelData.find("**/locator1")
            #b
        
        elif missleType == 'heatmissile' :            
            self.lifetime   = 1000
            self.speed      = .5
            self.maxSpeed   = 1
            self.targetID   = 0 #EnemyShipID
            self.ownerID    = 0 #OwnerShipID
            self.maxDMG     = 13
            self.tracking   = 0
            
            self.ModelData = loader.loadModel("Art/missile3.bam")
        else :
            print 'ERROR: No such missile'
            return
         
    #Accessor functions for the values of a missle        
    def setSpeed( self , tempSpeed ) : self.speed = tempSpeed
    def setMaxSpeed( self , tempmSpeed ) : self.maxSpeed = tempmSpeed
    def setTarget( self , tempEnemyShipID ) : self.targetID = tempEnemyShipID
    def setOwner( self , tempOwnerID ) : self.ownerID = tempOwnerID
    def setMaxDamage( self , tempMaxDMG ) : self.maxDMG = tempMaxDMG
    def setTracking( self , tempTracking ) : self.tracking = tempTracking
    def setModelData(self, tempName ) : self.ModelData = loader.loadModel(tempName)
    def setDead( self ) :
        if self.isDead == False :
           self.isDead = True
        else :
            self.isDead = False
    
    def getSpeed( self ) : return self.speed
    def getMaxSpeed( self ) : return self.maxSpeed
    def getTarget( self ) : return self.targetID
    def getOwner( self ) : return self.ownerID
    def getMaxDamage( self ) : return self.maxDMG
    def getTracking( self ) : return self.tracking
    def getModelData( self ) : return self.ModelData
    def getDead( self ) : return self.isDead
        
    def cleanUp( self ) :
        #print 'missile destruction in BaseMissile'
        self.ModelData.removeNode()
        del self.ModelData
        del self.lifetime   
        del self.speed      
        del self.maxSpeed   
        del self.targetID   
        del self.ownerID    
        del self.maxDMG     
        del self.tracking
        del self.isDead