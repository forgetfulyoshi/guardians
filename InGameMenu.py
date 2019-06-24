from direct.showbase import DirectObject
from pandac.PandaModules import *
from direct.gui.DirectGui import *

import sys

class InGameMenu(DirectObject.DirectObject):
    def __init__(self):

        self.menuFont = loader.loadFont("Art/fonts/space_age.ttf")
        self.inGameMenuGeom = loader.loadModel("Art/gamemenu.bam")



        self.frame = DirectFrame(image = "Art/textures/gamemenu_bg.png",
                                    scale = .5,
                                    )

        #Set up In Game Menu buttons
        #----------------------------------------------------------------------
        self.resumeButton = DirectButton(geom = (self.inGameMenuGeom.find('**/button_normal'),
                                                self.inGameMenuGeom.find('**/button_click'),
                                                self.inGameMenuGeom.find('**/button_over'),
                                                self.inGameMenuGeom.find('**/button_normal')),
                                            command = self.display,
                                            scale = (.9, 1, .1),
                                            pos = (.01, 0, .6),
                                            relief = None
                                            )
        self.resumeButton.reparentTo(self.frame)

        self.restartButton = DirectButton(geom = (self.inGameMenuGeom.find('**/button_normal'),
                                                self.inGameMenuGeom.find('**/button_click'),
                                                self.inGameMenuGeom.find('**/button_over'),
                                                self.inGameMenuGeom.find('**/button_normal')),
                                            command = self.restart,
                                            scale = (.9, 1, .1),
                                            pos = (.01, 0, .2),
                                            relief = None
                                            )
        self.restartButton.reparentTo(self.frame)

        self.exitToMenuButton = DirectButton(geom = (self.inGameMenuGeom.find('**/button_normal'),
                                                self.inGameMenuGeom.find('**/button_click'),
                                                self.inGameMenuGeom.find('**/button_over'),
                                                self.inGameMenuGeom.find('**/button_normal')),
                                                command = self.exitToMenu,
                                                scale = (.9, 1, .1),
                                                pos = (.01, 0, -.2),
                                                relief = None
                                                )
        self.exitToMenuButton.reparentTo(self.frame)

        self.exitToWindowsButton = DirectButton(geom = (self.inGameMenuGeom.find('**/button_normal'),
                                                self.inGameMenuGeom.find('**/button_click'),
                                                self.inGameMenuGeom.find('**/button_over'),
                                                self.inGameMenuGeom.find('**/button_normal')),
                                                command = exit,
                                                scale = (.9, 1, .1),
                                                pos = (.01, 0, -.6),
                                                relief = None
                                                )
        self.exitToWindowsButton.reparentTo(self.frame)
        #----------------------------------------------------------------------

        #Set up In Game Menu text
        #----------------------------------------------------------------------
        self.resumeText = OnscreenText(text = "Resume",
                                        pos = (0, .58, 0),
                                        font = self.menuFont)
        self.resumeText.reparentTo(self.frame)

        self.restartText = OnscreenText(text = "Restart",
                                        pos = (0, .18, 0),
                                        font = self.menuFont)
        self.restartText.reparentTo(self.frame)

        self.exitToMenuText = OnscreenText(text = "Exit to Menu",
                                            pos = (0, -.22, 0),
                                            font = self.menuFont)
        self.exitToMenuText.reparentTo(self.frame)

        self.exitToWindowsText = OnscreenText(text = "Exit to Windows",
                                                pos = (0, -.62, 0),
                                                font = self.menuFont)
        self.exitToWindowsText.reparentTo(self.frame)
        #----------------------------------------------------------------------
        self.frame.hide()


    def display(self):
        if self.frame.isHidden():
            self.frame.show()
            props = WindowProperties()
            props.setCursorHidden(False)
            base.win.requestProperties(props)
        else:
            self.frame.hide()
            #props = WindowProperties()
            #props.setCursorHidden(True)
            #base.win.requestProperties(props)

    def restart(self):
        self.frame.hide()
        messenger.send('restart')

    def exitToMenu(self):
        self.frame.hide()
        messenger.send('exittomenu')
