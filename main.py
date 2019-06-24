from pandac.PandaModules import *
from pandac.PandaModules import loadPrcFileData
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.IntervalGlobal import *

import os
import pickle
import config




config.FARPLANEVAL = 100000
config.configfarplane = ConfigVariableDouble("default-far", config.FARPLANEVAL)
config.textflatten = ConfigVariableInt("text-flatten", 0)
config.TEXT_COLOR = Vec4(.1,.95,.1,9)

#Force the game fullscreen and have a starting resolution of 1280 x 1024
if not os.path.exists('./saveInfo/slotOne'):
    slotOne = open('./saveInfo/slotOne', 'w')
    pickle.dump(['0', 'health', 'ammo', 'armor'], slotOne)
    slotOne.close()
if not os.path.exists('./saveInfo/slotTwo'):
    slotTwo = open('./saveInfo/slotTwo', 'w')
    pickle.dump(['0', 'health', 'ammo', 'armor'], slotTwo)
    slotTwo.close()
if not os.path.exists('./saveInfo/slotThree',):
    slotThree = open('./saveInfo/slotThree', 'w')
    pickle.dump(['0', 'health', 'ammo', 'armor'], slotThree)
    slotThree.close()
if not os.path.exists('./saveInfo/options'):
    optionsFile = open('./saveInfo/options', 'w')
    optionsList = ['1024', '768', 2, .7, 'music', 'sfx']
    pickle.dump(optionsList, optionsFile)
    optionsFile.close()


optionsFile = open('./saveInfo/options')
optionsList = pickle.load(optionsFile)
optionsFile.close()
resolution = "win-size" + ' ' + optionsList[0] + ' ' + optionsList[1]
##loadPrcFileData("", "fullscreen 1")
loadPrcFileData("", resolution)
loadPrcFileData("", "window-title The Guardians")
#ConfigVariableBool("show-frame-rate-meter", #t)
loadPrcFileData("", "show-frame-rate-meter #t")
loadPrcFileData("", "sync-video 0")
#loadPrcFileData("", "want-pstats 1")
#loadPrcFileData("", "premunge-data 0")
import direct.directbase.DirectStart


config.traverser = CollisionTraverser('traverser name')
base.cTrav = config.traverser
config.traverser.traverse(render)
config.collisionHandler = CollisionHandlerEvent()
config.collisionHandler.addInPattern('collide')

base.enableParticles()


from BeginningSequence import *

import pygame


def startGame():
    import GameManager
    loadingImage.hide()
    Sequence(Func(loadingImage.destroy),
                Wait(2),
                Func(GameManager.GameManager)).start()



#prints your windows screen resolution, not the resolution of the game
##print base.pipe.getDisplayWidth()
##print base.pipe.getDisplayHeight()

pygame.init()
pygame.mouse
startGame = BeginningSequence()
run()
pygame.quit()
