import threading

from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenImage import OnscreenImage

class SplashScreen(DirectObject.DirectObject):
    def __init__(self):
        base.win.setClearColor(Vec4(0,0,0,1))
        self.acceptOnce('escape', self.escapePressed)
        self.movie = loader.loadTexture("Art/videos/Comp 2.mpg")
        self.movieImage = OnscreenImage(image = self.movie ,pos = (-.1, 0, .7),scale = 1.5)
        self.movie.play()
        self.movie.setLoopCount(0)
        self.stopInterval = Sequence()
        self.stopInterval.append(Wait(11))
        self.stopInterval.append(Func(self.escapePressed))
        self.stopInterval.start()
        #self.stopThread = threading.Timer(5, self.escapePressed).start()
        

    def delete(self):
        pass
    def escapePressed(self):
        self.ignore('escape')
        self.stopInterval.pause()
        del self.stopInterval
        self.movie.stop()
        self.movieImage.removeNode()
        messenger.send("endsplash")
