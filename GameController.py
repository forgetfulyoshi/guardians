from Player import *
from LoadingScreen import *
class GameController():
    def __init__(self):
        #self.loading = LoadingScreen()
        #self.environment = loader.loadModel("environment.egg")
        #self.environment.reparentTo(render)
        self.player = Player()
        #self.loading.finished()

    def cleanUp(self):
        self.player.cleanUp()
        del self.player
