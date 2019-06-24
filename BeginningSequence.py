from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *

from SplashScreen import *

class BeginningSequence(DirectObject.DirectObject):
    def __init__(self):
        self.accept('endsplash', self.startGame)
        
        self.loadingImage = OnscreenImage(image = 'Art/textures/loadingcontrols.png',
                                        scale = (1.35, 1, 1))
        self.loadingImage.reparentTo(aspect2d)
        self.loadingImage.hide()
        
        splashScreen = SplashScreen()

    def startGame(self):
        Sequence(Func(self.loadingImage.show),
                    Wait(1),
                    Func(self.loadGame)).start()
                    
    def loadGame(self):
        import GameManager
        self.loadingImage.destroy()
        GameManager.GameManager()
