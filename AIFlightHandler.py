
from AIDumb import *
from AIRoger import *
from AIBen import *
from AIBattleShip import *
class AIFlightHandler():

    def __init__(self, ship, type, alignment): #position is a vec3
        if type == "dumb":
            self.ai = AIDumb(ship)
        elif type == "smart":
            pass
        elif type == "insane":
            pass
        elif type == "roger":
            self.ai = AIRoger(ship, alignment)
        elif type == "ben":
            self.ai = AIBen(ship, alignment)
        elif type == "battleShip":
            self.ai = AIBattleShip(ship, alignment)
        else:
            pass
    def cleanUp( self ) :
        self.ai.cleanUp()
        del self.ai
