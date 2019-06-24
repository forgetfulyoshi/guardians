class ShipHandler :
    def __init__( self , handleID ) :
         self.handleID = handleID
         self.shipList = []
    def addShip(self, ship) :
        self.shipList.append(ship)
    def delShip(self, ship) :
        self.shipList.remove(ship)
    def getShip(self, shipID) :
        for x in self.shipList:
            if x.UID == shipID :
                return x


class BaseShip :
    UIDKey = 1000
    def __init__( self , name ) :

        if name == 'player-pegasus' :
            if BaseShip.UIDKey >= 1000 :
                self.UID = self.setUid()
            self.name                   = name
            self.missiles               = 25
            self.energy                 = 100
            self.leftHull               = 100
            self.rightHull              = 100
            self.frontHull              = 100
            self.backHull               = 100
            self.maxAnglePerFrame       = .8
            self.mainGun                = 'cannon'
            self.maxSpeed               = 1
##            self.maxSpeed               = 1 #for testing purposes
            self.maxSpeedX              = .2
            self.maxSpeedY              = .2
            self.maxSpeedZ              = .2
            self.accel                  = .005
        if name == 'player-pegasus-broken' :
            if BaseShip.UIDKey >= 1000 :
                self.UID = self.setUid()
            self.name                   = name
            self.missiles               = 25
            self.energy                 = 100
            self.leftHull               = 100
            self.rightHull              = 100
            self.frontHull              = 100
            self.backHull               = 100
            self.maxAnglePerFrame       = .9
            self.mainGun                = 'cannon'
            self.maxSpeed               = 1
            #self.maxSpeed               = 1 #for testing purposes
            self.maxSpeedX              = .2
            self.maxSpeedY              = .2
            self.maxSpeedZ              = .2
            self.accel                  = .01
        if name == 'cruiser' :
            if BaseShip.UIDKey >= 1000 :
                self.UID = self.setUid()
            self.name                   = name
            self.missiles               = 25
            self.energy                 = 100
            self.leftHull               = 100
            self.rightHull              = 100
            self.frontHull              = 100
            self.backHull               = 100
            self.blowupDamage       = 35
            self.maxAnglePerFrame       = .33
            self.mainGun                = 'cannon'
            self.maxSpeed               = .7
            self.accel                  = .05
            self.shipPath               = "Art/mjolnir.bam"
            self.shipModel              = loader.loadModel("Art/mjolnir.bam")

        elif name == 'pegasus-wings' :
            if BaseShip.UIDKey >= 1000 :
                self.UID = self.setUid()
            self.name                   = name
            self.missiles               = 5
            self.energy                 = 100
            self.leftHull               = 100
            self.rightHull              = 100
            self.frontHull              = 100
            self.backHull               = 100
            self.blowupDamage       = 35
            self.maxAnglePerFrame       = .5
            self.mainGun                = 'cannon'
            self.maxSpeed               = 1.1
            self.accel                  = .06
            self.shipPath               = "Art/pegasus_wings.bam"
            self.shipModel              = loader.loadModel("Art/pegasus_wings.bam")
        elif name == 'hawkeye' :
            if BaseShip.UIDKey >= 1000 :
                self.UID = self.setUid()
            self.name                   = name
            self.missiles               = 5
            self.energy                 = 100
            self.leftHull               = 100
            self.rightHull              = 100
            self.frontHull              = 100
            self.backHull               = 100
            self.blowupDamage       = 35
            self.maxAnglePerFrame       = .8
            self.mainGun                = 'cannon'
            self.maxSpeed               = 1.1
            self.accel                  = .06
            self.shipPath               = "Art/hawkeye.bam"
            self.shipModel              = loader.loadModel("Art/hawkeye.bam")
        elif name == 'vulture' :
            if BaseShip.UIDKey >= 1000 :
                self.UID = self.setUid()
            self.name                   = name
            self.missiles               = 5
            self.energy                 = 100
            self.leftHull               = 130
            self.rightHull              = 130
            self.frontHull              = 130
            self.backHull               = 130
            self.blowupDamage       = 35
            self.maxAnglePerFrame       = .7
            self.mainGun                = 'cannon'
            self.maxSpeed               = .9
            self.accel                  = .05
            self.shipPath               = "Art/vulture.bam"
            self.shipModel              = loader.loadModel("Art/vulture.bam")
        elif name == "alienBattleShip":
            if BaseShip.UIDKey >= 1000 :
                self.UID = self.setUid()
            self.name                   = name
            self.missiles               = 25
            self.energy                 = 100
            self.leftHull               = 5000
            self.rightHull              = 5000
            self.frontHull              = 5000
            self.backHull               = 5000
            self.blowupDamage           = 35
            self.maxAnglePerFrame       = .3
            self.mainGun                = 'cannon'
            self.maxSpeed               = .3
            self.accel                  = .005
            self.shipPath               = "Art/cruiser_2.bam"
            self.shipModel              = loader.loadModel("Art/cruiser_1.bam")
        elif name == "humanBattleShip":
            if BaseShip.UIDKey >= 1000 :
                self.UID = self.setUid()
            self.name                   = name
            self.missiles               = 25
            self.energy                 = 100
            self.leftHull               = 500
            self.rightHull              = 500
            self.frontHull              = 500
            self.backHull               = 500
            self.blowupDamage           = 35
            self.maxAnglePerFrame       = .05
            self.mainGun                = 'cannon'
            self.maxSpeed               = .01
            self.accel                  = .005
            self.shipPath               = "Art/cruiser_2.bam"
            self.shipModel              = loader.loadModel("Art/cruiser_2.bam")
            
        else :
            print 'Error: No such ship'
    def getShipModel(self):
            if self.name == 'player-pegasus' :
                return
            else :
                return self.shipModel

    def setNewGun( self , gun ) :
        self.gunType = gun
    def setNewMissile( self , missle ) :
        for x in self.weaponsPayLoad :
            if x == missle :
                return
            else :
                self.weaponsPayLoad.append( missle )
    def setShieldLevel( self, shieldLevel ) :
        self.shields = shieldLevel
    def setName( self , name ) :
        self.name = name
    def setMaxAnglePerFrame( self , mapf ):
        if mapf > 2 :
            mapf = 2
            self.maxAnglePerFrame = mapf
        else :
            self.maxAnglePerFrame = mapf
    def setAmmo( self , ammo ) :
        self.ammo = ammo
    def setHullStrength( self , hull ) :
        self.hull = hull
    def setAccelRate( self , accel ) :
        self.accel = accel
    def setMaxSpeed( self , speed ) :
        self.maxSpeed = speed
    def setMaxSpeedX( self, speed ) :
        self.maxSpeedX = speed
    def setMaxSpeedY( self, speed ) :
        self.maxSpeedY = speed
    def setMaxSpeedZ( self, speed ) :
        self.maxSpeedZ = speed
##    def setActiveMissile( self , missile ) : self.activeMissile = missile


    def getName( self ) :
        return self.name
    def getGunType( self ) :
        return self.gunType
    def getShieldLevel( self ) :
        return self.shields
    def getHullStrength( self ) :
        return self.hull
    def getAmmo( self ) :
        return ammo
    def getMissilePayload( self ) :
        return self.weaponsPayLoad
    def getMaxAnglePerFrame( self ) :
        return self.maxAnglePerFrame
    def getAccelRate( self ) :
        return self.accel
    def getMaxSpeed( self ) :
        return self.maxSpeed
    def getMaxSpeedX( self ) :
        return self.maxSpeedX
    def getMaxSpeedY( self ) :
        return self.maxSpeedY
    def getMaxSpeedZ( self ) :
        return self.maxSpeedZ
##    def getActiveMissile( self ) : return self.activeMissile

    def setUid( self ) :
        BaseShip.UIDKey = BaseShip.UIDKey + 1
        self.UID = BaseShip.UIDKey
    def cycleActiveWeapon( self ) :
        self.x = self.weaponsPayLoad.index(self.activeMissile)
        if self.x < len(self.weaponsPayLoad) - 1 :
            self.x +=1
            self.activeMissile = self.weaponsPayLoad[self.x]
            print self.activeMissile
        else :
            self.activeMissile = self.weaponsPayLoad[0]
            print self.activeMissile

    def cleanUp( self ) :
        if self.name == 'player-pegasus' or self.name == 'player-pegasus-broken' :
            pass
        else:
            self.shipModel.removeNode()
            del self.shipModel

        del self.UID
        del self.name
        #del self.weaponsPayLoad
        #del self.activeMissile
        #del self.ammo
        #del self.shields
        #del self.hull
        del self.maxAnglePerFrame
        del self.mainGun
        del self.maxSpeed
        del self.accel
