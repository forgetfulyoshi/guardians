#Entity.py
# Created - 1/11/2009
#Programmer: Eric Ranaldi
import GameManager
import Missile
import Bullet
import AIPlayer
import CometImmobile
import Asteroid
class EntityManager :
    def __init__( self ) :
        EntityManager.list = []
        EntityManager.started  = 0
        EntityManager.iterator = 0

        #taskMgr.add('Missile Manager Task' , managerTask )
    def start( self ) :
        print 'STARTING Entity MANAGMENT'
        if EntityManager.started == 0 :
            print 'start succesful'
            taskMgr.add( GameManager.EntityMgr.managerTask , 'Entity Manager Task' )
            EntityManager.started = 1

        elif EntityManager.started == 1 :
            return
        else :
            EntityManager.started = 0
            print 'Invalid Value for MissileManager - Deactivating the manager'
            #eventually you would throw a invalid value error here
    def Stop( self ) :
        if EntityManager.started > 0 :
            taskMgr.remove('Entity Manager Task' )
            EntityManager.started = 0
        else :
            return
    def add( self , Entity ) :
        #print Entity
        #print 'added above Entity'
        EntityManager.list.append(Entity)
        #print EntityManager.list
    def managerTask( self , task ) :
        if EntityManager.iterator > len(EntityManager.list) :
            EntityManager.iterator = 0
        elif len(EntityManager.list) == 0 :
            return task.again
        else :

            x = EntityManager.list[EntityManager.iterator - 1]
            if x.__class__ == Missile.Missile and x.missileData.isDead == True :
                x.cleanUp()
                EntityManager.list.remove( x )
                del x
            elif x.__class__ != Missile.Missile and x.isDead == True :
                x.cleanUp()
                EntityManager.list.remove( x )
                del x
##            elif x.__class__ == Bullet.Bullet and x.isDead == 'true' :
##                x.cleanUp()
##                EntityManager.list.remove( x )
##                del x
##            elif x.__class__ == AIPlayer.AIPlayer and x.isDead == 'true' :
##                x.cleanUp()
##                EntityManager.list.remove( x )
##                del x
##            elif x.__class__ == CometImmobile.CometImmobile and x.isDead == 'true':
##                x.cleanUp()
##                EntityManager.list.remove( x )
##                del x
##            elif x.__class__ == Asteroid.Asteroid and x.isDead == 'true':
##                x.cleanUp()
##                EntityManager.list.remove( x )
##                del x
            EntityManager.iterator += 1

        """for x in MissileManager.list :
            #print x
            if x.missileData.isDead == 'true' :
               # print 'killing missile'
                x.cleanUp()
                MissileManager.list.remove( x )
                #return"""
        return task.again
    def cleanUp( self ) :
        del MissileManager.list

    def cleanUpAI(self):
        for entity in EntityManager.list:
            entity.cleanUp()
            EntityManager.list.remove(entity)
            del entity
