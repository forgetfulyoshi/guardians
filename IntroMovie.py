import threading

from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *
from direct.gui.OnscreenImage import OnscreenImage

class IntroMovie(DirectObject.DirectObject):
    def __init__(self):
        self.acceptOnce('escape', self.escapePressed)
        self.movie = loader.loadTexture("Art/videos/intro2.mpg")
        self.movieImage = OnscreenImage(image = self.movie,
                                        pos = (0,0, .35),
                                        scale = (1.4,1.4,1.4))
        #self.movie.play()
        self.movie.setLoopCount(0)
        self.stopInterval = Sequence()
        self.stopInterval.append(Wait(357))
        self.stopInterval.append(Func(self.escapePressed))
        self.stopInterval.start()
        self.mySound=loader.loadSfx("Art/videos/intro2.mpg")
        self.movie.synchronizeTo(self.mySound)
        #self.movie.play()
        self.mySound.play()


    def delete(self):
        pass
    def escapePressed(self):
        self.mySound.stop()
        messenger.send("gotonextzone")
        
    def cleanUp(self):
        self.ignore('escape')
        self.stopInterval.pause()
        del self.stopInterval
        self.movie.stop()
        self.movieImage.removeNode()
